import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import numpy as np
import csv

browser = webdriver.Chrome('E:/Tools/Dev_tools/chromedriver.exe') 
profile_base_url = 'https://www.freelancer.com/u/'
lancers_base_url = 'https://www.freelancer.com/freelancers/skills/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

# def clean_username(name):
#     username = str(name.text).split("\n")[1].replace(" ", "")
#     return username

def get_username(name):
    return name.split(profile_base_url)[1]

def scrape_profile(username, url, users_by_skill_url, name_coun_img, textfile):
    ## get browser of profile by username
    browser.get(url)
    time.sleep(3)
    items = browser.find_elements_by_class_name('CardClickable')
    Breadcrumbs = browser.find_element_by_class_name('Breadcrumbs')
    country_name = browser.find_element_by_xpath('/html/body/app-root/app-logged-out-shell/app-user-profile-wrapper/app-user-profile/fl-bit[2]/fl-bit[2]/fl-container/fl-grid/fl-col[2]/app-user-profile-summary/fl-card/fl-bit/fl-bit/fl-grid/fl-col[1]/fl-grid/fl-col[2]/app-user-profile-summary-information/fl-grid/fl-col/fl-text/div/fl-link/a/div/div').text
    print("========country_name=======", country_name)

    # for item in items:
    for i in range(0, len(items)):
        items = browser.find_elements_by_class_name('CardClickable')
        items[i].click()
        time.sleep(4)
        imgs = browser.find_elements_by_class_name('PagePortfolio-image')
        back_urls = browser.find_elements_by_class_name('Breadcrumbs-link')
        block = ''
        for img in imgs:
            time.sleep(1)
            # print("=======333===", img.get_attribute("src"))
            image_link = img.get_attribute("src").split('&')[0]
            block = country_name + ',' + username + ',' + image_link

            # name_coun_img.append(block)
            # print("=========name_coun_img======", name_coun_img)
            # for element in name_coun_img:
            print("-----1--------")
            textfile1 = open("data.txt", "a")
            textfile1.write(block + "\n")
            textfile1.close()
            print("------2-------")
            # time.sleep(2)

        hr = back_urls[2].get_attribute('href')
        print("====hr=======", hr)
        back_urls[2].click()
        time.sleep(5)
    browser.get(users_by_skill_url)

def start_scrape(skill):
    ## get user name and profile url
    users_by_skill_url = lancers_base_url + skill
    browser.get(users_by_skill_url)
    name_coun_img = []
    textfile = open("data.txt", "w")
    while True:
        time.sleep(5)
        modeling_users = browser.find_elements_by_class_name('find-freelancer-username-mobile')
        print("===len(modeling_users)=======", len(modeling_users))
        # for user in modeling_users:
        for j in range(0, len(modeling_users)):
            # if j == 0 or j == 9:
            modeling_users = browser.find_elements_by_class_name('find-freelancer-username-mobile')
            # modeling_users[j]
            a_usernames = modeling_users[j].get_attribute('href')
            username = get_username(a_usernames)
            profile_url = profile_base_url + username
            print("=====j=====", j)
            scrape_profile(username, profile_url, users_by_skill_url, name_coun_img, textfile)
            time.sleep(5)
        try:
            browser.find_element_by_xpath("/html/body/div[2]/main/div/div[3]/div[2]/div/div[2]/div[4]/div/ul/li[7]/a").click()
            print("=====click============")
            time.sleep(5)
        except NoSuchElementException :
            
            break
        textfile.close()


    # for username in usernames:
    #     time.sleep(1)
    #     username.click()
    #     items = browser.find_elements_by_class_name('PortfolioItemCard-file-image')
    #     print("*****************", items)
    #     for item in items:
    #         item.click()
    #         time.sleep(1)
    #         imgs = browser.find_elements_by_class_name('PagePortfolio-image')
    #         for img in imgs:
    #             print("==========", img["src"])



if __name__ == '__main__':
    skill = '3d-modelling'
    start_scrape(skill)