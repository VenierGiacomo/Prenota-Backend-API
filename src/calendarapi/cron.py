import requests
import json

print('task ')
header = {"Content-Type": "application/json; charset=utf-8",}
ids=['a416d507-a073-4ec5-983b-cd6dff542160','1f80985d-fa71-4010-a925-3861907a6b64']
title = "Test 🙂"
cont = "Automatic message every minute"
payload = {"app_id": os.environment.get('ONESIGNAL_APP_ID'),
        "include_player_ids":ids ,
        "headings": {"en": title},
        "contents": {"en":cont }}
requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))