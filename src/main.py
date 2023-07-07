from aiohttp import ClientSession, BasicAuth
from asyncio import run
from random import choice
from loguru import logger
from json import load
import aiofiles

class steam():
    def __init__(self, ip=None, login=None, password=None, 
                 username=None, alphabet=None, lenght=None):
        self.ip = f'https://{ip}'
        self.login, self.password = login, password
        self.username = username
        self.alphabet = alphabet
        self.lenght = lenght

    async def checkUsername(self):
        async with ClientSession() as session:
            if self.ip != "None":
                if self.login != "None":
                    proxy_auth = BasicAuth(self.login, self.password)
                    async with session.get(f'https://steamcommunity.com/id/{self.username}/', proxy=f"http://{self.ip}/", proxy_auth = proxy_auth, verify_ssl=False) as response:
                        text = await response.text()
                else:
                    async with session.get(f'https://steamcommunity.com/id/{self.username}/', proxy=f"http://{self.ip}/", verify_ssl=False) as response:
                        text = await response.text()
            else:
                async with session.get(f'https://steamcommunity.com/id/{self.username}/', verify_ssl=False) as response:
                    text = await response.text()
        if 'Error' in text:
            async with aiofiles.open('data/nicks.txt', 'r+') as f:
                await f.read()
                await f.write(f'{self.username}\n')
            logger.info(f'{self.username} available')
        else:
            logger.error(f'{self.username} unavailable')

    def getAlphabet(self, alphabet):
        if alphabet.lower() in ('n', 'no'):
            alphabet = 'qwertyuioplkjhgfdsazxcvbnm'
        self.alphabet = list(alphabet)

    async def getRandomUsername(self, lenght):
        abc = ""
        for _ in range(int(lenght)):
            abc += choice(self.alphabet)
        self.username = abc    

    def getProxy(self):
        with open('data/config.json', 'r') as f:
            data = load(f)
        self.ip, self.password, self.login = data['ip'], data['password'], data['login'] 

    async def start(self):
        steam.getProxy()
        alphabet = input('Enter alphabet for gen nicks, or write n to use default: ')
        steam.getAlphabet(alphabet=alphabet)
        cycles = input('1 - range ( enter number of loops)\n2 - while true( enter "N")\nEnter a type of cycle: ')
        lenght = int(input('Enter a len of username: '))
        if str(cycles.lower()) in ('n', 'no'):
            while True:
                await steam.getRandomUsername(lenght)
                await steam.checkUsername()
        else:
            for _ in range(int(cycles)):
                await steam.getRandomUsername(lenght)
                await steam.checkUsername()  
                
steam = steam(None, None, None, 
              None, None, None)
run(steam.start())