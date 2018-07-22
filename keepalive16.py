__author__ = 'arpit(supersaeyan)'

import requests
import time
import argparse
import re
from multiprocessing import Process
from random import randrange

ttlarg = 600

userarg = ""


def rollgen():
    global userarg
    userarg = randrange(1444069, 1444384)
    return userarg


passwarg = "student"

servers = {
    'vm1': 'socks5://10.10.1.1:3001', 'vm2': 'socks5://10.10.1.1:3002',
    'vm3': 'socks5://10.10.1.1:3003', 'vm4': 'socks5://10.10.1.1:3004',
    'vm5': 'socks5://10.10.1.1:3005', 'vm6': 'socks5://10.10.1.1:3006',
    'vm7': 'socks5://10.10.1.1:3007', 'vm8': 'socks5://10.10.1.1:3008',
    'vm9': 'socks5://10.10.1.1:3009', 'vm10': 'socks5://10.10.1.1:3010',
    'vm11': 'socks5://10.10.1.1:3011', 'vm12': 'socks5://10.10.1.1:3012',
    'vm13': 'socks5://10.10.1.1:3013', 'vm14': 'socks5://10.10.1.1:3014',
    'vm15': 'socks5://10.10.1.1:3015', 'vm16': 'socks5://10.10.1.1:3016',
    'vm17': 'socks5://10.10.1.1:3017', 'vm18': 'socks5://10.10.1.1:3018',
    'vm19': 'socks5://10.10.1.1:3019', 'vm20': 'socks5://10.10.1.1:3020',
    'vm21': 'socks5://10.10.1.1:3021', 'vm22': 'socks5://10.10.1.1:3022',
    'vm23': 'socks5://10.10.1.1:3023', 'vm24': 'socks5://10.10.1.1:3024',
    'vm25': 'socks5://10.10.1.1:3025', 'vm26': 'socks5://10.10.1.1:3026',
    'vm27': 'socks5://10.10.1.1:3027', 'vm28': 'socks5://10.10.1.1:3028',
    'vm29': 'socks5://10.10.1.1:3029', 'vm30': 'socks5://10.10.1.1:3030',
    'vm31': 'socks5://10.10.1.1:3031', 'vm32': 'socks5://10.10.1.1:3032',
}

active_vm = servers['vm1']


def getlen(params):
    return len(str(params).replace(': ', ':').replace(', ', (',')))


def trigger(url):
    headers = {

        'Host': 'go.microsoft.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    # print("TRIGGER ACTIVE VM: " + active_vm)
    r = requests.get(url, headers=headers, proxies=dict(http=active_vm), verify=False)

    redirUrl = str(r.history[0].headers['Location'])
    # print("DEBUG: TRIGGER:")

    print("VM-" + active_vm + "  " + "DEBUG: HISTORY[0]: " + str(r.history[0].status_code))

    status = r.history[0].status_code

    # print("DEBUG: REDIRECT URL: " + redirUrl)

    print("VM-" + active_vm + "  " + "DEBUG: FINAL: " + str(r.status_code) + " " + str(r.reason))

    return redirUrl, status


def getauth(redirection):
    headers = {
        'Host': '192.168.1.1:1000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    # print("GETAUTH ACTIVE VM: " + active_vm)
    r = requests.get(redirection, headers=headers, proxies=dict(http=active_vm), verify=False)
    print("VM-" + active_vm + "  " + "DEBUG: GETAUTHPAGE:" + str(r.status_code) + " " + str(r.reason))


def auth(url, token, user, passw):
    params = {
        '4Tredir': url,
        'magic': token,
        'username': user,
        'password': passw,
    }

    referer = "http://192.168.1.1:1000/fgtauth?" + token

    headers = {
        'Host': '192.168.1.1:1000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Referer': referer,
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': getlen(params),
    }

    # print("AUTH ACTIVE VM: " + active_vm)
    r = requests.post("http://192.168.1.1:1000/", headers=headers, data=params, proxies=dict(http=active_vm),
                      verify=False)

    source = str(r.content)
    # print("DEBUG: SOURCE =>" + source)
    failure = False
    matches = re.findall('Authentication Failed', source)

    if len(matches) > 0:
        failure = True

    index = source.find("http://192.168.1.1:1000/logout?")
    logouturl = source[index:(index + 47)]
    # print("DEBUG: LOGOUT: " + str(logouturl))

    print("VM-" + active_vm + "  " + "DEBUG: AUTH:" + str(user) + " : " + str(passw))

    # print("DEBUG: " + str(r.headers))

    print("VM-" + active_vm + "  " + "DEBUG: FINAL: " + str(r.status_code) + " " + str(r.reason))

    return failure, logouturl


def keepalive(url):
    headers = {
        'Host': '192.168.1.1:1000',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q = 0.5',
        'Accept-Encoding': 'gzip,deflate',
        'DNT': '1',
        'Referer': 'http://192.168.1.1:1000/',
        'Connection': 'keep-alive',
    }
    print("VM-" + active_vm + "  " + "DEBUG: KEEPALIVE")

    print("VM-" + active_vm + "  " + "AUTHENTICATED")

    # print("DEBUG: KEEPALIVE URL: " + str(url))

    # print("VM: " + active_vm + "KEEPALIVE")
    r = requests.get(url, headers=headers, proxies=dict(http=active_vm), verify=False)
    print("VM-" + active_vm + "  " + "DEBUG: KEEPALIVE " + str(r.status_code) + " " + str(r.reason))


def logout(logouturl):
    keepaliveurl = logouturl.replace('logout', 'keepalive')

    headers = {
        'Host': '192.168.1.1:1000',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q = 0.5',
        'Accept-Encoding': 'gzip,deflate',
        'DNT': '1',
        'Referer': keepaliveurl,
        'Connection': 'keep-alive',
    }

    # print("VM: " + active_vm + "LOGOUT")
    r = requests.get(logouturl, headers=headers, proxies=dict(http=active_vm), verify=False)
    # print("LOGGED OUT SUCCESSFULLY")

    print("VM-" + active_vm + "  " + "DEBUG: LOGOUT: " + str(r.status_code), str(r.reason))


def runtime(ttl, keepaliveurl):
    i = int(ttl)
    # print("DEBUG: initial TTL: " + str(i))

    while i > 0:
        print("VM-" + active_vm + "  " + "DEBUG: TTL " + str(i))

        time.sleep(1)
        i -= 1
        if i is 0:
            keepalive(keepaliveurl)

    runtime(ttl, keepaliveurl)


def login(ttl, vmno, username, password='student'):
    try:

        trigUrl = "http://go.microsoft.com/fwlink/?LinkID=219472&clcid=0x409"
        logouturl = "http://192.168.1.1:1000/logout?0f02040d040e0c09"

        vmkey = "vm" + str(vmno)
        global active_vm
        active_vm = servers[vmkey]

        redirUrl, status = trigger(trigUrl)
        redirToken = redirUrl[32:]

        if status == 302:
            print("VM-" + active_vm + "  " + "HISTORY IS 302 SO LOGGED OUT TO RELOGIN")
            logout(logouturl)
            login(ttl, vmno, userarg, password)

        getauth(redirUrl)

        auth_status, authlogout = auth(trigUrl, redirToken, username, password)

        if auth_status == True:
            print("VM-" + active_vm + "  " + "FAILED TO LOGIN SO LOGGED OUT TO RELOGIN")
            logout(logouturl)
            login(ttl, vmno, rollgen(), password)

        # print("DEBUG: LOGOUT: " + str(authlogout))
        token = authlogout[35:]
        print("VM-" + active_vm + "  " + "DEBUG: TOKEN: " + str(token))
        keepaliveurl = authlogout.replace('logout', 'keepalive')
        # print("DEBUG: KEEPALIVE: " + str(keepaliveurl))

        # Keepalive timer
        runtime(ttl, keepaliveurl)

    except KeyboardInterrupt:
        print("YOU PRESSED CTRL + C, PROGRAM WILL NOW LOGOUT AND EXIT")
        logout(logouturl)

    except:
        print(active_vm, "UNEXPECTED ERROR OCCURED SO LOGGED OUT TO RELOGIN")
        logout(logouturl)
        login(ttlarg, vmno, rollgen(), passwarg)


if __name__ == '__main__':
    """
    threadlist = list()
    threadcount = 16

    for i in xrange(16):
        threadlist.append(Process(target=login, args=(ttlarg, i, rollgen(), ...))
    """
    th1 = Process(target=login, args=(ttlarg, 1, rollgen(), passwarg,))
    th2 = Process(target=login, args=(ttlarg, 2, rollgen(), passwarg,))
    th3 = Process(target=login, args=(ttlarg, 3, rollgen(), passwarg,))
    th4 = Process(target=login, args=(ttlarg, 4, rollgen(), passwarg,))
    th5 = Process(target=login, args=(ttlarg, 5, rollgen(), passwarg,))
    th6 = Process(target=login, args=(ttlarg, 6, rollgen(), passwarg,))
    th7 = Process(target=login, args=(ttlarg, 7, rollgen(), passwarg,))
    th8 = Process(target=login, args=(ttlarg, 8, rollgen(), passwarg,))
    th9 = Process(target=login, args=(ttlarg, 9, rollgen(), passwarg,))
    th10 = Process(target=login, args=(ttlarg, 10, rollgen(), passwarg,))
    th11 = Process(target=login, args=(ttlarg, 11, rollgen(), passwarg,))
    th12 = Process(target=login, args=(ttlarg, 12, rollgen(), passwarg,))
    th13 = Process(target=login, args=(ttlarg, 13, rollgen(), passwarg,))
    th14 = Process(target=login, args=(ttlarg, 14, rollgen(), passwarg,))
    th15 = Process(target=login, args=(ttlarg, 15, rollgen(), passwarg,))
    th16 = Process(target=login, args=(ttlarg, 16, rollgen(), passwarg,))
    # th17 = Process(target= login, args=(ttlarg, 17, rollgen(), passwarg,))
    # th18 = Process(target= login, args=(ttlarg, 18, rollgen(), passwarg,))
    # th19 = Process(target= login, args=(ttlarg, 19, rollgen(), passwarg,))
    # th20 = Process(target= login, args=(ttlarg, 20, rollgen(), passwarg,))
    # th21 = Process(target= login, args=(ttlarg, 21, rollgen(), passwarg,))
    # th22 = Process(target= login, args=(ttlarg, 22, rollgen(), passwarg,))
    # th23 = Process(target= login, args=(ttlarg, 23, rollgen(), passwarg,))
    # th24 = Process(target= login, args=(ttlarg, 24, rollgen(), passwarg,))
    # th25 = Process(target= login, args=(ttlarg, 25, rollgen(), passwarg,))
    # th26 = Process(target= login, args=(ttlarg, 26, rollgen(), passwarg,))
    # th27 = Process(target= login, args=(ttlarg, 27, rollgen(), passwarg,))
    # th28 = Process(target= login, args=(ttlarg, 28, rollgen(), passwarg,))
    # th29 = Process(target= login, args=(ttlarg, 29, rollgen(), passwarg,))
    # th30 = Process(target= login, args=(ttlarg, 30, rollgen(), passwarg,))
    # th31 = Process(target= login, args=(ttlarg, 31, rollgen(), passwarg,))
    # th32 = Process(target= login, args=(ttlarg, 32, rollgen(), passwarg,))

    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()
    th7.start()
    th8.start()
    th9.start()
    th10.start()
    th11.start()
    th12.start()
    th13.start()
    th14.start()
    th15.start()
    th16.start()
    # th17.start()
    # th18.start()
    # th19.start()
    # th20.start()
    # th21.start()
    # th22.start()
    # th23.start()
    # th24.start()
    # th25.start()
    # th26.start()
    # th27.start()
    # th28.start()
    # th29.start()
    # th30.start()
    # th31.start()
    # th32.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()
    th5.join()
    th6.join()
    th7.join()
    th8.join()
    th9.join()
    th10.join()
    th11.join()
    th12.join()
    th13.join()
    th14.join()
    th15.join()
    th16.join()
# th17.join()
# th18.join()
# th19.join()
# th20.join()
# th21.join()
# th22.join()
# th23.join()
# th24.join()
# th25.join()
# th26.join()
# th27.join()
# th28.join()
# th29.join()
# th30.join()
# th31.join()
# th32.join()
