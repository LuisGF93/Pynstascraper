from selenium import webdriver as web
from selenium.webdriver.common import by as find
import os
from urllib import request
#import ssl
from downloader import downloader
from downloader import createHashtagList
import argparse

#command line arguments to execute the script
commandParser = argparse.ArgumentParser()
commandParser.add_argument('--mainPath', help='path to main directory')
commandParser.add_argument('--user', help='instagram user id')
commandParser.add_argument('--password', help='instagram user password')
args = commandParser.parse_args()

#labels
labList = []
createHashtagList(labList)

#user agent
opener = request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')]
request.install_opener(opener)

#ssl
#ssl._create_default_https_context = ssl._create_unverified_context

#url instagram
urlLink = "https://www.instagram.com/"

#path to create the different folders
mainPath = args.mainPath

if not os.path.exists(mainPath):
    os.mkdir(mainPath)

for x in labList:
    dirPath = os.path.join(mainPath, x[0])
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

#initialize Driver for Chrome
cDriver = web.Chrome(executable_path='/usr/local/bin/chromedriver')
cDriver.get(urlLink)
cDriver.implicitly_wait(time_to_wait=2000)

#click on cookies
cDriver.find_element(find.By.XPATH, "/html/body/div[2]/div/div/div/div[2]/button[1]").click()

#YOUR ID CREDENTIALS
userName = args.user
psswrd = args.password

#CREDENTIALS INPUT
cDriver.find_element(find.By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(userName)
cDriver.find_element(find.By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(psswrd)
cDriver.find_element(find.By.XPATH, "//*[@id='loginForm']/div/div[3]/button/div").click()

#search for the images
for lab in labList:
    dirPath = os.path.join(mainPath, lab[0])
    search = lab[1]
    downloader(cDriver, search, dirPath)

#close Chrome
cDriver.close()
