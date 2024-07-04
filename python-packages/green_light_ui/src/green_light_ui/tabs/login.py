import streamlit as st
import requests
import config
import sys
from pathlib import Path
from passlib.context import CryptContext

# sidebar_name = "Admin Login"

# def run_adminlogin():
#     # st.title("Admin Login Demo")

#     # with st.form("login_form"):
#     #     st.write("Enter your admin credentials:")
#     #     username = st.text_input("Username")
#     #     password = st.text_input("Password", type="password")
#     #     submit_button = st.form_submit_button(label="Login")

#     # if submit_button:
#     #     token = authenticate_user(config.ADMIN_USERNAME , password)
#     #     if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
#     #         st.success("Login successful!")
#     #         st.write("You are logged in as admin.")
#     #     else:
#     #         st.error("Invalid username or password. Please try again!")
            
#     # if submit_button:
#     #         token = authenticate_user(username, password)
#     #         if token:
#     #             st.success("Login successful!")
#     #             st.write(f"You are logged in as {username}.")
#     #             st.write("Here is your JWT token:")
#     #             st.code(token)
#     #         else:
#     #             st.error("Invalid username or password")

#     st.write("""
#     ### Instructions:
#     1. Enter the admin credentials (stored in the .env) in the form above.
#     2. Click on the "Login" button to authenticate.
#     """)

# pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__default_rounds=12, deprecated="auto")

# # In-memory users database from the api.py in modelAPI
# users_db = {
#     "testuser": {
#         "username": "testuser",
#         "password": pwd_context.hash("testpassword")
#     }
# }

# st.code("""
#     # In-memory users database from the api.py in modelAPI
#     users_db = {
#         "testuser": {
#             "username": "testuser",
#             "password": pwd_context.hash("testpassword")
#         }
#     }
#     """)

# #hashes a string password using bcrypt   
# def hash_password(password: str):
#     return pwd_context.hash(password)

# def run_usersignup():
#     st.title("User Signup Demo")

#     with st.form("signup_form"):
#         st.write("Enter your credentials to sign up:")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submit_button = st.form_submit_button(label="Sign Up")

#     if submit_button:
#         if username in users_db:
#             st.error("Username already exists")
#         else:
#             users_db[username] = {"username": username, "password": hash_password(password)}
#             st.success("Signup successful!")
#             st.write("You have signed up.")


     