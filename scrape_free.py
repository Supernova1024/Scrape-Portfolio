import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
browser = webdriver.Chrome('E:/Tools/Dev_tools/chromedriver.exe') 
profile_base_url = 'https://www.freelancer.com/u/'
lancers_base_url = 'https://www.freelancer.com/freelancers/skills/'
def scrape(url):
    # response = requests.get(url)
    # text = response.text
    browser.get(url)
    html_data = BeautifulSoup(browser.page_source)
    return html_data

# card = browser.find_elements_by_class('PortfolioCardContent')
# card[0].click()
# time.sleep(1)

def clean_username(name):
    username = str(name.text).split("\n")[1].replace(" ", "")
    return username
    
def start_scrape(skill):
    users_by_skill_url = lancers_base_url + skill
    user_html_data = scrape(users_by_skill_url)
    a_usernames = user_html_data.find_all('a', {'class': 'find-freelancer-username-mobile'})

    username = clean_username(a_usernames[0])
    profile_url = profile_base_url + username
    profile_html_data = scrape(profile_url)
    # portfolio1 = profile_html_data.find_all('source', {'class': 'ng-star-inserted'})
    portfolios = profile_html_data.find_all('fl-bit', {'class': 'PortfolioCardContent'})
    i = 0
    for portfolio in portfolios:
        # print("===========", portfolio)
        img_links_repeat = portfolio.find_all('div', {'class': 'NativeElement ng-star-inserted'})
        img_links = list(dict.fromkeys(img_links_repeat))
        for link in img_links:
            i += 1
            link.click()
            time.sleep(1)
            figures = browser.find_elements_by_class("PagePortfolio-figure")
            print("==========", figures)
            # # print("----------", link.text, len(link.text), i)
            # portfolio_detail_url = portfolio_base_url + link.text
            # portfolio_detail = scrape(portfolio_detail_url)
            # print("&&&&&&", portfolio_detail_url)
            # imgs = portfolio_detail.find_all('figure', {'class': 'PagePortfolio-figure'})
            # print("*********", imgs)
# def start_scrape(skill):
#     users_by_skill_url = lancers_base_url + skill
#     user_html_data = scrape(users_by_skill_url)
#     a_usernames = user_html_data.find_all('a', {'class': 'find-freelancer-username-mobile'})

#     for a_username in a_usernames:
#         profile_url = profile_base_url + str(a_username.text)
#         print("******************", profile_url)
#         profile_html_data = scrape(profile_url)
#         # portfolio = profile_html_data.find_all('fl-picture', {'class': 'PortfolioItemCard-file-image'})
#         portfolio1 = profile_html_data.find_all('source')
#         print("++++++++", profile_html_data)
#         # for j  in portfolio:
#         #     portfolio1 = portfolio.find_all('a', {'class': 'ImageElement'})
#         #     print("============", portfolio1)
#         #     for i in portfolio:
#         #         print("======*********========", i)


if __name__ == '__main__':
    skill = '3d-modelling'
    start_scrape(skill)