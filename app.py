import streamlit as st
import json
import os
from datetime import datetime
import google.generativeai as palm

# Configure Gemini API
palm.configure(api_key="AIzaSyAIXvzvPjXFVBgutzCpp7hKhyMEIFFJdXw")

# Define JSON file path
JSON_FILE = "notes.json"

# Function to load notes from a JSON file
def load_notes():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r") as file:
        try:
            notes = json.load(file)
            return notes
        except json.JSONDecodeError:
            st.error("Error: JSON file is corrupted.")
            return []

# Function to save a note to the JSON file
def save_note(note):
    notes = load_notes()
    note['id'] = len(notes) + 1
    note['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes.append(note)
    with open(JSON_FILE, "w") as file:
        json.dump(notes, file, indent=4)

# Function to generate notes using AI
def generate_notes(content, model_name="gemini-1.5-flash"):
    try:
        model = palm.GenerativeModel(model_name=model_name)
        prompt = f"""Generate detailed study notes based on the following content:\n{content}\n\nProvide the notes in a valid JSON format with the following structure:\n{{\n    "title": "Note Title",\n    "summary": "A brief summary of the content.",\n    "details": "Detailed notes based on the content."\n}}\n\nEnsure there is no additional text outside the JSON structure."""
        response = model.complete(prompt=prompt)
        return response.result
    except Exception as e:
        st.error(f"Error generating notes: {e}")
        return None

# Home page content
def home():
    st.title("Intelligent Note-Taking Assistant")
    st.markdown("""
    Welcome to the **Intelligent Note-Taking Assistant**! This application helps you generate, save, and view your study notes efficiently using AI-powered technologies.
    
    ### Features:
    - **Generate Notes**: Input your study material, and the assistant will generate detailed notes for you.
    - **View Notes**: Access all your saved notes in one place.
    
    ### Navigation:
    Use the sidebar to navigate between different sections of the application.
    """)

# Page for generating notes
def generate_notes_page():
    st.title("Generate Notes")
    st.write("Enter your study material to generate notes:")
    input_text = st.text_area("Study Material")
    if st.button("Generate Notes"):
        generated_text = generate_notes(input_text)
        if generated_text:
            st.write("### Generated Notes:")
            st.code(generated_text, language='json')

            try:
                note = json.loads(generated_text)
                save_note(note)
                st.success("Note saved successfully!")
            except json.JSONDecodeError:
                st.error("Failed to parse generated notes. Ensure the AI response is in valid JSON format.")
        else:
            st.error("Failed to generate notes.")

# Page for viewing notes
def view_notes_page():
    st.title("View Notes")
    notes = load_notes()

    if notes:
        # Sidebar to list all notes
        with st.sidebar:
            st.title("All Notes")
            selected_note = st.selectbox("Select a note to view", options=[note["title"] for note in notes])

        # Display the content of the selected note
        for note in notes:
            if note["title"] == selected_note:
                st.title(f"{note['title']}")
                st.write(f"**Summary:** {note['summary']}")
                st.write(f"**Details:** {note['details']}")
                st.write(f"**Saved on:** {note['timestamp']}")
                st.markdown("---")
                break
    else:
        st.write("No notes saved yet. Navigate to the 'Generate' page to create your first note.")

# Main function to navigate between pages
def main():
    st.sidebar.title("Navigation")
    menu = ["Home", "Generate Notes", "View Notes"]
    choice = st.sidebar.selectbox("Go to", menu)

    if choice == "Home":
        home()
    elif choice == "Generate Notes":
        generate_notes_page()
    elif choice == "View Notes":
        view_notes_page()

if __name__ == "__main__":
    main()
