from urllib3 import PoolManager
from bs4 import BeautifulSoup


url = 'http://utopiac.ddns.net:8000'
page = PoolManager().request("GET", url)

content_page = page.data

soup = BeautifulSoup(content_page, 'html.parser')
images_list = soup.find_all('img')
for i in images_list:
    print(url + i['src'])
    print(i['src'].split('/')[-1])
