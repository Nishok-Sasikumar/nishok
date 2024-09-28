import streamlit as st
import json
import os

# Define JSON file path
JSON_FILE = "notes.json"

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

def get_all_notes():
    return load_notes()

def main():
    
    notes = get_all_notes()
    
    if notes:
        # Sidebar to list all notes
        with st.sidebar:
            st.title("All Notes")
            # Create a dictionary to store the selected note
            selected_note = st.selectbox(
                "Select a note to view",
                options=[note["title"] for note in notes]
            )
        
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

if __name__ == "__main__":
    main()
