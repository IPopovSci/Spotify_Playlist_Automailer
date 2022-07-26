# Spotify Playlist Parser & Automailer

Project designed to extract contact information from relevant Spotify playlists, and send templated messages to playlist owners via gmail API.

## Table of contents

* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Setup](#setup)
* [Features](#features)
* [Author](#Author)

### Introduction

This is a project designed to automate sending your songs to playlist owners on Spotify.
Caution should be used, since over-emailing will get your Gmail API access revoked.

### Technologies and libraries

* Anaconda 3
* Python 3.7
* Spotipy
* re
* Pandas
* OS
* Dotenv
* Jinja2
* simplegmail

### Setup

To set up, clone the repository.
This project has 2 entry points: Obtaining playlists w/ contact information and an Automailer.

First, set up your enviromental variables (.env):

keywords = What keywords Spotify uses to search for playlists
client_id = Your Spotify API client ID
client_secret = Your Spotify secret ID

playlist_info_save = Name of csv to save found playlists (Include .csv at the end)
playlist_contact_info = Name of csv to save found playlists with contact information 

your_song_name = Name of the song you are promoting
your_song_url = Spotify URL of the song you are promoting
your_gmail = Your gmail address
email_subject = Subject of the email

To obtain playlists with contact information, run Get_Playlist_Contact_Info.py

Notice, that one contact can own multiple playlists, and those duplicates aren't filtered

Make sure to go through the resultant csv and select which playlist fits you the most, delete the rest

To send emails, set up your templates in Templates.odf (A few been already provided)

Then follow the steps here to obtain Google Oauth: https://pypi.org/project/simplegmail/

Then run Automailer.py

Double check your csvs, and exercise caution as its very easy to spam someone and get your gmail priviligies revoked

### Features

* Spotify API search for playlists with relevant keywords
* Search for contact information (Email and IG) in found playlists
* Automatic templating for emails
* Automailer that uses email contact info to send templated messages

### Project Status
While this project can use several improvements, such as auto removal of duplicated emails and draft creation, its unlikely it will be worked upon.

### Author

Created by Ivan Popov
