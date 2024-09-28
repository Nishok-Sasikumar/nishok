import json
content = """
{
  "days": [
    {
      "day": 1,
      "activities": [
        {
          "title": "Salem Museum",
          "description": "Learn about the history of Salem, Tamil Nadu.",
          "link": "https://www.salemmuseum.org/",
          "start_time": "10:00 AM",
          "end_time": "12:00 PM",
          "location": "https://goo.gl/maps/h5uY18gM5H8J89bG8"
        },
        {
          "title": "Lunch at Annapoorna",
          "description": "Enjoy delicious South Indian food.",
          "link": "https://www.zomato.com/salem/annapoorna-hotel-near-new-bus-stand-salem",
          "start_time": "12:30 PM",
          "end_time": "01:30 PM",
          "location": "https://goo.gl/maps/o9a8q2Z1d6w32j9t7"
        },
        {
          "title": "Kailasanathar Temple",
          "description": "A beautiful temple dedicated to Lord Shiva.",
          "link": "https://www.tripadvisor.com/Attraction_Review-g471337-d3941737-Reviews-Kailasanathar_Temple-Salem_Tamil_Nadu.html",
          "start_time": "02:00 PM",
          "end_time": "04:00 PM",
          "location": "https://goo.gl/maps/886B5n9b1Z44X6bH9"
        },
        {
          "title": "Salem Botanical Garden",
          "description": "Relax and explore the beautiful gardens.",
          "link": "https://www.google.com/search?q=salem+botanical+garden&oq=salem+botanical+garden&aqs=chrome..69i57j0l2j46j69i60l2.1376j0j4&sourceid=chrome&ie=UTF-8",
          "start_time": "04:30 PM",
          "end_time": "06:30 PM",
          "location": "https://goo.gl/maps/K9V9b76wY8Qh2hC98"
        },
        {
          "title": "Evening Snacks at Hotel Grand",
          "description": "Enjoy some local snacks and refreshments.",
          "link": "https://www.zomato.com/salem/hotel-grand-near-new-bus-stand-salem",
          "start_time": "07:00 PM",
          "end_time": "08:00 PM",
          "location": "https://goo.gl/maps/Y52C5wQ9oU683rZ58"
        }
      ]
    }
  ]
}
"""



json_data = json.loads(content)
print(json_data)