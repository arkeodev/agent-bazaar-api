import logging
import os

import streamlit as st
import yaml
from PIL import Image
from pydantic import BaseModel

from src.app.core.logger import logging
from src.app.schemas.agent import Agent
from src.app.streamlit.streamlit_auth import (
    get_current_user,
    is_logged_in,
    login_user,
    logout_user,
    register_user,
)

logger = logging.getLogger(__name__)


# Load agents from the configuration file
def load_agents_from_config(config_file):
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        logger.info(f"Loading config from: {config_file}")
        with open(config_file) as file:
            config = yaml.safe_load(file)

        agents = []
        for agent_data in config["agents"]:
            # Convert relative image path to absolute path
            image_path = os.path.abspath(
                os.path.join(current_dir, agent_data["image_path"])
            )
            agent_data["image_path"] = image_path
            logger.info(f"Agent: {agent_data['name']}, Image path: {image_path}")
            agents.append(Agent(**agent_data))

        return agents
    except Exception as e:
        logger.error(f"Error loading agents from config: {str(e)}")
        return []


# New function to load image using PIL
def load_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {str(e)}")
        return None


# Authentication handling functions
# Handle login submission
def call_login_user():
    # Retrieve username and password from session state
    username = st.session_state.get("login_username", "")
    password = st.session_state.get("login_password", "")

    # Ensure both username and password are provided
    if username and password:
        logger.info(f"Login attempt for username: {username}")
        result = login_user(username, password)
        if result:
            # Store access token in session state if login is successful
            st.session_state["access_token"] = result["access_token"]
            st.success("Logged in successfully!")
            logger.info(f"User {username} logged in successfully")
        else:
            st.error("Invalid username or password")
            logger.error(f"Login failed for user {username}")


# Show login form modal
def show_login_modal():
    with st.form("login_form", clear_on_submit=True):
        st.subheader("Login")
        # Username and password fields
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        st.form_submit_button("Login", on_click=call_login_user)


# Handle registration submission
def call_register_user():
    # Retrieve registration details from session state
    username = st.session_state.get("register_username", "")
    email = st.session_state.get("register_email", "")
    full_name = st.session_state.get("register_full_name", "")
    password = st.session_state.get("register_password", "")
    password_confirm = st.session_state.get("register_password_confirm", "")

    # Check that all fields are filled and passwords match
    if username and email and full_name and password and password == password_confirm:
        logger.info(f"Registration form submitted for username: {username}")
        if register_user(username, email, full_name, password, password_confirm):
            st.success("Registered successfully! Please login.")
            logger.info(f"User {username} registered successfully")
        else:
            st.error("Registration failed. Please try again.")
            logger.error(f"Registration failed for user {username}")
    else:
        st.error("Please fill in all fields correctly.")


# Show registration form modal
def show_register_modal():
    with st.form("register_form", clear_on_submit=True):
        st.subheader("Register")
        # Registration fields
        full_name = st.text_input("Full Name", key="register_full_name")
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        password_confirm = st.text_input(
            "Confirm Password", type="password", key="register_password_confirm"
        )
        st.form_submit_button("Register", on_click=call_register_user)


# Handle user logout
def call_logout_user():
    current_user = get_current_user()
    if current_user:
        logger.info(f"Logout attempt for user: {current_user['username']}")
        if logout_user():
            st.success("Logged out successfully!")
            logger.info(f"User {current_user['username']} logged out successfully")
            st.session_state["logout_success"] = True
        else:
            st.error("Logout failed. Please try again.")
            logger.error(f"Logout failed for user {current_user['username']}")


# Agent handling functions
# Set the current agent and rerun the app
def set_current_agent(name):
    # Set the selected agent in session state and rerun the app to update the UI
    st.session_state["current_agent"] = name
    st.rerun()


# Reset the current agent and rerun the app
def reset_current_agent():
    # Reset the current agent in session state and rerun the app to update the UI
    st.session_state["current_agent"] = None
    st.rerun()


# Display agent details
def agent_detail_page(agent_name):
    # Display the detail page for the selected agent
    st.markdown(f"<h1 class='centered-title'>{agent_name}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 class='centered-text'>You are now using {agent_name}.</h3>",
        unsafe_allow_html=True,
    )
    # Back button to return to the main Agent Bazaar page
    st.button("Back", key="back_button", on_click=reset_current_agent)


# Main application function
def main():
    # Set up the page configuration
    st.set_page_config(page_title="Agent Bazaar", page_icon="🏪", layout="wide")

    # Custom CSS for the menu to hide specific Streamlit elements
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        .auth-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Top menu for login, registration, and logout
    col1, col2, col3, col4 = st.columns([1, 1, 1, 7])

    # Authentication and user actions
    if not is_logged_in():
        # Show login and register buttons if the user is not logged in
        if col1.button("Login"):
            show_login_modal()
        if col2.button("Register"):
            logger.info("Register button clicked")
            show_register_modal()

        # Welcome message when not logged in
        st.markdown(
            "<h1 class='centered-title'>Welcome to Agent Bazaar</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 class='centered-text'>Please login or register to access the agents.</h3>",
            unsafe_allow_html=True,
        )
    else:
        # Show logout button if the user is logged in
        if col1.button("Logout"):
            call_logout_user()
            st.rerun()
        user = get_current_user()
        if user:
            # Display a welcome message with the username
            col2.write(f"Welcome, {user['username']}!")

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to config.yaml
        config_path = os.path.join(current_dir, "config.yaml")

        # Load and display agents from configuration
        agents = load_agents_from_config(config_path)

        # Log the loaded agents
        for agent in agents:
            logger.info(f"Loaded agent: {agent.name}, Image path: {agent.image_path}")

        # Set current agent in session state if not set
        if "current_agent" not in st.session_state:
            st.session_state["current_agent"] = None

        if st.session_state["current_agent"] is None:
            # Display the main Agent Bazaar page
            st.markdown(
                "<h1 class='centered-title'>Agent Bazaar</h1>", unsafe_allow_html=True
            )
            st.markdown(
                "<h3 class='centered-text'>Welcome to Agent Bazaar! Click on an agent to explore its functionality.</h3>",
                unsafe_allow_html=True,
            )

            # Display agents in rows of 3
            for i in range(0, len(agents), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(agents):
                        agent = agents[i + j]
                        with cols[j]:
                            st.markdown(
                                f"<h4 style='text-align: center;'><strong>{agent.name}</strong></h4>",
                                unsafe_allow_html=True,
                            )
                            image = load_image(agent.image_path)
                            if image:
                                st.image(image, use_column_width=True)
                            else:
                                st.error(f"Failed to load image for {agent.name}")
                            st.button(
                                "Use", key=f"use_{agent.name}", use_container_width=True
                            )
        else:
            # Display the agent detail page if an agent is selected
            agent_detail_page(st.session_state["current_agent"])


if __name__ == "__main__":
    main()
