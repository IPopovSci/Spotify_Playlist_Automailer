from dotenv import load_dotenv
from Backend import GmailTemplate, Templator

load_dotenv()

#Create templated CSVs
Templator.create_templated_playlist_csv()

GmailTemplate.send_emails()