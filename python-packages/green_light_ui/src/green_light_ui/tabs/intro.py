import streamlit as st
import pandas as pd
import numpy as np

title = "MLOPS Project Accident Predictions May 24"
subtitle = "GreenLightServices"
sidebar_name = "Introduction"


def run():

    st.title(title)
    st.subheader(subtitle)
    st.markdown("---")

    st.markdown(
        """
        ### Project Description
        In this project we intend to demonstrate core MLOps approaches, processes and tools.
        
        We do so by using a given model with its predictions and evaluations
        and solemly focusing on the MLOps part of providing a service based on an ML-Model. 
        
        As scenario we use a hypothetical service provider 'GreenLightService' that offers the service of predicting 
        the gravity of an accident in France. 
        
        The core components of this service are:
       
        - **Service Platform** to provide the service running in docker-compose
        - **Secured API** with a Prediction endpoint accessed via User Authentication and Authorization (Unit Testing)
        - **User Interface** to make predictions based on the ML Model
        - **Data Ingestion with Airflow** to extract, transform and load new data coming in every year
        - **Automated Training** of the model to include the new data in the predictions
        - **Automated Model Evaluation** to ensure performance of the model
        - **Automated CI/CD processes** to ensure consistent integration and development quality of our work
        - **Service Monitoring** Implemented monitoring tools to track our models performance
        ...
        """
        
    )


# This Streamlit app is designed to interactively present various aspects of our project. Navigate through the following sections:
# Each tab is dedicated to a specific aspect of the project, offering insights and allowing for interactive engagement with the project's outputs.
