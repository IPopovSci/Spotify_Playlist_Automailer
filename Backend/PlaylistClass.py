import re
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()


'''Playlist class
Contains findcontact method, that searches for email or instagram handles in the playlist description
to_dct method returns details of the playlist as a dictionary'''


class Playlist:

    def __init__(self, url, desc, auth_name, name):
        self.url = url
        self.desc = desc
        self.email = None
        self.ig = None
        self.auth_name = auth_name
        self.name = name

    def findcontact(self): #Find email or IG information in playlist description
        self.email = next(iter(re.findall(r'[\w\.-]+@[\w\.-]+', self.desc)), None)
        self.ig = next(iter(re.findall(r'\s[@]+\S+', self.desc)), None)

    def to_dict(self): #Converts to dictionary
        return {
            'url': self.url,
            'desc': self.desc,
            'email': self.email,
            'ig': self.ig,
            'Author Name': self.auth_name,
            'Playlist Name': self.name,
        }


'''Grabs playlists from Spotify based on keywords
There is a 50 item limit on the API, so we grab first 1000 playlists
Accepts: keywords - list of keywords
Returns: raw_playlist_info - list of relevant playlists as dict'''


def get_playlists_from_spotify(keywords):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['client_id'],
                                                               client_secret=os.environ['client_secret']))  # Auth
    raw_playlist_info = []
    for keyword in keywords:
        x = 0
        while x < 1000: #1000 is the API limit, if something breaks here check if it has been changed
            # make search call, q = keyword, type = playlist
            fit = sp.search(q=keyword, type="playlist", limit=50, offset=x)

            raw_playlist_info.extend((fit["playlists"])["items"])  # This is a list, each element is a dict
            x += 50
    return raw_playlist_info

'''Gets a list of relevant playlists, then unpacks playlist information by URL, description, playlist author and playlist name
Accepts: list of relevant keywords
Returns: List of playlist objects, with unpacked information, including contact data'''
def get_and_process_playlists(keywords):
    raw_playlists = get_playlists_from_spotify(keywords)
    playlists = []
    for p in raw_playlists:
        url = p["external_urls"]["spotify"]
        desc = p["description"]
        auth_name = p['owner']["display_name"]
        name = p["name"]
        playlist = Playlist(url, desc, auth_name, name)
        playlist.findcontact()
        playlists.append(playlist)
    return playlists

'''Deletes playlists that do not contain contact information
Accepts: list of playlist objects
Returns: list of playlist objects that contain contact information'''
def filter_out_no_contact(playlists):
    playlist_clean = []
    for n in playlists:
        if n.email or n.ig:
            playlist_clean.append(n)
    return playlist_clean

'''Saves the list of playlist objects as csv'''
def save_to_csv(playlists):
    to_print = pd.DataFrame.from_records([s.to_dict() for s in playlists])
    to_print.to_csv(os.environ['playlist_info_save'])

def get_playlists_with_contact(keywords):
    # Get playlists
    playlists = get_and_process_playlists(keywords)

    # Filter out playlists with no IG or email
    fit_playlists = filter_out_no_contact(playlists)

    # Write to CSV
    save_to_csv(fit_playlists)

