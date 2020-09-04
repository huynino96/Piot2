from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

'''
This class is for interacting with the Google Calendar API to create or remove and event
'''


class Calendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, secretFile):
        self.__credentials = None
        self.__client_secret = secretFile
        self.__service = None
        self.__initiated = False

    def init(self):
        if not self.__credentials:
            flow = InstalledAppFlow.from_client_secrets_file(self.__client_secret, scopes=Calendar.SCOPES)
            self.__credentials = flow.run_console()
            self.__service = build('calendar', 'v3', credentials=self.__credentials)
            self.__initiated = True     # Set to true to prevent from creating extra prompt

    # For this method, we check if the credentials has been obtained to prevent from prompting users to authorise our
    # app again and again
    def ifInitiated(self):
        return self.__initiated

    def addEvent(self, summary, description, time, remind=False):
        # Construct event object
        event = {
            "summary": summary,
            "description": description,
            "start": {
                'dateTime': time.isoformat(),   # Switch to iso format to comply with Google API requirements
                'timeZone': 'GMT+7:00'  # Use the Vietnam time zone for accurate timing
            },
            "end": {
                'dateTime': time.isoformat(),
                'timeZone': 'GMT+7:00'
            },
            "sendNotifications": remind # Set whether users will receive an notification about the event or not
        }

        # Use service to add
        event = self.__service.events().insert(calendarId="primary", body=event).execute()
        return event

    # Remove the event using a unique event string we obtain from creating the event
    def removeEvent(self, event_id):
        self.__service.events().delete(calendarId="primary", eventId=event_id).execute()