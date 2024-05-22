import streamlit as st
from controllers import teams as teams_controller
import app_session_state


def show(team_id: str, agent_id: str):
    print("show edit agent")