import streamlit as st

def init():
    print("init session")

def set_session_state_adding_team(adding_team: bool):
    st.session_state.adding_team = adding_team
    st.session_state.editing_team = not adding_team
    st.session_state.listing_team = not adding_team

    st.session_state.adding_agent = not adding_team
    st.session_state.editing_agent = not adding_team

    st.session_state.adding_task = not adding_team
    st.session_state.editing_task = not adding_team

    st.rerun()

def set_session_state_editing_team(editing_team: bool, team):
    st.session_state.adding_team = not editing_team
    st.session_state.editing_team = editing_team
    st.session_state.listing_team = not editing_team

    st.session_state.adding_agent = not editing_team
    st.session_state.editing_agent = not editing_team

    st.session_state.adding_task = not editing_team
    st.session_state.editing_task = not editing_team

    st.session_state.team = team

    st.rerun()

def set_session_state_listing_team(listing_team: bool):
    st.session_state.adding_team = not listing_team
    st.session_state.editing_team = not listing_team
    st.session_state.listing_team = listing_team
    
    st.session_state.adding_agent = not listing_team
    st.session_state.editing_agent = not listing_team

    st.session_state.adding_task = not listing_team
    st.session_state.editing_task = not listing_team

    st.rerun()

def set_session_state_adding_agent(adding_agent: bool):
    
    st.session_state.adding_team = not adding_agent
    st.session_state.listing_team = not adding_agent
    st.session_state.editing_team = not adding_agent
    
    st.session_state.adding_agent = adding_agent
    st.session_state.editing_agent = not adding_agent

    st.session_state.adding_task = not adding_agent
    st.session_state.editing_task = not adding_agent

    st.rerun()

def set_session_state_editing_agent(editing_agent: bool, team, agent):
    st.session_state.adding_team = not editing_agent
    st.session_state.editing_team = not editing_agent
    st.session_state.listing_team = not editing_agent
    
    st.session_state.adding_agent = not editing_agent
    st.session_state.editing_agent = editing_agent

    st.session_state.adding_task = not editing_agent
    st.session_state.editing_task = not editing_agent
    
    st.session_state.team = team 
    st.session_state.agent = agent
    st.rerun()

def set_session_state_adding_task(adding_task: bool, team, agent):
    st.session_state.adding_team = not adding_task
    st.session_state.editing_team = not adding_task
    st.session_state.listing_team = not adding_task
    
    st.session_state.adding_agent = not adding_task
    st.session_state.editing_agent = not adding_task

    st.session_state.adding_task = adding_task
    st.session_state.editing_task = not adding_task
    
    st.session_state.team = team 
    st.session_state.agent = agent
    st.rerun()

def set_session_state_editing_task(editing_task: bool, team, agent, task):
    st.session_state.adding_team = not editing_task
    st.session_state.editing_team = not editing_task
    st.session_state.listing_team = not editing_task
    
    st.session_state.adding_agent = not editing_task
    st.session_state.editing_agent = not editing_task

    st.session_state.adding_task = not editing_task
    st.session_state.editing_task = editing_task
    
    st.session_state.team = team 
    st.session_state.agent = agent
    st.session_state.task = task

    st.rerun()