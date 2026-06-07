import datetime
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'

def get_credentials():
    """Gets valid user credentials from storage or dynamic auth."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_unread_emails(max_results: int = 5, **kwargs) -> str:
    """
    Fetch and summarize the latest unread emails from Gmail.
    """
    creds = get_credentials()
    if not creds:
        return "Boss, I need the 'credentials.json' file in the root directory to access your Gmail. Please add it via the Command Center."

    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            return "You're all caught up, boss. No unread emails in the inbox."

        summary = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = m['payload']
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = m.get('snippet', '')
            summary.append(f"- From: {sender}\n  Subject: {subject}\n  Snippet: {snippet}")

        return "Here are your latest unread emails, boss:\n\n" + "\n\n".join(summary)

    except HttpError as error:
        return f"An error occurred while fetching emails: {error}"

def get_classroom_assignments(**kwargs) -> str:
    """
    Fetch recent assignments and coursework from Google Classroom.
    """
    creds = get_credentials()
    if not creds:
        return "Boss, I need credentials to access Google Classroom. Please initialize the 'Link Google Workspace' protocol."

    try:
        service = build('classroom', 'v1', credentials=creds)
        
        # List courses
        courses_result = service.courses().list(pageSize=10).execute()
        courses = courses_result.get('courses', [])

        if not courses:
            return "I couldn't find any active courses in your Classroom, boss."

        summary = []
        for course in courses:
            course_id = course['id']
            course_name = course['name']
            
            # List coursework (assignments)
            work_result = service.courses().courseWork().list(courseId=course_id, pageSize=3).execute()
            works = work_result.get('courseWork', [])
            
            if not works:
                continue

            summary.append(f"📚 {course_name}:")
            for work in works:
                title = work.get('title')
                due_date = work.get('dueDate', 'No due date')
                summary.append(f"  - {title} (Due: {due_date})")

        if not summary:
            return "Everything is quiet in the Classroom. No pending assignments found."
            
        return "Here is your Classroom briefing, boss:\n\n" + "\n".join(summary)

    except HttpError as error:
        return f"Status update: Encountered an error with the Classroom API: {error}"

def get_calendar_events(max_events: int = 5, **kwargs) -> str:
    """
    Fetch upcoming events from Google Calendar.
    """
    creds = get_credentials()
    if not creds:
        return "Boss, I need credentials for Google Calendar. Please initiate the link protocol."

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_events, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return "Your schedule is clear, boss. No upcoming events found."

        summary = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary.append(f"- {event['summary']} ({start})")

        return "Here is your upcoming schedule, boss:\n\n" + "\n".join(summary)

    except HttpError as error:
        return f"Calendar sync failure: {error}"

def register(mcp):
    mcp.tool()(get_unread_emails)
    mcp.tool()(get_classroom_assignments)
    mcp.tool()(get_calendar_events)
