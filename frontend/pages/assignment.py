import streamlit as st
import datetime
from menu import menu
from controllers import teams as teams_controller
from controllers import assignment as assignment_controller
import pandas as pd
import app_session_state 
import json

def main():
    menu()

    st.markdown("##### Demandas")

    assignment_tab, assingment_list_tab = st.tabs(["Registrar demanda", "Listar demandas"])

    with assignment_tab:
        register_assignment()
    with assingment_list_tab:
        list_assignments()

def register_assignment():

    assignment_title = st.text_input("Título")
    assignment_description = st.text_area("Descrição")
   
    teams = teams_controller.list()

    #selected_team = None

    if teams:
        # Criar uma lista de tuplas (nome do time, id do time)
        team_options = [(team["name"], team["_id"]) for team in teams]

        # Obter a lista de nomes dos times
        team_names = [team[0] for team in team_options]

        # Usar selectbox para selecionar o índice do time
        team_selected_index = st.selectbox("Atribuído para:", 
                                           range(len(team_names)), 
                                           format_func=lambda x: team_names[x])
        # Obter o ID do time selecionado com base no índice
        team_selected_id = team_options[team_selected_index][1]

        # Encontrar os dados do time selecionado
        selected_team = next((team for team in teams if team["_id"] == team_selected_id), None)
    else:
        st.info("Você precisa adicionar um time para registrar uma demanda.")

    message_placeholder = st.empty()

    if st.button("Registrar"):
        if selected_team and assignment_description:

            assignment_data = {
                "title": assignment_title,
                "description": assignment_description,
                "created_at": datetime.datetime.now().isoformat(),
                "assigned_to": selected_team
            }

            result = assignment_controller.add(assignment_data)

            if result:
                message_placeholder.success("Demanda registrada com sucesso!")
            else:
                message_placeholder.error("Erro ao registrar a demanda.")
        else:
            message_placeholder.info("Preencha todos os campos para registrar a demanda.")

def list_assignments():
    
    assignments = assignment_controller.list()

    if assignments:
        df = pd.DataFrame(assignments)

        if 'select' not in df:
            df.insert(0, "select", False)

        edited_df = st.data_editor(df, 
                                key="assignment_editor_key",
                                num_rows="dynamic",
                                disabled=["_id"],
                                hide_index=True,
                                column_order=["title", "created_at", "select"],
                                column_config={
                                    "_id": st.column_config.Column(disabled=True),
                                    "title": st.column_config.Column("Título"),
                                    "created_at": st.column_config.Column("Criado em"),
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
                if _is_one_row_selected():
                    #_edit_team()
                    selected_team = json.loads(edited_df[edited_df.select].drop('select', axis=1).iloc[0].to_json())
                    st.write(selected_team)
                    app_session_state.set_session_state_editing_team(True, selected_team)
                else:
                    placeholder.info("Selecione um time para editar.")
    else:
        st.write("Não há demandas registradas.")

def _is_pending_save() -> bool:
    if  (st.session_state["assignment_editor_key"]["added_rows"] or
        st.session_state["assignment_editor_key"]["deleted_rows"]):
        return True
    elif (st.session_state["assignment_editor_key"]["edited_rows"] and
        not _is_one_row_selected()):
            return True
    else:
        return False

def _is_one_row_selected():

    if st.session_state["assignment_editor_key"]["edited_rows"]:
        i = 0
        for row in st.session_state["assignment_editor_key"]["edited_rows"]:
            if st.session_state["assignment_editor_key"]["edited_rows"][row]:
                if 'select' in st.session_state["assignment_editor_key"]["edited_rows"][row]:
                    if st.session_state["assignment_editor_key"]["edited_rows"][row]["select"]:
                        i = i + 1
        if i == 1:
            return True
        else:
            return False
    #app_session_state.set_session_state_editing_team(True)

def _save_rows(df: pd.DataFrame):

    result = ""

    if st.session_state["assignment_editor_key"]["added_rows"]:
        result = _add_rows()

    if st.session_state["assignment_editor_key"]["edited_rows"]:
        result = _update_rows(df)

    if st.session_state["assignment_editor_key"]["deleted_rows"]:
        result = _delete_rows(df)

    if result:
        st.success("Atualizado com sucesso!")
    else:
        st.error("Erro ao atualizar.")

    st.rerun()

def _add_rows():
    
    st.write(st.session_state["assignment_editor_key"]["added_rows"])
    for added_row in st.session_state["assignment_editor_key"]["added_rows"]:
        added_row.pop('select')
    st.write(st.session_state["assignment_editor_key"]["added_rows"])
    result = teams_controller.add_many(st.session_state["assignment_editor_key"]["added_rows"])

    return result

def _update_rows(df: pd.DataFrame):
    team_data_to_update = {}
    teams_to_update = []

    for row in st.session_state["assignment_editor_key"]["edited_rows"]:
        st.session_state["assignment_editor_key"]["edited_rows"][row]["_id"] = df.iloc[row]["_id"]
        team_data_to_update = st.session_state["assignment_editor_key"]["edited_rows"][row]
        teams_to_update.append(team_data_to_update)

    result = teams_controller.update_many(teams_to_update)

    return result
    
def _delete_rows(df: pd.DataFrame):
    rows_to_delete = []

    if st.session_state["assignment_editor_key"]["deleted_rows"]:
        for row in st.session_state["assignment_editor_key"]["deleted_rows"]:
            rows_to_delete.append(df.iloc[row]['_id'])
    else:
        for team_id in df:
            rows_to_delete.append(team_id)

    result = assignment_controller.delete_many(rows_to_delete)

    return result


if __name__ == "__main__":
    main()