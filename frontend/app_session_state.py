import streamlit as st

def set_session_state_adding_team(adding_team: bool):
    st.session_state.adding_team = adding_team
    st.session_state.editing_team = not adding_team
    st.session_state.listing_team = not adding_team

    st.session_state.adding_agent = not adding_team
    st.session_state.editing_agent = not adding_team

    st.rerun()

def set_session_state_editing_team(editing_team: bool, team_id: str):
    st.session_state.adding_team = not editing_team
    st.session_state.editing_team = editing_team
    st.session_state.listing_team = not editing_team

    st.session_state.adding_agent = not editing_team
    st.session_state.editing_agent = not editing_team

    st.session_state.team_id = team_id 
    st.rerun()

def set_session_state_listing_team(listing_team: bool):
    st.session_state.adding_team = not listing_team
    st.session_state.editing_team = not listing_team
    st.session_state.listing_team = listing_team
    
    st.session_state.adding_agent = not listing_team
    st.session_state.editing_agent = not listing_team

    st.rerun()

def set_session_state_adding_agent(adding_agent: bool, team_id: str):
    
    st.session_state.adding_team = not adding_agent
    st.session_state.listing_team = not adding_agent
    st.session_state.editing_team = not adding_agent
    
    st.session_state.adding_agent = adding_agent
    st.session_state.editing_agent = not adding_agent

    st.session_state.team_id = team_id 
    st.rerun()

def set_session_state_editing_agent(editing_agent: bool, team_id: str, agent_id: str):
    st.session_state.adding_team = not editing_agent
    st.session_state.editing_team = not editing_agent
    st.session_state.listing_team = not editing_agent
    
    st.session_state.adding_agent = not editing_agent
    st.session_state.editing_agent = editing_agent
    
    st.session_state.team_id = team_id 
    st.session_state.agent_id = agent_id 
    st.rerun()