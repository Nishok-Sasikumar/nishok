# app.py

import streamlit as st

def main():
    st.title("Intelligent Note-Taking Assistant")
    
    st.markdown("""
    Welcome to the **Intelligent Note-Taking Assistant**! This application helps you generate, save, and view your study notes efficiently using AI-powered technologies.

    ### Features:
    - **Generate Notes**: Input your study material, and the assistant will generate detailed notes for you.
    - **View Notes**: Access all your saved notes in one place.

    ### Navigation:
    Use the sidebar to navigate between different sections of the application.
    """)

if __name__ == "__main__":
    main()
