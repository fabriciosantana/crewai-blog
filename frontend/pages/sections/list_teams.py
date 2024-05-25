import streamlit as st
from controllers import teams as teams_controller
import app_session_state
from pages.sections import edit_team as edit_team_section
import pandas as pd
import app_session_state 
import json

def show():
    
    teams = teams_controller.list()

    if teams:
        _new_display_teams_grid(teams)
    else:
        _display_empty_grid()
    
def _display_teams_grid(teams):
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Lista de Times")

    with col2:
        if st.button("Adicionar Time", type="primary"):
            app_session_state.set_session_state_adding_team(True)
            
    cols = st.columns(3)
    fields = ["Nome do Time"]

    # header
    for col, field in zip(cols, fields):
        col.write("**" + field + "**")

    # rows
    for team in teams:
        
        col1, col2, col3 = st.columns(3)
        col1.write(team["name"])

        alter_placeholder = col2.empty()
        delete_placeholder = col3.empty()

        if alter_placeholder.button("Editar", key="alter_" + team["_id"]):
            #print(f"team antes do session state {team}")
            app_session_state.set_session_state_editing_team(True, team)

        if delete_placeholder.button("Excluir", key="delete_" + team["_id"]):
            result = teams_controller.delete(team["_id"])
            if result:
                st.success(f"Time {team['name']} excluído com sucesso!")                
            else:
                st.error(f"Erro ao excluir time {team['name']}")
            app_session_state.set_session_state_listing_team(True)

def _new_display_teams_grid(teams):
    
    st.markdown("##### Lista de Times")

    #st.write(teams)

    df = pd.DataFrame(teams)

    if 'select' not in df:
        df.insert(0, "select", False)

    edited_df = st.data_editor(df, 
                               key="my_key",
                               num_rows="dynamic",
                               disabled=["_id"],
                               hide_index=True,
                               column_order=["name", "select"],
                               column_config={
                                   "_id": st.column_config.Column(disabled=True),
                                   "name": st.column_config.Column("Nome"),
                                   "select": st.column_config.CheckboxColumn("", required=True, default=False)
                               },
                               use_container_width=True)

    placeholder = st.empty()

    if _is_pending_save():
        placeholder.info("Clique no botão 'Salvar' para salvar alterações pendentes.")
        placeholder.warning("Ao clicar em 'Salvar' todas as alterações serão gravadas no banco de dados.")
    else:
        placeholder.empty()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Salvar", type="primary"):
            _save_rows(df.drop('select', axis=1))
    with col2:
        if st.button("Editar"):
            if _is_one_team_selected():
                #_edit_team()
                selected_team = json.loads(edited_df[edited_df.select].drop('select', axis=1).iloc[0].to_json())
                st.write(selected_team)
                app_session_state.set_session_state_editing_team(True, selected_team)
            else:
                placeholder.info("Selecione um time para editar.")

def _is_pending_save() -> bool:
    if  (st.session_state["my_key"]["added_rows"] or
        st.session_state["my_key"]["deleted_rows"]):
        return True
    elif (st.session_state["my_key"]["edited_rows"] and
        not _is_one_team_selected()):
            return True
    else:
        return False

def _is_one_team_selected():

    if st.session_state["my_key"]["edited_rows"]:
        i = 0
        for row in st.session_state["my_key"]["edited_rows"]:
            if st.session_state["my_key"]["edited_rows"][row]:
                if 'select' in st.session_state["my_key"]["edited_rows"][row]:
                    if st.session_state["my_key"]["edited_rows"][row]["select"]:
                        i = i + 1
        if i == 1:
            return True
        else:
            return False
    #app_session_state.set_session_state_editing_team(True)

def _save_rows(df: pd.DataFrame):

    result = ""

    if st.session_state["my_key"]["added_rows"]:
        result = _add_rows()

    if st.session_state["my_key"]["edited_rows"]:
        result = _update_rows(df)

    if st.session_state["my_key"]["deleted_rows"]:
        result = _delete_rows(df)

    if result:
        st.success("Atualizado com sucesso!")
    else:
        st.error("Erro ao atualizar.")

    st.rerun()

def _add_rows():
    
    st.write(st.session_state["my_key"]["added_rows"])
    for added_row in st.session_state["my_key"]["added_rows"]:
        added_row.pop('select')
    st.write(st.session_state["my_key"]["added_rows"])
    result = teams_controller.add_many(st.session_state["my_key"]["added_rows"])

    return result

def _update_rows(df: pd.DataFrame):
    team_data_to_update = {}
    teams_to_update = []

    for row in st.session_state["my_key"]["edited_rows"]:
        st.session_state["my_key"]["edited_rows"][row]["_id"] = df.iloc[row]["_id"]
        team_data_to_update = st.session_state["my_key"]["edited_rows"][row]
        teams_to_update.append(team_data_to_update)

    result = teams_controller.update_many(teams_to_update)

    return result
    
def _delete_rows(df: pd.DataFrame):
    team_ids_to_delete = []

    if st.session_state["my_key"]["deleted_rows"]:
        for row in st.session_state["my_key"]["deleted_rows"]:
            team_ids_to_delete.append(df.iloc[row]['_id'])
    else:
        for team_id in df:
            team_ids_to_delete.append(team_id)

    result = teams_controller.delete_many(team_ids_to_delete)

    return result

def _display_empty_grid():
    st.markdown("##### Você ainda não tem um time.")
    st.write("Clique no botão abaixo para adicionar um time.")
    if st.button("Adicionar Time", type="primary"):
        app_session_state.set_session_state_adding_team(True)