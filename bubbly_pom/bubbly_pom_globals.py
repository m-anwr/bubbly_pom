import os

APP_NAME = "BubblyPom"
user_app_folder_path = os.path.join(os.path.expanduser("~"), "." + APP_NAME)
notes_folder_name = "notes"
notes_folder_path = os.path.join(user_app_folder_path, notes_folder_name)
timer_settings_file = "timer_settings.json"
notes_list_file = "notes.json"