# google_calendar.py
import os
import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no credentials, initiate auth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_blog_event(title, scheduled_time):
    service = get_calendar_service()

    event = {
        'summary': f'📌 Blog Scheduled: {title}',
        'start': {'dateTime': scheduled_time.isoformat(), 'timeZone': 'Asia/Colombo'},
        'end': {'dateTime': (scheduled_time + datetime.timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Colombo'},
        'description': f'Blog "{title}" is scheduled for auto-generation via MCP server.',
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('✅ Calendar event created:', event.get('htmlLink'))
    return event.get('htmlLink')
