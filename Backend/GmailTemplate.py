from simplegmail import Gmail
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

'''Module to send emails based on templates and playlist information
Use with caution, it will send the emails to everyone'''

def send_emails():
    #Need to create app auth for this to work
    gmail = Gmail() # will open a browser window to ask you to log in and authenticate
    df = pd.read_csv(os.environ['playlist_contact_info'], usecols= ['url','Author Name', "Playlist Name","email","templatesEmail"], skipinitialspace=True)

    #Iterate over index items, and send emails
    for idx,row in df.iterrows():
        try:
            msgn = df.at[idx, "templatesEmail"]
            msgn = msgn.replace("\n\n" , "<br /><br />") #Formatting
            params = {
                "to": df.at[idx, "email"],
                "sender": os.environ['your_gmail'],
                "subject": os.environ['email_subject'],
                "msg_html": msgn,
                "msg_plain": None,
                "signature": True  # use my account signature
            }
            message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)
            print('message sent!')

        except:
            print('cant send message')
            continue