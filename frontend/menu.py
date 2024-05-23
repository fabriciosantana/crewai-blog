import streamlit as st

def _authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/ask.py", label="Demandas")
    st.sidebar.page_link("pages/teams.py", label="Times")
    st.sidebar.page_link("pages/generate.py", label="Gerar conteúdo")
    st.sidebar.page_link("pages/list.py", label="Listar conteúdos")
    

    #if st.session_state.role in ["admin", "super-admin"]:
        #st.sidebar.page_link("pages/admin.py", label="Manage users")
        #st.sidebar.page_link(
            #"pages/super-admin.py",
            #label="Manage admin access",
            #disabled=st.session_state.role != "super-admin",
        #)

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    #if "role" not in st.session_state or st.session_state.role is None:
        #unauthenticated_menu()
#        return
    _authenticated_menu()

def _menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    #if "role" not in st.session_state or st.session_state.role is None:
        #st.switch_page("app.py")
    menu()
