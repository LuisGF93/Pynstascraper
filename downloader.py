from selenium.webdriver.common import by as find
from urllib.error import HTTPError
import time as t
import os
from urllib import request
import csv

class Link:
    def __init__(self, src, status):
        self.src = src
        self.status = status

def downloader(cdriverf, finder, directory):

    find_a_term = finder
    cdriverf.find_element(find.By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input").send_keys(find_a_term)
    cdriverf.find_element(find.By.XPATH, '//a[contains(@class, "yCE8d")]').click()

    lastHigh = 0
    newHigh = 0
    image_loaded = 0
    image_counter = 0
    srcList = []
    trigger = 0
    index = 0

    #load state if exists
    if not os.path.exists(finder+"savedState.csv"):
        open(finder+"savedState.csv", "a+")
    else:
        srcList = loadState(finder)
        print("loaded images")
        for l in srcList:
            print(l)

    while checkbodyheight(lastHigh, newHigh) | image_loaded < 400:

        newHigh = cdriverf.execute_script("return document.body.scrollHeight")

        if image_loaded < 50:
            cdriverf.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            t.sleep(3)
            for i in cdriverf.find_elements_by_xpath('//img[contains(@class, "FFVAD")]'):
                image_counter += 1
            image_loaded = image_counter
            print("image loaded number", image_loaded, "\n")
            image_counter = 0

        elif ((image_loaded == 50) & (trigger == 0)) | ((image_loaded == 51) & (trigger == 0)):
            for i in cdriverf.find_elements_by_xpath('//img[contains(@class, "FFVAD")]'):
                aux = i.get_attribute('src')
                if any(link.src == aux for link in srcList):
                    print("src repeated, not loaded")
                else:
                    auxLink = Link(aux, False)
                    srcList.append(auxLink)
                    image_loaded += 1
                    print("image loaded number ", image_loaded, "\n")

            cdriverf.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            t.sleep(3)
            trigger = 1

        elif (image_loaded >= 50) & (trigger == 1):
            cdriverf.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            t.sleep(3)
            for i in cdriverf.find_elements_by_xpath('//img[contains(@class, "FFVAD")]'):
                aux = i.get_attribute('src')
                if any(link.src == aux for link in srcList):
                    print("src repeated, not loaded")
                else:
                    auxLink = Link(aux, False)
                    srcList.append(auxLink)
                    image_loaded += 1
                    print("image loaded number ", image_loaded, "\n")

        lastHigh = cdriverf.execute_script("return document.body.scrollHeight")


    #save the state before download the images
    for line in srcList:
        print(line.src)

    #downloading the images
    for l in srcList:
        try:
            if(l.status == False):
                jpgPath = os.path.join(directory, finder + str(index) + ".jpg")
                request.urlretrieve(l.src, jpgPath)
                l.status = True
                index += 1
                t.sleep(3)
                print("download ok")
        except TimeoutError:
            print("timeout, cannot get the pic")
        except HTTPError:
            print("forbidden, cannot get the pic")

    saveState(srcList, finder)

def checkbodyheight(lasth, newh):
    if lasth == newh:
        return False
    else:
        return True

def saveState(srclist, finder):
    with open(finder+"savedState.csv", 'w') as csv_file:
        file = csv.writer(csv_file, delimiter=",")
        for link in srclist:
            file.writerow([link.src, link.status])

def loadState(finder):
    auxlist = []
    with open(finder+"savedState.csv", 'r') as f:
        readingCsv = csv.reader(f)
        for link in readingCsv:
            aux = Link(link[0], link[1])
            auxlist.append(aux)
    return auxlist

def createHashtagList(labList):
    aux = []
    index = 0
    flag = True
    while flag:
        print("input Directory name")
        aux.append(input())
        print("input Hashtag name")
        aux.append(input())
        aux.append(index)
        index += 1
        labList.append(aux)
        print("press 0 to scape")
        keyEsc = input()
        if keyEsc == '0':
            flag = False
