# -*- coding: utf-8 -*-

# This model was reworked by JH on 26/06/2024 and ff to fit in our GreenLightService model
from pathlib import Path
import os

import pandas as pd
import numpy as np
from pathlib import Path
import click
import logging
from sklearn.model_selection import train_test_split
from check_structure import (
    check_existing_file,
    check_existing_folder,
    mv_existing_file_archive,
)
from sqlalchemy import create_engine
from dotenv import load_dotenv

from road_accidents_database_ingestion.db_tasks import get_db_url

load_dotenv()  # take environment variables from .env.

db_url = get_db_url()

model_base = "/models"
data_base = "/data"


def main(input_filepath, output_filepath):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../preprocessed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")

    # JH: Changed to Volume folder.
    output_filepath = data_base + "/preprocessed"
    # Call the main data processing function with the provided file paths
    process_data(output_filepath)


def process_data(
    output_folderpath,
    users_table="users",
    caract_table="caracteristiques",
    places_table="lieux",
    veh_table="vehicules",
):
    output_folderpath = Path(output_folderpath)

    # --Fetch dataframes from db
    print("Fetching dataframes from the DB")
    raw_sql_query = "SELECT * FROM {table}"
    # cnx = create_engine(db_url).connect()
    # JH: changed to .raw_connection() to avoid ... no cursor.... problem
    cnx = create_engine(db_url).raw_connection()
    df_caract = pd.read_sql_query(raw_sql_query.format(table=caract_table), con=cnx)
    df_places = pd.read_sql_query(
        raw_sql_query.format(table=places_table), con=cnx
    ).drop("id", axis=1, errors=False)
    df_users = pd.read_sql_query(raw_sql_query.format(table=users_table), con=cnx).drop(
        "id", axis=1, errors=False
    )
    df_veh = pd.read_sql_query(raw_sql_query.format(table=veh_table), con=cnx)

    # --Creating new columns
    nb_victim = pd.crosstab(df_users.Num_Acc, "count").reset_index()
    nb_vehicules = pd.crosstab(df_veh.Num_Acc, "count").reset_index()
    df_users["year_acc"] = (
        df_users["Num_Acc"].astype(str).apply(lambda x: x[:4]).astype(int)
    )
    df_users["victim_age"] = df_users["year_acc"] - df_users["an_nais"]
    for i in df_users["victim_age"]:
        if (i > 120) | (i < 0):
            df_users["victim_age"].replace(i, np.nan)
    df_caract["hour"] = df_caract["hrmn"].astype(str).apply(lambda x: x[:-3])
    df_caract.drop(["hrmn", "an"], inplace=True, axis=1)
    df_users.drop(["an_nais"], inplace=True, axis=1)

    # --Replacing names
    df_users.grav.replace([1, 2, 3, 4], [1, 3, 4, 2], inplace=True)
    df_caract.rename({"agg": "agg_"}, inplace=True, axis=1)
    corse_replace = {"2A": "201", "2B": "202"}
    df_caract["dep"] = df_caract["dep"].str.replace("2A", "201")
    df_caract["dep"] = df_caract["dep"].str.replace("2B", "202")
    df_caract["com"] = df_caract["com"].str.replace("2A", "201")
    df_caract["com"] = df_caract["com"].str.replace("2B", "202")

    # --Converting columns types
    df_caract["dep"] = pd.to_numeric(df_caract["dep"], errors="coerce").notnull().astype(int)
    df_caract["com"] = pd.to_numeric(df_caract["com"], errors="coerce").notnull().astype(int)
    df_caract["hour"] = pd.to_numeric(df_caract["hour"], errors="coerce").notnull().astype(int)
    
    # df_caract[["dep", "com", "hour"]] = df_caract[["dep", "com", "hour"]].astype(int)

    dico_to_float = {"lat": float, "long": float}
    df_caract["lat"] = df_caract["lat"].str.replace(",", ".")
    df_caract["long"] = df_caract["long"].str.replace(",", ".")
    df_caract = df_caract.astype(dico_to_float)

    # --Grouping modalities
    dico = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 0, 9: 0}
    df_caract["atm"] = df_caract["atm"].replace(dico)
    catv_value = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        50,
        60,
        80,
        99,
    ]
    catv_value_new = [
        0,
        1,
        1,
        2,
        1,
        1,
        6,
        2,
        5,
        5,
        5,
        5,
        5,
        4,
        4,
        4,
        4,
        4,
        3,
        3,
        4,
        4,
        1,
        1,
        1,
        1,
        1,
        6,
        6,
        3,
        3,
        3,
        3,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
    ]
    df_veh["catv"].replace(catv_value, catv_value_new, inplace=True)

    # --Merging datasets
    fusion1 = df_users.merge(
        df_veh, on=["Num_Acc", "num_veh", "id_vehicule"], how="inner"
    )
    fusion1 = fusion1.sort_values(by="grav", ascending=False)
    fusion1 = fusion1.drop_duplicates(subset=["Num_Acc"], keep="first")
    fusion2 = fusion1.merge(df_places, on="Num_Acc", how="left")
    df = fusion2.merge(df_caract, on="Num_Acc", how="left")

    # --Adding new columns
    df = df.merge(nb_victim, on="Num_Acc", how="inner")
    df.rename({"count": "nb_victim"}, axis=1, inplace=True)
    df = df.merge(nb_vehicules, on="Num_Acc", how="inner")
    df.rename({"count": "nb_vehicules"}, axis=1, inplace=True)

    # --Modification of the target variable  : 1 : prioritary // 0 : non-prioritary
    df["grav"].replace([2, 3, 4], [0, 1, 1], inplace=True)

    # --Replacing values -1 and 0
    col_to_replace0_na = ["trajet", "catv", "motor"]
    col_to_replace1_na = [
        "trajet",
        "secu1",
        "catv",
        "obsm",
        "motor",
        "circ",
        "surf",
        "situ",
        "vma",
        "atm",
        "col",
    ]
    df[col_to_replace1_na] = df[col_to_replace1_na].replace(-1, np.nan)
    df[col_to_replace0_na] = df[col_to_replace0_na].replace(0, np.nan)

    # --Dropping columns
    list_to_drop = [
        "senc",
        "larrout",
        "actp",
        "manv",
        "choc",
        "nbv",
        "prof",
        "plan",
        "Num_Acc",
        "id_vehicule",
        "num_veh",
        "pr",
        "pr1",
        "voie",
        "trajet",
        "secu2",
        "secu3",
        "adr",
        "v1",
        "lartpc",
        "occutc",
        "v2",
        "vosp",
        "locp",
        "etatp",
        "infra",
        "obs",
    ]
    df.drop(list_to_drop, axis=1, inplace=True)

    # --Dropping lines with NaN values
    col_to_drop_lines = ["catv", "vma", "secu1", "obsm", "atm"]
    df = df.dropna(subset=col_to_drop_lines, axis=0)

    target = df["grav"]
    feats = df.drop(["grav"], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        feats, target, test_size=0.3, random_state=42
    )

    # --Filling NaN values
    col_to_fill_na = ["surf", "circ", "col", "motor"]
    X_train[col_to_fill_na] = X_train[col_to_fill_na].fillna(
        X_train[col_to_fill_na].mode().iloc[0]
    )
    X_test[col_to_fill_na] = X_test[col_to_fill_na].fillna(
        X_train[col_to_fill_na].mode().iloc[0]
    )

    # Create folder if necessary
    output_folderpath.mkdir(parents=True, exist_ok=True)

    mv_existing_file_archive(output_folderpath)

    # --Saving the dataframes to their respective output file paths
    for file, filename in zip(
        [X_train, X_test, y_train, y_test], ["X_train", "X_test", "y_train", "y_test"]
    ):
        output_filepath = output_folderpath / f"{filename}.csv"
        file.to_csv(output_filepath, index=False)
        print("Saved preprocessed file:", filename)


# if __name__ == '__main__':
#     log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_fmt)

#     # not used in this stub but often useful for finding various files
#     project_dir = Path(__file__).resolve().parents[2]


#     main()
