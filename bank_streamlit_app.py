import streamlit as st

page_names = [
    "Demo (4 Features)",
    "Full Input",
    "About the App",
    "About the Project",
    "Contact",
]

# Initialize only once
if "page" not in st.session_state:
    st.session_state.page = default_page

# Protect against an invalid/default page name
if st.session_state.page not in page_names:
    st.session_state.page = page_names[0]

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    page_names,
    key="page",
)

# Run selected page
if page == "Demo (4 Features)":
    page_demo_4()

elif page == "Full Input":
    page_full()

elif page == "About the App":
    page_about_app()

elif page == "About the Project":
    page_about_project()

elif page == "Contact":
    page_contact()


