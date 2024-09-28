import streamlit as st
import pprint
import google.generativeai as palm
import os
from ics import Calendar, Event
from datetime import datetime, timedelta
import json

# Configure the API key
palm.configure(api_key="AIzaSyBwKThK9t_S2eC5j6CXwpN442Swjukrds0")

# List models and select the appropriate one
model = "gemini-1.5-flash"
print(model)

# Streamlit app title and user input
st.title("Travel Itinerary Generator")

city = st.text_input("Enter the city you're visiting:")
start_date = st.date_input("Select the start date for your trip:", value=datetime.today())

# Set the maximum end date to 30 days after the start date
max_end_date = start_date + timedelta(days=30)

# User selects the end date of the trip
end_date = st.date_input("Select the end date for your trip:", 
                         value=start_date + timedelta(days=1),  # Default to the next day
                         min_value=start_date, 
                         max_value=max_end_date)

# Calculate the number of days between start_date and end_date
days = (end_date - start_date).days

# User preferences checkboxes
art = st.checkbox("Art")
museums = st.checkbox("Museums")
outdoor = st.checkbox("Outdoor Activities")
indoor = st.checkbox("Indoor Activities")
kids_friendly = st.checkbox("Good for Kids")
young_people = st.checkbox("Good for Young People")

# Generate itinerary button
if st.button("Generate Itinerary"):
    # Create a prompt based on user input
    prompt = f"You are a travel expert. Give me an itinerary for {city}, for {days} days, assume each day starting at 10am and ending at 8pm having a buffer of 30 minutes between each activity. I like to"
    if art:
        prompt += " explore art,"
    if museums:
        prompt += " visit museums,"
    if outdoor:
        prompt += " engage in outdoor activities,"
    if indoor:
        prompt += " explore indoor activities,"
    if kids_friendly:
        prompt += " find places suitable for kids,"
    if young_people:
        prompt += " discover places suitable for young people,"

    prompt += """Limit the length of output json string to 1200 characters. Generate a structured JSON representation for the travel itinerary.

       {
  "days": [
    {
      "day": 1,
      "activities": [
        {
          "title": "Activity 1",
          "description": "Description of Activity 1",
          "link": "https://example.com/activity1",
          "start_time": "10:00 AM",
          "end_time": "12:00 PM",
          "location": "https://maps.google.com/?q=location1"
        },
        {
          "title": "Activity 2",
          "description": "Description of Activity 2",
          "link": "https://example.com/activity2",
          "start_time": "02:00 PM",
          "end_time": "04:00 PM",
          "location": "https://maps.google.com/?q=location2"
        },
        ....
      ]
    },
    {
      "day": 2,
      "activities": [
        {
          "title": "Another Activity 1",
          "description": "Description of Another Activity 1",
          "start_time": "09:30 AM",
          "end_time": "11:30 AM",
          "location": "https://maps.google.com/?q=location1"
        },
        {
          "title": "Another Activity 2",
          "description": "Description of Another Activity 2",
          "start_time": "01:00 PM",
          "end_time": "03:00 PM",
          "location": "https://maps.google.com/?q=location2"
        },
        ...
      ]
    }
  ]
}

        Ensure that each day has a 'day' field and a list of 'activities' with 'title', 'description', 'start_time', 'end_time', and 'location' fields. Keep descriptions concise.
"""

    model = palm.GenerativeModel(model_name=model)

    # Call the correct API method
    completion = model.generate_content(
        prompt
    )

    
    # Check if the completion result has candidates and parts
    if hasattr(completion, '_result') and completion._result.candidates:
        candidate = completion._result.candidates[0]
        if hasattr(candidate, 'content') and candidate.content.parts:
            content_part = candidate.content.parts[0]
            if hasattr(content_part, 'text'):
                itinerary_text = content_part.text  

                itinerary_text = itinerary_text.replace("```","").replace("json","")

                print(itinerary_text)
                
                # Attempt to parse the itinerary text as JSON
                itinerary_json = json.loads(itinerary_text)
                st.write("Itinerary JSON loaded successfully.")
                
                # Display the itinerary
                for day in itinerary_json["days"]:
                    st.header(f"Day {day['day']}")
                    for activity in day["activities"]:
                        keys = activity.keys()
                        if "title" in keys:
                            st.subheader(activity["title"])
                        if "description" in keys:
                            st.write(activity["description"])
                        if "link" in keys:
                            st.write(f"Link: {activity['link']}")
                        if "start_time" in keys and "end_time" in keys:
                            st.write(f"Time: {activity['start_time']} - {activity['end_time']}")
                        if "location" in keys:
                            st.write(f"Location: {activity['location']}")
                        st.write("---")                            
            else:
                st.error("No text found in the content part.")
        else:
            st.error("No content parts found in the candidate.")
    else:
        st.error("No candidates found in the completion result.")

