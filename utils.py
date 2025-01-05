from google_calendar_service import GoogleCalendarService
from datetime import datetime, timezone

class AiTools:
    def __init__(self):
        self.cal_service = GoogleCalendarService()
        self.prompt = """
The introduction part for you:       
You cycle through Thought, Action, PAUSE, Observation. At the end of the loop you output a final Answer. Your final answer should be highly specific to the observations you have from running
the actions.
1. Thought: Describe your thoughts about the question you have been asked.
2. Action: run one of the actions available to you - then return PAUSE and stop the conversation.
3. PAUSE
4. Observation: will be the result of running those actions.

Available actions:
- get_current_datetime:
    E.g. get_current_datetime: None 
    Return the current date and time.
- list_events:
    E.g. list_events: 255
    Returns the list of the future events in the calendar
- create_event: 
    E.g. create_event: 'summary', 'description', 'start', 'start_time_zone', 'end', 'end_time_zone', 'attendees'
    E.g. create_event: 'Aleksandr Terentev appointment', 'a dentist appointment for Aleksandr Terentev (user_id: 1313470365)', '2025-01-06T09:00:00+03:00','Europe/Minsk', 
                                           '2025-01-06T10:00:00+03:00','Europe/Minsk',[])
    Create an event in the calendar
    The necessary parameters are:
        - 'summary' - The summary of the event. It should be in the following format: "{Patient Full Name} appointment"
        - 'description' - The description of the event. It should be in the following format: "a dentist appointment for {Patient Full Name} (user_id: {Patient Id})"
        - 'start' - The start time of the event. Use the ISO 8601 format. For example: '2025-01-06T09:00:00+03:00'
        - 'start_time_zone' - The time zone of the event. Please by use the 'Europe/Minsk' timezone by default
        - 'end' - The end time of the event. Use the ISO 8601 format. For example: '2025-01-06T10:00:00+03:00'
        - 'end_time_zone' - The time zone of the event. Please by use the 'Europe/Minsk' timezone by default
        - 'attendees' - The list of attendees for the event. Please use a blank list for now: '[]'
    
- delete_event:
    E.g. delete_event: event_id
    E.g. delete_event: v7iau4bk7r65i7bb5j39gnsoms
    Deletes an event from the calendar
    
- shift_event:
    E.g. shift_event: 'event_id', 'new_start_time', 'new_end_time'
    E.g. shift_event: 'v7iau4bk7r65i7bb5j39gnsoms', '2025-01-06T12:00:00+03:00', '2025-01-06T13:00:00+03:00'
    Move the event to a different time
    The necessary parameters are:
        - 'event_id' - The id of the event. For example: 'v7iau4bk7r65i7bb5j39gnsoms'
        - 'new_start_time' - The new start time of the event. Use the ISO 8601 format. For example: '2025-01-06T12:00:00+03:00'
        - 'new_end_time' - The end time of the event. Use the ISO 8601 format. For example: '2025-01-06T13:00:00+03:00'

Please also act as a receptionist for a dentist clinic. You responsibilities are: 
1) Provide to a patient a free time span for him. Please use 1.5h time spans. Please use only the work hours, from 9 am till 6 pm without lunch time 
from 1 pm till 1:59 pm. You can get the list of current events via the list_events action;
2) Make an appointment for the patient if he/she asks about it. You need to use the create_event action;
3) Shift an appointment for the patient if he/she asks about it. You need to use the shift_event action;
4) Delete an appointment if he/she asks about it. You need to use the delete_event action;
You must shift or delete an appoint only if this appoint belongs to the user. You must check the user_id attribute in the event description data.
You must use the closest time to make an appointment for a patient only if it is ahead the current time for 2h. For example if the current time is 2:30pm and the 
patient asks for an appoint you should suggest him the 4:30 pm as the closest time.

-------------------------------------------
Example session 1:
Question: Hi I want to make an appointment. I need the dentist help. What is the closest time in your clinic?
Thought: I should look up the current date and time firstly afterwards I can query the list of the occupated events and try to find a free 1.5h time slot from 9am till 6pm excluding lunch time from 1 pm till 2 pm.
Action: get_current_datetime: None
PAUSE

You will be called again with something like this:
Observation: 2025-01-06T08:30:20.123456+03:00

Then you loop again:
Thought: To suggest the available time slot I need to get the list of already existed appointments from the calendar.
Action: list_events: 255
PAUSE

You will be called again with something like this:
Observation: [{'kind': 'calendar#event', 'etag': '"3472128744014000"', 'id': 'ltbnnd56mqo0lpht3hlkqm62ho', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bHRibm5kNTZtcW8wbHBodDNobGtxbTYyaG8gYWxla3NhbmRyLmdhcmlrb3YyQG0', 'created': '2025-01-05T08:06:12.000Z', 'updated': '2025-01-05T08:06:12.007Z', 'summary': 'Aleksandr Terentev appointment', 'description': 'a dentist appointment for Aleksandr Terentev (user_id: 1313470365)', 'location': 'Offline', 'creator': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'organizer': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'start': {'dateTime': '2025-01-06T09:00:00+03:00', 'timeZone': 'Europe/Minsk'}, 'end': {'dateTime': '2025-01-06T10:30:00+03:00', 'timeZone': 'Europe/Minsk'}, 'iCalUID': 'ltbnnd56mqo0lpht3hlkqm62ho@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}, {'kind': 'calendar#event', 'etag': '"3472128744402000"', 'id': 'amn52ssrs8vamhk01a8sohn0ks', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=YW1uNTJzc3JzOHZhbWhrMDFhOHNvaG4wa3MgYWxla3NhbmRyLmdhcmlrb3YyQG0', 'created': '2025-01-05T08:06:12.000Z', 'updated': '2025-01-05T08:06:12.201Z', 'summary': 'Mark Twain appointment', 'description': 'a dentist appointment for Mark Twain (user_id: 6583470365)', 'location': 'Offline', 'creator': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'organizer': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'start': {'dateTime': '2025-01-06T10:30:00+03:00', 'timeZone': 'Europe/Minsk'}, 'end': {'dateTime': '2025-01-06T12:00:00+03:00', 'timeZone': 'Europe/Minsk'}, 'iCalUID': 'amn52ssrs8vamhk01a8sohn0ks@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}]

You then output:
Answer: <Suggest 3 closest available timeslots based on the current date and time and the list of the already existed appointments and the workhours schedule>

-------------------------------------------
Example session 2:
Question: (user name: "Aleksandr Terentev" user_id: 1313470365) Can you please make for me an appointment at 4:30 PM on the 6th of January??
Thought: I need to create a new appointment for Aleksandr Terentev at 4:30 PM on January 6th, 2025.  I need to check if that time slot is available based on the existing appointments.
Action: list_events: 255
PAUSE

You will be called again with something like this:
Observation: [{'kind': 'calendar#event', 'etag': '"3472128744014000"', 'id': 'ltbnnd56mqo0lpht3hlkqm62ho', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bHRibm5kNTZtcW8wbHBodDNobGtxbTYyaG8gYWxla3NhbmRyLmdhcmlrb3YyQG0', 'created': '2025-01-05T08:06:12.000Z', 'updated': '2025-01-05T08:06:12.007Z', 'summary': 'Aleksandr Terentev appointment', 'description': 'a dentist appointment for Aleksandr Terentev (user_id: 1313470365)', 'location': 'Offline', 'creator': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'organizer': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'start': {'dateTime': '2025-01-06T09:00:00+03:00', 'timeZone': 'Europe/Minsk'}, 'end': {'dateTime': '2025-01-06T10:30:00+03:00', 'timeZone': 'Europe/Minsk'}, 'iCalUID': 'ltbnnd56mqo0lpht3hlkqm62ho@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}, {'kind': 'calendar#event', 'etag': '"3472128744402000"', 'id': 'amn52ssrs8vamhk01a8sohn0ks', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=YW1uNTJzc3JzOHZhbWhrMDFhOHNvaG4wa3MgYWxla3NhbmRyLmdhcmlrb3YyQG0', 'created': '2025-01-05T08:06:12.000Z', 'updated': '2025-01-05T08:06:12.201Z', 'summary': 'Mark Twain appointment', 'description': 'a dentist appointment for Mark Twain (user_id: 6583470365)', 'location': 'Offline', 'creator': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'organizer': {'email': 'aleksandr.garikov2@gmail.com', 'self': True}, 'start': {'dateTime': '2025-01-06T10:30:00+03:00', 'timeZone': 'Europe/Minsk'}, 'end': {'dateTime': '2025-01-06T12:00:00+03:00', 'timeZone': 'Europe/Minsk'}, 'iCalUID': 'amn52ssrs8vamhk01a8sohn0ks@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default'}]

Then you loop again:
Thought: Okay, Aleksandr Terentev, I have checked the 1.5h timeslot from 4:30 PM on January 6th, 2025 is available. I need to make an appointment for you.
Action: create_event: 'Aleksandr Terentev appointment', 'a dentist appointment for Aleksandr Terentev (user_id: 1313470365)', '2025-01-06T16:30:00+03:00','Europe/Minsk', 
                                           '2025-01-06T18:00:00+03:00','Europe/Minsk',[])
PAUSE

You will be called again with something like this:
Observation: created event id: j3kt9aegmo4sj2u5il6ctnho7g, result: Event created: https://www.google.com/calendar/event?eid=ajNrdDlhZWdtbzRzajJ1NWlsNmN0bmhvN2cgYWxla3NhbmRyLmdhcmlrb3YyQG0

You then output:
Answer: <Inform the user that event is successfully created>
-------------------------------------------
Start working with an user request from the following line:
"""

    # Dummy functions to simulate API calls
    def getLocation(self,place=None):
        location = {
            "city": "New York City",
            "state": "NY",
            "country": "USA"
        }
        return location

    def getCurrentWeather(self,place=None):
        weather = {
            "temperature": "2",
            "unit": "F",
            "forecast": "snowy"
        }
        return weather

    def get_current_datetime(self, fake_param):
        # Get the current date and time with the local timezone
        now = datetime.now(timezone.utc)  # or replace timezone.utc with your desired timezone
        iso_8601_string = now.isoformat() # 2025-01-04T14:53:20.123456+00:00
        return iso_8601_string
        
    