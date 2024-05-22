import streamlit as st
from menu import menu

from pages.sections import list_teams as list_teams_section
from pages.sections import add_team as add_team_section
from pages.sections import edit_team as edit_team_section

from pages.sections import add_agent as add_agent_section
from pages.sections import edit_agent as edit_agent_section

from pages.sections import add_task as add_task_section
from pages.sections import edit_task as edit_task_section

def main():

    menu()

    if 'team' not in st.session_state:
        st.session_state.team = {}
    if 'adding_team' not in st.session_state:
        st.session_state.adding_team = False
    if 'editing_team' not in st.session_state:
        st.session_state.editing_team = False
    if 'listing_team' not in st.session_state:
        st.session_state.listing_team = False
    if 'adding_agent' not in st.session_state:
        st.session_state.adding_agent = False
    if 'editing_agent' not in st.session_state:
        st.session_state.editing_agent = False
    if 'agent_template' not in st.session_state:
        st.session_state.agent_template = {}
    if 'agent' not in st.session_state:
        st.session_state.agent = {}
    if 'adding_task' not in st.session_state:
        st.session_state.adding_task = False
    if 'editing_task' not in st.session_state:
        st.session_state.editing_task = False
    if 'task_template' not in st.session_state:
        st.session_state.task_template = {}

    if st.session_state.adding_team:
        add_team_section.show()
    elif st.session_state.editing_team:
        edit_team_section.show(st.session_state.team)
    elif st.session_state.listing_team:
        list_teams_section.show()
    elif st.session_state.adding_agent:
        add_agent_section.show(st.session_state.team)
    elif st.session_state.editing_agent:
        edit_agent_section.show(st.session_state.team, st.session_state.agent)
    elif st.session_state.adding_task:
        add_task_section.show(st.session_state.team, st.session_state.agent)
    elif st.session_state.editing_task:
        edit_task_section.show(st.session_state.team, st.session_state.agent, st.session_state.task)
    else:
        list_teams_section.show()

if __name__ == "__main__":
    main()