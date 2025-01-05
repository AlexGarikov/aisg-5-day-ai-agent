from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pydantic.v1.generics import get_caller_frame_info
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleCalendarService:

    def __init__(self, credentials_file_path = '.google_api_credentials.json'):
        # Path to your credentials JSON file
        self.CREDENTIALS_FILE = credentials_file_path
        # Scopes define the level of access requested
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.service = self.prepare_service()

    def prepare_service(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)
        return service

    def list_events(self, event_count=255):
        # Get the next 10 events on the user's primary calendar
        events_result = self.service.events().list(
            calendarId='primary',
            maxResults=int(event_count),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return 'No upcoming events found.'

        #result = ''
        #for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    result = result + f"Event: {event['summary']} at {start}; "

        #return result
        return events

    def create_event(self, summary, description, start, start_time_zone, end, end_time_zone, attendees):
        event = {
            'summary': summary,
            'location': 'Offline',
            'description': description,
            'start': {
                'dateTime': start,  # Use ISO 8601 format
                'timeZone': start_time_zone,
            },
            'end': {
                'dateTime': end,
                'timeZone': end_time_zone,
            },
            'attendees': attendees,
        }

        """
        event = {
        'summary': 'Sample Event',
        'location': 'Online',
        'description': 'This is a sample event.',
        'start': {
            'dateTime': '2025-01-06T09:00:00-07:00',  # Use ISO 8601 format
            'timeZone': 'America/Los_Angeles',
            'timeZone': 'Europe/Minsk'
        },
        'end': {
            'dateTime': '2025-01-06T10:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': 'example1@gmail.com'},
            {'email': 'example2@gmail.com'},
        ],
    }
        """

        event_result = self.service.events().insert(calendarId='primary', body=event).execute()

        #print(event_result)

        return event_result.get('id'), f"Event created: {event_result.get('htmlLink')}"

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        return f"Event with ID {event_id} has been deleted successfully."

    def shift_event(self, event_id, new_start_time, new_end_time):
        # Retrieve the event
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()

        # Update event times
        event['start']['dateTime'] = new_start_time
        event['end']['dateTime'] = new_end_time

        #print(event)

        # Send the updated event back to Google Calendar
        updated_event = self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return f"Event updated: {updated_event.get('htmlLink')}"




