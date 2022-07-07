import requests, json, csv
from bs4 import BeautifulSoup as BS

url = 'https://coinmarketcap.com'

headers = {
    'accept': 'application/json, text/plain, */*',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

def get_html():
    r = requests.get(url, headers=headers)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

def get_hrefs():
    hrefs = []

    with open('index.html', encoding='utf-8') as file:
        html = file.read()

    soup = BS(html, 'html.parser')

    all_cryptos = soup.find(class_='h7vnx2-2 czTsgW cmc-table').find('tbody').find_all('tr')

    for crypto in all_cryptos:
            hrefs.append('https://coinmarketcap.com/currencies/' + crypto.find('a', class_='cmc-link').get('href'))

    with open('hrefs.txt', 'w') as file:
        for href in hrefs:
            file.write(f'{href}\n')

def get_data():
    data = []

    with open('index.html', encoding='utf-8') as file:
        html = file.read()

    with open('data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'href', 'symbol', 'logo', 'price', 'market_cap'
        ])

    soup = BS(html, 'html.parser')

    all_cryptos = soup.find(class_='h7vnx2-2 czTsgW cmc-table').find('tbody').find_all('tr')

    count = 1
    for crypto in all_cryptos:
        if count <= 10:
            name = crypto.find(class_='sc-16r8icm-0 sc-1teo54s-1 dNOTPP').find('p').text
            href = url + crypto.find(class_='sc-16r8icm-0 escjiH').find(class_='cmc-link').get('href')
            symbol = crypto.find(class_='sc-1teo54s-2 fZIJcI').find('p').text
            logo = crypto.find(class_='sc-16r8icm-0 sc-1teo54s-0 dBKWCw').find('img').get('src')
            price = crypto.find(class_='sc-131di3y-0 cLgOOr').text
            market_cap = crypto.find('span', class_='sc-1ow4cwt-1 ieFnWP').text

            data.append(
                {
                    'name': name,
                    'href': href,
                    'symbol': symbol,
                    'logo': logo,
                    'price': price,
                    'market_cap': market_cap
                }
            )

            with open('data.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([name, href, symbol, logo, price, price, market_cap])

        count += 1

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    get_html()
    get_hrefs()
    get_data()

if __name__ == '__main__':
    main()