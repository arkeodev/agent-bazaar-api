# src/app/streamlit_auth.py
import logging
from typing import Optional

import requests
import streamlit as st

from ..core.config import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Use the API_BASE_URL from settings
API_BASE_URL = settings.API_BASE_URL


def login_user(username: str, password: str) -> Optional[dict]:
    logger.info(f"Attempting to log in user: {username} on {API_BASE_URL}/api/v1/login")
    response = requests.post(
        f"{API_BASE_URL}/api/v1/login",
        data={"username": username, "password": password},
    )
    if response.status_code == 201:
        logger.info(f"User {username} logged in successfully")
        return response.json()
    else:
        logger.error(
            f"Login failed for user {username}. Status code: {response.status_code}, Response: {response.text}"
        )
    return None


def register_user(
    username: str, email: str, full_name: str, password: str, password_confirm: str
) -> bool:
    logger.info(
        f"Attempting to register user: {username} on {API_BASE_URL}/api/v1/user"
    )
    if password != password_confirm:
        logger.error(f"Password confirmation failed for user {username}")
        return False
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/user",
            json={
                "username": username,
                "email": email,
                "name": full_name,
                "password": password,
            },
        )
        logger.info(f"Registration response status code: {response.status_code}")
        logger.info(f"Registration response content: {response.text}")

        if response.status_code == 201:
            logger.info(f"User {username} registered successfully")
            return True
        else:
            logger.error(
                f"Registration failed for user {username}. Status code: {response.status_code}, Response: {response.text}"
            )
            return False
    except requests.RequestException as e:
        logger.error(f"Error during registration request: {str(e)}")
        return False


def is_logged_in() -> bool:
    return "access_token" in st.session_state


def get_current_user() -> Optional[dict]:
    if not is_logged_in():
        return None

    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    response = requests.get(f"{API_BASE_URL}/api/v1/users/me", headers=headers)

    if response.status_code == 200:
        return response.json()
    return None


def logout_user():
    logger.info("Attempting to log out user on {API_BASE_URL}/api/v1/logout")
    try:
        access_token = st.session_state.get("access_token")
        if not access_token:
            logger.warning("No access token found in session state")
            return True  # User is already logged out

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{API_BASE_URL}/api/v1/logout", headers=headers)

        if response.status_code == 201:
            logger.info("User logged out successfully")
            # Clear session state
            st.session_state.pop("access_token", None)
            # Note: We can't directly manipulate cookies in Streamlit,
            # but the server-side will handle deleting the refresh token
            return True
        else:
            logger.error(
                f"Logout failed. Status code: {response.status_code}, Response: {response.text}"
            )
            return False
    except requests.RequestException as e:
        logger.error(f"Error during logout request: {str(e)}")
        return False


def show_login_modal():
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login", on_click=call_login_user)


def call_login_user():
    username = st.session_state.login_username
    password = st.session_state.login_password
    result = login_user(username, password)
    if result:
        st.session_state["access_token"] = result["access_token"]
        st.success("Logged in successfully!")
        st.experimental_rerun()
    else:
        st.error("Invalid username or password")


def show_register_modal():
    with st.form("register_form", clear_on_submit=True):
        st.subheader("Register")
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        full_name = st.text_input("Full Name", key="register_full_name")
        password = st.text_input("Password", type="password", key="register_password")
        password_confirm = st.text_input(
            "Confirm Password", type="password", key="register_password_confirm"
        )
        submit = st.form_submit_button("Register", on_click=call_register_user)


def call_register_user():
    username = st.session_state.register_username
    email = st.session_state.register_email
    full_name = st.session_state.register_full_name
    password = st.session_state.register_password
    password_confirm = st.session_state.register_password_confirm

    logger.info(f"Registration form submitted for username: {username}")
    if register_user(username, email, full_name, password, password_confirm):
        st.success("Registered successfully! Please login.")
        logger.info(f"User {username} registered successfully")
        st.experimental_rerun()
    else:
        st.error("Registration failed. Please try again.")
        logger.error(f"Registration failed for user {username}")
