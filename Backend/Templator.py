import pandas as pd
import random
from jinja2 import Template
from pandas_ods_reader import read_ods
import os
from dotenv import load_dotenv

load_dotenv()

templates = (read_ods("../Templates.ods", 1))  # Templates.ods stores the templates
df = pd.read_csv(os.environ['playlist_info_save'])

'''Basic class to store playlist properties'''


class txttemplate:

    def __init__(self, authname, playname, playurl, songname, songurl, email):
        self.authname = authname
        self.playname = playname
        self.playurl = playurl
        self.songname = songname
        self.songurl = songurl
        self.email = email


'''Processes dataframe for templating information
Accepts: songname - your song name to promote
songurl - url of the promoted song
Returns: List of relevant information to template'''


def process_dataframe(playlist_csv,songname, songurl):
    info = []
    for index, row in playlist_csv.iterrows():
        authname = df.at[index, "Author Name"]
        playname = df.at[index, "Playlist Name"]
        playurl = df.at[index, "url"]
        email = df.at[index, "email"]

        if type(email) != str:  # Check to ensure that the email is valid
            email = None
        info.append(txttemplate(authname, playname, playurl, songname, songurl, email))
    return info


'''Function to populate email templates with relevant information
Accepts: list of relevant information
Returns: List of templates'''


def populate_templateemail(info):
    templatelist = []
    for item in info:
        if item.email != None:
            rndint = random.randint(0, len(templates) - 1)  # Pick a random template
            tojinja = templates.loc[rndint, "Templates"]
            templatejinja = (Template(tojinja))  # Reads random row of Templates Column
            templatelist.append(
                templatejinja.render(authname=item.authname, playname=item.playname, songname=item.songname,
                                     songurl=item.songurl, playurl=item.playurl))
        else:
            templatelist.append(" ")

    return templatelist

def create_templated_playlist_csv():
    df = pd.read_csv(os.environ['playlist_info_save'],index_col=0)

    info = process_dataframe(df,os.environ['your_song_name'],
                             os.environ['your_song_url'])
    populated_templates = populate_templateemail(info)

    df["templatesEmail"] = pd.DataFrame(populated_templates)

    df.to_csv(os.environ['playlist_contact_info'], mode='w', index=True)


