import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import random


def getProxy():

    # get proxy from free-proxy-list.net
    page = requests.get('https://free-proxy-list.net/')
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.find('table', attrs={'class': 'table table-striped table-bordered'})\
            .find_all('tr')
        rawTable = [row.find_all('td') for row in rows[1:]]

        proxy = [(f'{ip.text}:{port.text}', code) for ip, port, code, _, anonymity, *_ in rawTable
                if code.text!='RU' and anonymity.text == 'elite proxy']
    
    proxy = set(proxy)

    # get proxies from proxydb.net
    numproxy = 1800
    proxy_list = []
    i = 0

    for i in range(numproxy // 30):
        print(i)
        time.sleep(random.random())
        page = requests.get(f'https://proxydb.net/?anonlvl=4&country=&offset={30*i}&protocol=http&protocol=https')
        if page.status_code != 200: 
            print(f'{i} failed')
            continue

        soup = BeautifulSoup(page.text, 'html.parser')

        rows = soup.find('tbody').find_all('tr')
        rawTable = [row.find_all('td') for row in rows]
        proxies = [f'{ip.text.strip()}:{port.find('a').text.strip()}' for ip, port, *_ in rawTable]
        proxy_list.extend(proxies)


    proxy_list = set(proxy_list)

    return proxy | proxy_list

def checkProxy(proxy, url, listToSave):
    try:
        page = requests.get(url,
                            proxies={'http': proxy, 'https': proxy},
                            timeout=3)
        if page.status_code == 200:
            listToSave.append(proxy)
    except:
        pass

if __name__ == "__main__":
    goodProxies = []
    checkonInsta = lambda x: checkProxy(x, 'https://www.instagram.com', goodProxies)
    proxy = getProxy()
    print(len(proxy))
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     executor.map(checkonInsta, proxy)

    # print(len(goodProxies))

    # with open('proxy.txt', 'w') as f:
    #     f.write('\n'.join(goodProxies))