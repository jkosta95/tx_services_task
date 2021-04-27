
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from xml.dom import minidom
from datetime import datetime

class InfostudSpider(scrapy.Spider):

    name = 'infostud_spider'

    def __init__(self):
        main_url = 'https://poslovi.infostud.com/sitemap-jobs.xml'
        headers = requests.utils.default_headers()
        resp = requests.get(main_url, headers=headers)
        data = resp.text
        xmldoc = minidom.parseString(data)
        itemlist = xmldoc.getElementsByTagName('loc')
        parsing_list = []
        for item in itemlist:
            if item.firstChild:
                parsing_list.append(str(item.firstChild.data))
        self.start_urls = parsing_list

    def parse(self, response):
        item = {}
        job_title = response.xpath('.//h1[@class="'+InfostudSpider.get_job_title_class(response)+'"]/text()').extract_first()
        employer_name = InfostudSpider.get_employer_name(response)
        # job_address = response.xpath('.//p[@class="uk-margin-remove-bottom uk-margin-small-top"]//text()').getall()[1].strip()
        job_address = InfostudSpider.get_job_address(response)
        #city = job_address.split(',')[0] if ',' in job_address else job_address
        cities = InfostudSpider.get_city(job_address)
        publish_date_str = response.xpath('.//p[@class="uk-margin-remove-top uk-text-bold"]//text()').getall()[1].strip()
        publish_date = datetime.strptime(publish_date_str, '%d.%m.%Y.')
        job_details = []
        for one_job in response.xpath('.//span[@class="uk-flex uk-flex-middle"]'):
            job_details.append(one_job.xpath('.//text()').getall()[1].strip())

        item['published_date'] = publish_date
        item['city'] = cities
        item['job_address'] = job_address
        item['job_title'] = job_title
        item['employer_name'] = employer_name
        item['job_details'] = job_details
        yield item

    @staticmethod
    def get_job_title_class(response):
        return response.xpath('//h1[contains(@class, "uk-h2 uk-text-bold uk-margin-remove-top uk-margin-small-bottom ")]')[0].attrib['class']

    @staticmethod
    def get_employer_name(response):
        if response.xpath('.//h2[@class="uk-h4 uk-margin-remove"]/a'):
            return response.xpath('.//h2[@class="uk-h4 uk-margin-remove"]//text()').getall()[1].strip()
        return response.xpath('.//h2[@class="uk-h4 uk-margin-remove"]//text()').extract_first().strip()

    @staticmethod
    def get_city(address):
        def _hasDigit():
            for s in address.split(','):
                # If any of the characters in the string are digits:
                if any(c.isdigit() for c in s):
                    # Print the string and stop searching the list.
                    return True
            return False
        if _hasDigit():
            return [address.split(',')[0]]
        else:
            return address.split(',')

    @staticmethod
    def get_job_address(response):
        try:
            job_address = response.xpath('.//p[@class="uk-margin-remove-bottom uk-margin-small-top"]//text()').getall()[1].strip()
        except:
            job_address = response.xpath('.//div[@class="uk-margin-remove-bottom uk-margin-small-top"]//text()').getall()[1].strip()
        return job_address


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(InfostudSpider)
    process.start()