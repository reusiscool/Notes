# Web project "Notes"

## 1. Project tasks

Create web and bot app where you can create, store and see notes.

The web part will allow you the following
- Create multiple accounts
- Create notes
- Edit notes
- Delete notes

With bot part you can do the following:
- Create account
- Log into web accounts
- Create notifications
- Get notifications

## 2. Set up and run

App is built on python 3.10
To prepare for launch create venv and install requirements:

```
pip install -r requirements.txt
```

To run the full app you need to run database(rest api), website and bot.
To run the database use:
```
python3 main_api.py
```
To run the website use:
```
python3 main_site.py
```
To run the bot use:
```
python3 main_bot.py
```
Note that bot and website will not run without database, but bot can run without website and vica versa
