from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, re, json, shutil, pandas

buka = open("setup.json").read()
baca = json.loads(buka)

n = int()
opt = Options()
opt.binary_location = shutil.which("google-chrome-stable")
opt.add_argument("--headless")
driver = webdriver.Chrome(options=opt)

driver.get(baca["url"]["login"])
print("Opening Login Page")
time.sleep(2)
try:
    close = driver.find_element_by_xpath('//*[@id="myModal"]/div/div/div[3]/button').send_keys(Keys.ENTER)
    time.sleep(1)
except:
    time.sleep(1)
print("Inputing Username and Password")
username = driver.find_element_by_xpath('//*[@id="username"]')
username.send_keys(baca["username"])
password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys(baca["password"])
password.send_keys(Keys.ENTER)

def cekURL():
    pola = re.compile(r"ig|instagram")
    cari = ""
    try:
        cari = re.search(pola, driver.current_url)
    except:
        return False
    if (cari):
        return True
    else:
        return False

def cekHasil():
    try:
        hasil = driver.find_element_by_xpath('//*[@id="userList"]/p[1]')
        if (hasil):
            return True
    except:
        return False

while (cekURL()):
    time.sleep(0.25)
    continue
else:
    driver.get(baca["url"]["follow"])

time.sleep(1)
page = driver.page_source
soup = BeautifulSoup(page, "html.parser")
credit = soup.findAll(id = "takipKrediCount")[0].get_text()
print("Checking The Available Credit")
if (int(credit) <= 0):
    print("Out Of Credit")
    exit(0)
else:
    print("Credit Available : {}".format(int(credit)))

target = driver.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div[2]/form/div/div/input')
print("Inputing The Target Username")
target.send_keys(baca["target"])
target.send_keys(Keys.ENTER)

idIG = re.search("\d+", driver.current_url)
if (idIG):
    print("Your Instagram ID : " + idIG.group())
else:
    print("Wrong Username")
    driver.refresh

if (baca["number"] == "max"):
    n = int(credit)
else:
    try:
        n = int(baca["number"])
    except:
        print("Wrong Input")
        exit(0)

number = driver.find_element_by_xpath('//*[@id="formTakip"]/div[2]/input')
number.clear()
print("Inputing Number : ".format(n))
number.send_keys(n)
submit = driver.find_element_by_xpath('//*[@id="formTakipSubmitButton"]')
ActionChains(driver = driver).click(submit).perform()
print("Perform Action...")
while (not cekHasil()):
    time.sleep(0.25)
    continue
time.sleep(3)

page = driver.page_source
soup = BeautifulSoup(page, "html.parser")
listID = soup.findAll(id = "userList")[0]
listID = list(listID.children)
x = '{ "STATUS": [], "RESULT": [] }'
listData = json.loads(x)
banyakID = len(listID)
print(listID[0].get_text())
print("\n")
for i in range(1, banyakID):
    data = listID[i].get_text().split(". Result: ")
    status = listData["STATUS"]
    result = listData["RESULT"]
    status.append(data[0])
    result.append(data[1])

print(pandas.DataFrame(listData))
