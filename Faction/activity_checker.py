import requests
import time

KEY = "REPLACE WITH YOUR OWN KEY!!"  # Only requires a Public Key
url = "https://api.torn.com/v2/faction/members?striptags=true"
headers = {"accept": "application/json", "Authorization": f"ApiKey {KEY}"}

RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
DIM = "\033[2m"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    members = response.json()
    max_name_length = max(len(member["name"]) for member in members["members"])

    for member in members["members"]:
        last_action = round(time.time()) - member["last_action"]["timestamp"]
        days, hours, minutes = (
            last_action // 86400,
            (last_action % 86400) // 3600,
            (last_action % 3600) // 60,
        )
        reminder_to_check = days > 0

        if member["last_action"]["status"] == "Offline":
            color = RED if reminder_to_check else DIM
            activity = (
                f"{color}{member['name'].ljust(max_name_length)}   "
                f"{days:<2} Day{'s' if days != 1 else ' '} | "
                f"{hours:<2} Hour{'s' if hours != 1 else ' '} | "
                f"{minutes:<2} Minute{'s' if minutes != 1 else ' '} "
                f"{'⚠️' if reminder_to_check else ''}{RESET}"
            )
        else:
            idle = member["last_action"]["status"] == "Idle"
            color = YELLOW if idle else GREEN
            activity = (
                f"{color}{member['name'].ljust(max_name_length)}   ONLINE "
                f"{'(Idle)' if idle else ''}{RESET}"
            )

        print(activity)
else:
    print(f"Error {response.status_code}: {response.text}")
