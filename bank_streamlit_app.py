import streamlit as st
from demo_4_features import main as page_demo_4
from full_input_demo import main as page_full
from about_app import main as page_about_app
from about_project import main as page_about_project
from contact import main as page_contact

# Get the currently selected page from session state (default to About the APP)
default_page = st.session_state.get('page', 'About the App')

# Sidebar title
st.sidebar.title('Navigation')

# Define pages using Streamlit's native navigation (replaces manual radio + if/elif)
pg = st.navigation([
    st.Page(page_demo_4, title='Demo (4 Features)'),
    st.Page(page_full, title='Full Input'),
    st.Page(page_about_app, title='About the App'),
    st.Page(page_about_project, title='About the Project'),
    st.Page(page_contact, title='Contact'),
])

# Run whichever page is currently selected
pg.run()


