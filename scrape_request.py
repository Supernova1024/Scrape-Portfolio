import requests
from bs4 import BeautifulSoup 
import time
from lxml import etree
import asyncio
import re
import string

profile_base_url = 'https://www.freelancer.com/u/'
lancers_base_url = 'https://www.freelancer.com/freelancers/skills/'
portfolio_base_url = 'https://www.freelancer.com/u/filipstamate/portfolio/'
# HEADERS = {"content-type": "image/png"}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
def scrape(url):
    response = requests.get(url, headers=HEADERS).text
    html_data = BeautifulSoup(response, 'html.parser')
    return html_data, response


def clean_username(name):
    username = str(name.text).split("\n")[1].replace(" ", "")
    return username


async def scrape_img(link, res_profile, username, country, list1):
    imgs = []
    # if username == 'futivetechnet':

    ## method 1
    # item_name1 = link.text.replace(' – ', '--').encode('ascii', 'ignore').decode("utf-8")
    # translation_table = dict.fromkeys(map(ord, "'!@\#$^*}{;.><?`"), '')
    # item_name = item_name1.translate(translation_table).replace(' - ', '---').replace(' // ', '--').replace(' ||', '-').replace(' |', '-').replace(' , ', '--').replace(',', '').replace(' =', '-').replace('=', '').replace('] ', '-').replace(']', '').replace(' [', '-').replace('[', '').replace(' : ', '--').replace(':', '').replace(' % ', '--').replace('%', '').replace(' ~ ', '--').replace('~', '').replace(' " ', '--').replace('"', '').replace(' + ', '--').replace('+', '').replace(' & ', '--').replace('&', '').replace(') ', '-').replace(')', '').replace(' (', '-').replace('(', '').replace(' / ', '--').replace('/', '').replace('  ', '-').replace(' ', '-')[1:]

    ## method 2
    item_name1 = link.text.replace('  ', '-').replace(' ', '-').replace('"', '').encode('ascii', 'ignore').decode("utf-8")
    translation_table = dict.fromkeys(map(ord, "~!@#$%^&*()+}{][:?><`=';/.,\|–"), '')
    item_name = item_name1.translate(translation_table)[1:]

    if item_name == '':
        item_name = '-'

    # print("***", username, link.text)
    item_number = res_profile.split(item_name)[1].split('&')[0]
    portfolio_detail_url = profile_base_url + username + '/portfolio/' + item_name + item_number
    # print("==portfolio_detail_url=====", portfolio_detail_url)
    portfolio_detail, res_detail = scrape(portfolio_detail_url)
    imgs = portfolio_detail.find_all('img', {'class': 'PagePortfolio-image'})

    for img in imgs:
        src = img['src']
        block = username + ',' + country.split(' ')[1] + ',' + src
        list1.append(block)
        # textfile1 = open("data7.txt", "a")
        # textfile1.write(block + "\n")
        # textfile1.close()
    


async def scrape_portfolio(portfolio, res_profile, username, country, list1):
    img_links = []
    img_links_repeat = portfolio.find_all('div', {'class': 'NativeElement ng-star-inserted'})
    img_links = list(dict.fromkeys(img_links_repeat))

    for link in img_links:
        await scrape_img(link, res_profile, username, country, list1)
 

async def scrape_profile(a_username, list1):
        portfolios = []
        username = clean_username(a_username)
        profile_url = profile_base_url + username
        profile_html_data, res_profile = scrape(profile_url)
        dom_profile = etree.HTML(str(profile_html_data))
        country = dom_profile.xpath('/html/body/app-root/app-logged-out-shell/app-user-profile-wrapper/app-user-profile/fl-bit[2]/fl-bit[2]/fl-container/fl-grid/fl-col[2]/app-user-profile-summary/fl-card/fl-bit/fl-bit/fl-grid/fl-col[1]/fl-grid/fl-col[2]/app-user-profile-summary-information/fl-grid/fl-col/fl-text/div/fl-link/a/div/div')[0].text
        portfolios = profile_html_data.find_all('fl-bit', {'class': 'PortfolioCardContent'})
        
        for portfolio in portfolios:
            await scrape_portfolio(portfolio, res_profile, username, country, list1)


async def scrape_page(page, list1):
    a_usernames = []
    users_by_skill_url = lancers_base_url + skill + str(page)
    print(users_by_skill_url)
    user_html_data, res_skill = scrape(users_by_skill_url)
    a_usernames = user_html_data.find_all('a', {'class': 'find-freelancer-username-mobile'})
    for a_username in a_usernames:
        await scrape_profile(a_username, list1)

    
async def start_scrape(skill):
    list1 = []
    try:
        for page in range(1, 100):
            print("====================", page)
            await scrape_page(page, list1)
        textfile1 = open("data8.txt", "a")
        print(list1)
        for block in list1:
            textfile1.write(block + "\n")
        textfile1.close()
    except Exception as ex:
        print(ex)
        textfile2 = open("data7.txt", "a")
        print(list1)
        for block in list1:
            textfile2.write(block + "\n")
        textfile2.close()


if __name__ == '__main__':
    skill = '3d-modelling/'
    # start_scrape(skill)
    asyncio.run(start_scrape(skill))