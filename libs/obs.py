import os
import json


def obs_key_extractor():
    data = []
    obs_profiles_path = os.path.join(os.getenv('APPDATA'), 'obs-studio/basic/profiles')
    for i in os.listdir(obs_profiles_path):
        with open(os.path.join(obs_profiles_path, i + "/service.json"), 'r') as f:
            jsonData = json.loads(f.read())
        streamSettings = jsonData['settings']
        print(f"Streaming Platform: {streamSettings['service']}\nKey: {streamSettings['key']}")
        data.append({'platform': streamSettings['service'], 'key': streamSettings['key']})
    return data


if __name__ == '__main__':
    obs_key_extractor()