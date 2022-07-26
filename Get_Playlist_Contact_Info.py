from Backend import PlaylistClass
from dotenv import load_dotenv
import os
load_dotenv()

# Define keywords for playlist search.
keywords = os.environ['keywords']

#Generate csv with relevant playlists and contact information
PlaylistClass.get_playlists_with_contact(keywords)