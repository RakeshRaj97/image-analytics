from bs4 import BeautifulSoup
from selenium import webdriver

def image_url(url):
    browser = webdriver.Chrome('driver/chromedriver.exe')
    browser.get('https://www.linkedin.com/uas/login')
    file = open('config.txt')
    lines = file.readlines()
    username = lines[0]
    password = lines[1]

    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)

    elementID.submit()

    link = url
    browser.get(link)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    name_div = soup.find('div', {'class': 'pv-top-card__photo-wrapper ml0'})
    name_loc = name_div.find_all('img')
    name = name_loc[0].get('src').strip()
    return name
