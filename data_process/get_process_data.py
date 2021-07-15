import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

base_url = 'http://pems.dot.ca.gov'
station_url = base_url + '/?district_id=11&dnode=District&content=elv&tab=stations&pagenum_all=1'
headers = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    'Cache-Control':
    'max-age=0',
    'Connection':
    'keep-alive',
    'Cookie':
    '__utma=158387685.1561913567.1615192626.1615192626.1615192626.1; __utmz=158387685.1615192626.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); nmstat=7e44e525-0281-a9df-e54c-2ff801cddc8e; _ga=GA1.2.1561913567.1615192626; __utmz=267661199.1615193514.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=e633136de17c9bea79446e4fbf137666; __utma=267661199.1561913567.1615192626.1616861232.1616905253.9; __utmc=267661199; __utmt=1; __utmb=267661199.2.10.1616905253',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
station_html = requests.get(station_url, headers=headers)
station_soup = BeautifulSoup(station_html.content)
station_link_list = station_soup.find_all(href=re.compile(r'station_id'))
station_location = {}
with open('/Users/ran/Desktop/station_location.txt', 'a+') as f:
    for station_link in station_link_list:
        location_url = base_url + station_link['href']
        location_html = requests.get(location_url, headers=headers)
        location_soup = BeautifulSoup(location_html.content)
        location_soup_td_tag_list = location_soup.find(
            id='segment_context_box').find_all('table')[1].find_all(
                'tr')[2].find_all('td')
        lat = location_soup_td_tag_list[7].text
        lng = location_soup_td_tag_list[8].text
        station_location[station_link.text] = (lat, lng)
        f.write(station_link.text + ',' + lat + ',' + lng + os.linesep)
station_location_data = pd.read_csv('/Users/ran/Desktop/station_location.csv',
                                    header=None)
station_location_data.columns = ['ID', 'Lat', 'Lng']
way_station_data = df = pd.read_excel(
    '/Users/ran/Desktop/traffic/way_station.xlsx')
data = station_location_data.merge(way_station_data,
                                   on='ID')[['ID', 'Fwy', 'Lat', 'Lng']]
data.to_csv('/Users/ran/Desktop/traffic/way_station_location.csv', index=False)