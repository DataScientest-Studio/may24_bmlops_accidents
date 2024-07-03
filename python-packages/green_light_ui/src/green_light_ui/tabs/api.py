import streamlit as st
import pandas as pd
import numpy as np
import requests

title = "Secured API for Model Prediction"
sidebar_name = "API"

def run():
    st.header("Settings")
    st.markdown("""
        We defined JWT_SECRET and JWT_ALGORITHM to generate a JWT token to validate.
        In the environment variables we stored the info ADMIN_USERNAME and ADMIN_PASSWORD for the admin authentication.
    """)
    st.subheader("JWT Settings")
    st.code("""
    # JWT settings
    JWT_SECRET = "secret"
    JWT_ALGORITHM = "HS256"
    """)

    st.subheader("Admin Credentials")
    st.code("""
        # Admin credentials
        ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
        ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    """)
     
    st.header("User Authentication and Authorization")
    st.markdown("""
        We used the hash_password function to hash passwords securely.
        We then created an in-memory users_db dictionary for storing signed up user credentials (username and hashed password).
        These users as well as the admin can sign up to predict.
    """)
    st.code("""
    # In-memory users database
    users_db = {
        "testuser": {
            "username": "testuser",
            "password": pwd_context.hash("testpassword")
        }
    }""")
    st.header("JWT Token Verification")
    st.markdown("""
    A JWT token is created when username and password are correct. The token expires after 10 minutes starting from the time of login.
    With this token one can then access the prediction of the model.
   """)

