from bubbly_pom import bubbly_pom_globals as bpg
import json
import os
import shutil


class UserData:
    def __init__(self):
        if not os.path.exists(bpg.user_app_folder_path):
            os.makedirs(bpg.user_app_folder_path)
            os.makedirs(bpg.notes_folder_path)

            shutil.copy2(
                os.path.join("bubbly_pom", "defaults", bpg.timer_settings_file),
                bpg.user_app_folder_path
            )

            if not os.path.exists(os.path.join(bpg.user_app_folder_path, bpg.notes_list_file)):
                with open(os.path.join(bpg.user_app_folder_path, bpg.notes_list_file), "w") as f:
                    f.write(json.dumps([]))

    def fetch_timer_settings(self):
        with open(os.path.join(bpg.user_app_folder_path, bpg.timer_settings_file)) as f:
            return json.loads(f.read())

    def save_timer_settings(self, timer_settings):
        print("Saving Timer Data")
        with open(os.path.join(bpg.user_app_folder_path, bpg.timer_settings_file), "r+") as f:
            f.seek(0)
            f.write(json.dumps(timer_settings))
            f.truncate()