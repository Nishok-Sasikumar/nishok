# pages/1_Generate.py

import streamlit as st
import json
import os
from datetime import datetime
import google.generativeai as palm

# Configure Gemini API
palm.configure(api_key="AIzaSyAIXvzvPjXFVBgutzCpp7hKhyMEIFFJdXw")

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

def save_note(note):
    notes = load_notes()
    note['id'] = len(notes) + 1
    note['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes.append(note)
    with open(JSON_FILE, "w") as file:
        json.dump(notes, file, indent=4)

def generate_notes(content, model_name="gemini-1.5-flash"):
    try:
        model = palm.GenerativeModel(model_name=model_name)
        prompt = f"""Generate detailed study notes based on the following content:
{content}

Provide the notes in a valid JSON format with the following structure:
{{
    "title": "Note Title",
    "summary": "A brief summary of the content.",
    "details": "Detailed notes based on the content."
}}

Ensure there is no additional text outside the JSON structure."""
        
        response = model.generate_content(prompt)
        
        # Extract the generated text
        if hasattr(response, '_result') and response._result.candidates:
            candidate = response._result.candidates[0]
            if hasattr(candidate, 'content') and candidate.content.parts:
                content_part = candidate.content.parts[0]
                if hasattr(content_part, 'text'):
                    generated_text = content_part.text.strip()
                    # Clean the generated text if necessary
                    return generated_text[7:-4] if generated_text.startswith("```json") else generated_text
        return None
    except Exception as e:
        st.error(f"Error generating notes: {e}")
        return None

def parse_generated_text(generated_text):
    try:
        note = json.loads(generated_text)
        # Validate required fields
        if all(key in note for key in ("title", "summary", "details")):
            return note
        else:
            st.error("Error: Missing required fields in JSON.")
            return None
    except json.JSONDecodeError as e:
        st.error(f"JSON Decode Error: {e}")
        st.code(generated_text, language='json')
        return None

def main():
    st.title("Generate Notes")
    
    st.header("Enter Content to Generate Notes")
    user_content = st.text_area("Content", height=300)
    
    if st.button("Generate and Save Note"):
        if user_content.strip() == "":
            st.error("Please enter some content to generate notes.")
        else:
            st.info("Generating notes...")
            generated_text = generate_notes(user_content)
            if generated_text:
                st.write("### Generated Notes:")
                st.code(generated_text, language='json')
    
                note = parse_generated_text(generated_text)
                if note:
                    save_note(note)
                    st.success("Note saved successfully!")
                else:
                    st.error("Failed to parse generated notes. Ensure the AI response is in valid JSON format.")
            else:
                st.error("Failed to generate notes.")

if __name__ == "__main__":
    main()