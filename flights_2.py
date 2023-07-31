from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time


start_input = str(input('Enter Starting Location (City, State): '))
destination_input = str(input('Enter Destination (City, State): '))

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
opt = Options()
opt.add_argument(r"--silent")
opt.add_argument(r"--no-sandbox")
opt.add_argument(r"--disable-dev-shm-usage")
opt.add_argument(r'--ignore-certificate-errors')
opt.add_experimental_option("detach", True)
#opt.add_argument('headless')
#opt.add_argument(f'user-agent={user_agent}')
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=opt)


url = 'https://www.google.com/travel/flights?tfs=CBsQAhonEgoyMDIzLTA5LTAyagwIAxIIL20vMGYyczZyCwgCEgcvbS8wdnptGicSCjIwMjMtMDktMDlqCwgCEgcvbS8wdnptcgwIAxIIL20vMGYyczZAAUgBUgNVU0RwAXpsQ2pSSU4wTjFVM1ZyT1c5YVFUQkJVVzFZUldkQ1J5MHRMUzB0TFMwdExTMXZkWFYyTlVGQlFVRkJSMVJIUVZSRlNWVnNTazlCRWdaQlFURXlNRFlhQ3dpTmd3RVFBaG9EVlZORU9CeHdqWU1CmAEBsgERGAEgASoLCAMSBy9tLzB2em0&hl=en-US&curr=USD&sa=X&ved=0CAoQtY0DahgKEwi41qz95LWAAxUAAAAAHQAAAAAQiQE'
driver.get(url)

box_start = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input'
element = (By.XPATH, box_start)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

start_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'
element = (By.XPATH, start_text)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(start_input + '\n')

box_destination = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input'
element = (By.XPATH, box_destination)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

destination_text = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'
element = (By.XPATH, destination_text)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(destination_input + '\n')

time.sleep(8)

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

flights = soup.find_all("li", class_="pIav2d")


count = 0

for flight in flights:
    description = flight.find("div", class_='JMc5Xc').get("aria-label")
    print(description)
    count += 1

    if count == 6:
        break


#things to do
ttd = 'https://www.google.com/travel/things-to-do?dest_mid=%2Fm%2F03l2n&dest_state_type=main&dest_src=yts&q=Houston%20&ved=0CAAQ8IAIahcKEwiw1azKjriAAxUAAAAAHQAAAAAQBw'
driver.get(ttd)

clear_button = '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/div/div/div[3]/button'
element = (By.XPATH, clear_button)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).click()

search_box = '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div[2]/input'
element = (By.XPATH, search_box)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable(element)).send_keys(destination_input + '\n')

time.sleep(8)

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

places = soup.find_all("div", class_='f4hh3d')

for place in places:
    thingstd = place.find('div', class_='Ld2paf').get("data-title")
    print(thingstd)

    
#restaurants

c_and_s = destination_input.split(',')

city = c_and_s[0]
state = c_and_s[1]
state = state[1:]

search_link = ('https://www.yelp.com/search?cflt=restaurants&find_loc=' + city + '%2C+' + state)
driver.get(search_link)

time.sleep(6)

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

restaurants = soup.find_all("div", class_='  border-color--default__09f24__NPAKY')

for restaurant in restaurants:
    res = restaurant.find('a', class_= 'css-19v1rkv').get('name')
    href = restaurant.find('a', class_= 'css-19v1rkv').get('href')
    link = 'https://www.yelp.com' + href
    print(res)
    print(link)