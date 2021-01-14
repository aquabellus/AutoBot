from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import json
import shutil
import random
import requests
import traceback

browserBin = shutil.which("google-chrome-stable")
try:
    len(browserBin)
except (TypeError):
    browserBin = shutil.which("brave-browser")

class Browser:
    opt = Options()
    opt.binary_location = browserBin
    opt.add_argument("--headless")
    driver = webdriver.Chrome(options = opt)

    def login(self, url):
        self.driver.get(url)
        print("Login...")
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath('//*[@id="myModal"]/div/div/div[3]/button').send_keys(Keys.ENTER)
            print("Banner Detected")
            time.sleep(1)
        except (NoSuchElementException):
            print("No Banner Detected")
            time.sleep(1)

        print("Inputing Username and Password")
        print("Username ID : {}".format(uid))
        print("Username Used : {}".format(tumbal[1]))
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys(tumbal[1])
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(tumbal[2])
        password.send_keys(Keys.ENTER)
        pola = re.compile(r"ig|instagram")
        while True:
            try:
                time.sleep(1)
                re.search(pola, self.driver.current_url).group()
                continue
            except (AttributeError):
                break
        time.sleep(2)

    def cekHasil(self):
        try:
            hasil = self.driver.find_element_by_xpath('//*[@id="userList"]/p[1]')
            if (hasil):
                return True
        except (NoSuchElementException):
            return False

    def add(self, url, creditID, inputTargetForm, inputTarget, inputActionForm, inputValue, actionButton):
        self.driver.get(url)
        time.sleep(1)
        print("Check Available Credit...")
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        credit = soup.findAll(id = "{}".format(creditID))[0].get_text()
        if (int(credit) <= 0):
            print("Out Of Credit")
            return 0
        else:
            print("Credit Available : {}".format(int(credit)))

        print("Input Target...")
        print("Target: {}".format(inputTarget))
        target = self.driver.find_element_by_xpath(inputTargetForm)
        target.send_keys(inputTarget)
        target.send_keys(Keys.ENTER)

        if (inputValue == "max"):
            inputValue = int(credit)

        actionForm = self.driver.find_element_by_xpath(inputActionForm)
        actionForm.clear()
        print("Input Credit: {}".format(inputValue))
        actionForm.send_keys(inputValue)
        submit = self.driver.find_element_by_xpath(actionButton)
        ActionChains(driver = self.driver).click(submit).perform()
        print("Perform Action...")
        while (not self.cekHasil()):
            time.sleep(0.25)
            continue
        time.sleep(5)

        banyakUser = self.driver.find_element_by_xpath('//*[@id="userList"]/p[1]')
        print(banyakUser.text)
        time.sleep(2)

    def getIGMedia(self, username):
        r = requests.get("https://instagram.com/{}/?__a=1".format(username))
        index = json.loads(r.text)["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
        selectIndex = random.sample(range(0, len(index)), 1)
        shortcode = index[selectIndex[0]]["node"]["shortcode"]
        mediaLink = "https://instagram.com/p/{}/".format(shortcode)
        r.close()
        return mediaLink

    def exit(self):
        self.driver.close()

listLogin = [
    "https://ig.informatikamu.id/member/",
    "https://instagram.informatikamu.id/member/"
]

listFollow = [
    "https://ig.informatikamu.id/tools/send-follower/",
    "https://instagram.informatikamu.id/tools/send-follower/"
]

listLike = [
    "https://ig.informatikamu.id/tools/send-like/",
    "https://instagram.informatikamu.id/tools/send-like"
]

def addFollower():
    if (bool(target["follow"])):
        follower = Browser()
        for i in range(0, len(listLogin)):
            print("\n")
            print("LOGIN TO {}".format(listLogin[i]))
            url = listFollow[i]
            creditID = "takipKrediCount"
            inputTargetForm = "/html/body/main/div[2]/div[1]/div/div[2]/form/div/div/input"
            inputTarget = target["target"]
            inputActionForm = '//*[@id="formTakip"]/div[2]/input'
            inputValue = target["number"]
            actionButton = '//*[@id="formTakipSubmitButton"]'
            if (re.search(re.compile(r"instagram"), url)):
                inputTargetForm = "/html/body/div/div[2]/div[1]/div[3]/div[2]/div/form/div/input"

            follower.login(listLogin[i])
            follower.add(url, creditID, inputTargetForm, inputTarget, inputActionForm, inputValue, actionButton)

    else:
        print("Skipping Add Followers Feature")


def addLike():
    if (bool(target["like"])):
        like = Browser()
        for i in range(0, len(listLogin)):
            print("\n")
            print("LOGIN TO {}".format(listLogin[i]))
            url = listLike[i]
            creditID = "begeniKrediCount"
            inputTargetForm = "/html/body/main/div[2]/div[1]/div[2]/div[2]/form/div/div/input"
            inputActionForm = '//*[@id="formBegeni"]/div[2]/input'
            inputValue = target["number"]
            actionButton = '//*[@id="formBegeniSubmitButton"]'
            if (re.search(re.compile(r"instagram"), url)):
                inputTargetForm = '//*[@id="autolikes"]'

            inputTarget = like.getIGMedia(target["target"])
            print("Selected Post Media : " + inputTarget)
            like.login(listLogin[i])
            like.add(url, creditID, inputTargetForm, inputTarget, inputActionForm, inputValue, actionButton)

    else:
        print("Skipping Add Likes Feature")

if __name__ == "__main__":
    print("####################################################")
    print("###################INSTAGRAM BOT####################")
    print("####################################################")
    print("")
    print("AUTO ADD LIKES AND FOLLOWERS TO YOUR PRIMARY ACCOUNT")
    print("              DO WITH YOUR OWN RISK")
    print("        READ OUR LICENSE FOR MORE DETAILS")
    print("")

    buka = open("helper/helper.json").read()
    uid = json.loads(buka)["id"]

    buka = open("helper/target.json").read()
    target = json.loads(buka)

    buka = open("helper/tumbal.json").read()
    tumbal = json.loads(buka)[uid]
    
    try:
        addFollower()
        time.sleep(5)
        addLike()
    except UnexpectedAlertPresentException as e:
        print("\nAn Error Occured:")
        traceback.print_tb(e.__traceback__)
        raise SystemExit(e.alert_text)
    except (IndexError, Exception, SystemError) as e:
        print("\nAn Error Occured:")
        traceback.print_tb(e.__traceback__)
        raise SystemExit(str(e))
    else:
        print("Script Successfully Executed !!!")