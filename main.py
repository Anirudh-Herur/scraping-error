from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import requests

new_planet_data = []
planet_data = []
headers_list = ['name', 'light_year_from_earth',
                'planet_mass', 'stellar_magnitude', 'discovery_date', 'hyper_link', 'planet_type', 'discovery_date', 'planet_readius', 'orbital_radius', 'orbital_period', 'eccentricity']
browser = webdriver.Chrome(
    "C:/Users/Admin/Downloads/WhiteHat Python/Web Scraping/chromedriver_win32/chromedriver.exe")
browser.get("https://exoplanets.nasa.gov/exoplanet-catalog/")
time.sleep(10)


def scrap():
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    for i in range(0, 198):
        all_ul_tags = soup.find_all('ul', class_='exoplanet')
        for ul_tag in all_ul_tags:
            li_tags = ul_tag.find_all('li')
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all('a')[0].contents[0])
                else:
                    temp_list.append(li_tag.contents[0])
            hyper_link_li_tag = li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov/' +
                             hyper_link_li_tag.find_all('a')[0].get('href'))
            planet_data.append(temp_list)
        browser.find_element_by_xpath(
            "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a")



def scrap_more_data(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    temp_list = []
    all_tr_tags = soup.find_all('tr', class_='fact_row')
    for tr_tags in all_tr_tags:
        td_tags = tr_tags.find_all('td')
        for td_tag in td_tags:
            div_tag = td_tag.find_all('div', class_='value')[0].contents[0]
            temp_list.append(div_tag)
    new_planet_data.append(temp_list)

scrap()
for index, data in enumerate(planet_data):
    scrap_more_data(data[5])

final_planet_data = []

for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [i.replace('\n', '') for i in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[0:7]
    final_planet_data.append(data + new_planet_data_element)
with open("C:/Users/Admin/Downloads/WhiteHat Python/Web Scraping 2/planet data.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers_list)
        writer.writerows(final_planet_data)
