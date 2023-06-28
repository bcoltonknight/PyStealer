def get_wifi():
    import subprocess
    import re
    data = []
    KEY_PATTERN = r'Key Content\W*(.*)'
    PROFILE_PATTERN = r'\W*All User Profile\W*(.*)'
    # Get list of networks from netsh
    profileList = subprocess.Popen('netsh wlan show profile', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    profileList = re.findall(PROFILE_PATTERN, profileList)
    # Format all profiles
    print('WLAN Password:\n-----------------------------')
    for index, profile in enumerate(profileList):
        profileList[index] = profile.rstrip()

    # Print and get all profiles
    for profile in profileList:
        profileOutput = subprocess.Popen(f'netsh wlan show profile name="{profile}" key=clear', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        key = re.findall(KEY_PATTERN, profileOutput)
        if key != []:
            print(f'Network: {profile}\nPassword: {key[0]}\n')
            data.append({"network": profile, "password": key[0].strip()})

    return data