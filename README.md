# Chat Room Web App

## Description:
A web app to host and manage chat rooms.

## Requirements:
Python 3 and pip

## Setup:
1.  In a given directory, setup a python virtual environment with: "python -m venv venv"
	* Or "py -3 -m venv venv" or "python 3 -m venv venv" depending on your OS and if you have multiple python versions installed. The key is that python 3 is used.
1.  In this directory, cd to the venv\Scripts\ directory (on Windows) or the venv/bin directory (on Linux)
1.  Run "source activate" (on Windows) or ". activate" (on Linux)
	* The shell prompt should change to show the name of the activated environment
1.  Install Flask with: "pip install Flask"
1.  Install SQLAlchemy with: "pip install Flask-SQLAlchemy"
1.  This gives you a virutal environment to use for flask apps requiring SQLAlchemy. You can deactivate the environment by running "source deactivate" (on Windows) or "deactivate" (on Linux)

## Running:
1.  Initialize the database by setting the FLASK_APP environment variable to chat.py (e.g. "export FLASK_APP=chat.py") and running "flask initdb"
1.  Run with "flask run"
1.  Navigate to 127.0.0.1:5000 (the default ip for running flask apps) in your browser

## Specifications:
1.  When visiting the page for the first time, users should be given the chance to create an account or login
1.  Once successfully logged in, the user should be given a list of possible chat rooms to join, or a message stating that none currently exist.
	The user should also have the option to create a new chat room.
1.  Once in a chat room, the user should be shown the history of messages for that chat room, as well as be kept up to date as messages are sent to the chat room.
	The user should also have the option to post a new message to the chat room.
	The user should further be given a way to leave the chat room.
	* Users can be in only one chat room at a time.
	* You must use AJAJ and JSON to update the list of messages posted to the chat room, and to post new messages to the chat room.
	* All AJAJ chat updates should send only *new* messages to the user.  The user should not receive the full list of chat messages with every AJAJ update as this could grow quite large over time.
	* You must be sure that your application does not display "phantom" messages to the user.
		* I.e., All users in the same chat room should see the same messages in the same order and new messages should always appear at the end of the chat log, never in the middle of the chat log.
	* You should take a polling approach to ensure that new messages are always available to the user.
		Your application should have a 1 second time between polls.
1.  Once a user leaves the chat room, they should again be shown a list of potential chat rooms to join (or a message if none exist).
	* The user should also have the option to delete any chat rooms that they created.
		* Any users still in a room when it is deleted should be shown a message informing them that the room was deleted and be again presented with the list of available chat rooms (or a message if none exist).
1.  The user should always (on every page) be presented with a way to log out while they are logged in.
1.  All data should be stored in an SQLite database named "chat.db" using SQLAlchemy's ORM and the Flask-SQLAlchemy extension.

## Additional Notes:
*  Profiles (https://support.google.com/chrome/answer/2364824) are helpful for testing multiple users logging in to the chat site at the same time.
