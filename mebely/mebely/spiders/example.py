import scrapy
import time


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["pm.ru"]
    start_urls = [f"https://pm.ru/category/mebel-dlya-doma/komody/?page={page}" for page in range(1, 10)]

    def parse(self, response):
        heads = response.xpath('//div[@class="good__link-wrapper"]')
        self.logger.info(f'Найдено {len(heads)} товаров.')
        for head in heads:
            product_url = 'https://pm.ru' + head.xpath('.//a[@class="good__link"]/@href').get()
            if product_url:
                self.logger.info(f'Собранный URL товара: {product_url}')
                yield response.follow(product_url, self.parse_product)
        time.sleep(1)  # Это добавит задержку в 1 секунду между запросами

    def parse_product(self, response):
        # Сбор полной информации о товаре
        data = {
            'name': response.xpath('.//h1[@class="catalog-header__title"]/text()').get().strip(),
            'price': response.xpath('.//span[@class="price_no_rub"]/text()').get().strip(),
            'instruction': 'https://pm.ru' + response.xpath('.//a[@class="item-options__link"]/@href').get(),
            'photo': 'https://pm.ru' + response.xpath(
                './/div[@class="swiper-aspect4x3 swiper-loader"]/a/img/@src').get(),
            "params": []

        }
        # yield data
        rows = response.xpath('//ul[@class="item-options__list"]/li')

        for row in rows:
            key = row.xpath('./span[@class="item-options__item-span"]/text()').get().strip()
            value = row.xpath('./div[@class="item-options__item-text"]/span/text()').getall()
            value = " ".join(value).strip()
            if key and value:  # Проверка на наличие key и value
                all_params = f"{key}: {value}"  # Формирование строки параметров
                data['params'].append(all_params.strip())  # Добавление в список
        yield data
