

flags = {
    "Discord Employee": 1,
    "Discord Partner": 2,
    "HypeSquad Events": 4,
    "Bug Hunter Level 1": 8,
    "Dismissed Nitro promotion": 32,
    "HypeSquad Online House Bravery": 64,
    "HypeSquad Online House Brilliance": 128,
    "HypeSquad Online House Balance": 256,
    "Early Supporter": 512,
    "Team User": 1024,
    "System User": 4096,
    "Bug Hunter Level 2": 16384,
    "Verified Bot": 65536,
    "Early Verified Bot Developer": 131072,
    "Moderator Programs Alumni": 262144,
    "Bot has set an interactions endpoint url": 524288,
    "User is disabled for being a spammer": 1048576,
    "User is an active developer": 4194304,
    "User has a premium discriminator": 137438953472,
    "User has used the desktop client": 274877906944,
    "User has used the web client": 549755813888,
    "User has used the mobile client": 1099511627776,
    "User has a verified email": 8796093022208,
    "User is a collaborator and has staff permissions": 1125899906842624,
    "User is a restricted collaborator and has staff permissions": 2251799813685248
}


premium = ['None', 'Nitro Classic', 'Nitro', 'Nitro Basic']


def parse_flags(flag):
    userFlags = []
    for i in flags.keys():
        if flags[i] & flag == flags[i]:
            userFlags.append(i)

    return userFlags


if __name__ == '__main__':
    print(parse_flags(32))