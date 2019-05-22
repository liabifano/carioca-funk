import os
import json

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError

import settings as s
import utils as u


VALID_STYLES = ['axe', 'bossa-nova', 'forro', 'funk-carioca',
                'hard-rock', 'gospel', 'rock', 'rap', 'reggae', 'reggaeton',
                'samba', 'sertanejo', 'hip-hop', 'infantil', 'pagode', 'pop']


class VagaSpider(scrapy.Spider):
    name = 'vaga'
    allowed_domains = ['https://www.vagalume.com.br']
    start_urls = ['https://www.vagalume.com.br/browse/style/']
    path_data = os.path.join(s.PATH_DATA, 'all')
    path_singers = os.path.join(path_data, 'singers.txt')
    path_songs = os.path.join(path_data, 'songs.txt')

    def error(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


    def parse_songs(self, response):
        return


    def parse_singer(self, response):
        query = '//ol[@id="topMusicList"]/li//div[@class="lineColLeft"]/a/@href'
        songs_urls = response.xpath(query).extract()
        songs_urls = [response.urljoin(r) for r in songs_urls]

        n_songs = len(songs_urls)

        if n_songs==25:
            return


    def parse_singers(self, response):
        print('oi')
        query = '//div[@class="moreNamesContainer h16"]/ul/li/a/@href'
        singer_urls = response.xpath(query).extract()
        singer_urls = [response.urljoin(r) for r in singer_urls]

        import pdb;pdb.set_trace();

        return url

    def parse(self, response):
        u.clean_folder(self.path_data)

        query_styles = '//ul[@class="xsList3 xsmList4 smList5 mdList5 gridList flexSpcStart"]/li/a/@href'
        style_urls = response.xpath(query_styles).extract()

        for url in style_urls:
            if url.split('/')[-1].split('.')[0] in VALID_STYLES:
                url = response.urljoin(url)
                yield scrapy.Request(url,
                                     callback=self.parse_singers,
                                     errback=self.error)


