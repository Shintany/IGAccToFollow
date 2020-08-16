import sys
from random import randint
from time import sleep
from classes.InstaBot import InstaBot
from secret import pw
from secret import id

try:
    if len(sys.argv) == 1: raise Exception('There is no account to check')
    if 'test' in sys.argv: 
        print('id : ', id, 'password : ', pw)
    else:
        workingAccount = sys.argv[1]
        instabot = InstaBot(id, pw, workingAccount)
        instabot.LogIn()
        instabot.GoToWorkingAccountPage()
        usernames = instabot.GetAccountPageFollowing()
        dictUserFollowerAmount = dict()
        for username in usernames:
            sleepTime = randint(1,5)
            sleep(sleepTime)
            dictUserFollowerAmount[username] = instabot.GetAccountFollowersAmount(username)
        
except Exception as inst: 
    print(type(inst))
    print(inst.args[0])
    # instabot.quit()

# instabot.quit()

