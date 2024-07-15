import requests
from bs4 import BeautifulSoup
import json


class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching the eBay page: {e}")
            return None

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Название товара
        title_element = soup.find('h1', class_='x-item-title__mainTitle')
        self.data['title'] = title_element.get_text(strip=True) if title_element else 'No title found'

        # Ссылка на фото товара
        image_element = soup.find('div', class_='ux-image-carousel-item').find('img')
        self.data['image_url'] = image_element['src'] if image_element else 'No image found'

        # Ссылка на товар
        self.data['item_url'] = self.url

        # Цена товара
        price_element = soup.find('span', class_='ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD')
        self.data['price'] = price_element.get_text(strip=True) if price_element else 'No price found'

        # Продавец
        seller_element = soup.find('div', class_='x-sellercard-atf__info__about-seller').find('a', class_='ux-action')

        self.data['seller'] = seller_element.get_text(strip=True) if seller_element else 'No seller found'


        # Цена доставки и местоположение
        shipping_info = soup.find('div', class_='ux-labels-values__values-content')
        if shipping_info:
            shipping_texts = shipping_info.find_all('span', class_='ux-textspans')
            if shipping_texts:
                self.data['shipping_price'] = shipping_texts[0].get_text(strip=True) if len(
                    shipping_texts) > 0 else 'No shipping info'
                self.data['location'] = shipping_texts[-1].get_text(strip=True) if len(
                    shipping_texts) > 1 else 'No location info'

        # Вывод данных в консоль в формате JSON
        print(json.dumps(self.data, indent=4, ensure_ascii=False))

        # Сохранение данных в файл
        with open('ebay_item_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def scrape(self):
        html = self.fetch_page()
        if html:
            self.parse_page(html)


if __name__ == "__main__":
    url = "https://www.ebay.com/itm/204278525642?itmmeta=01J2VBD5VFY3WQ9SE5NWDPSDM1&hash=item2f8ff2eeca:g:kBkAAOSwGt5kFrjd"
    scraper = EbayScraper(url)
    scraper.scrape()
