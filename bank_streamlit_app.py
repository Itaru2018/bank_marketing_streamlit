import streamlit as st

from demo_4_features import main as page_demo_4
from full_input_demo import main as page_full
from about_app import main as page_about_app
from about_project import main as page_about_project
from contact import main as page_contact


page_names = [
    'Demo (4 Features)',
    'Full Input',
    'About the App',
    'About the Project',
    'Contact',
]


# Set the default page only once
if 'page' not in st.session_state:
    st.session_state.page = 'About the App'

# Protect against an invalid stored page
if st.session_state.page not in page_names:
    st.session_state.page = 'About the App'


# Sidebar page selector
st.sidebar.title('Navigation')

page = st.sidebar.radio(
    'Choose a page',
    page_names,
    key='page',
)


# Run selected page
if page == 'Demo (4 Features)':
    page_demo_4()

elif page == 'Full Input':
    page_full()

elif page == 'About the App':
    page_about_app()

elif page == 'About the Project':
    page_about_project()

else:
    page_contact()

