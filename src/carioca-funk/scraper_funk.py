import os
import json

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError

import settings as s
import utils as u

LANG_LOOKUP = {'1': 'portuguese', '2': 'english', '3': 'spanish'}

class FunkSpider(scrapy.Spider):
    name = 'funk'
    allowed_domains = ['www.vagalume.com.br']
    start_urls = ['https://www.vagalume.com.br/browse/style/funk-carioca.html']
    path_data = s.PATH_DATA
    # json should be the right format but I would have to write everything at once or open a single file multiple times
    path_singers = os.path.join(path_data, 'singers.txt')
    path_songs = os.path.join(path_data, 'songs.txt')
    path_popularity = os.path.join(path_data, 'popularity.txt')

    def parse_popularity(self, response):
        """
        Parses http response and extracts the year which the singer appeared
        In this page there is the popularity over time in a graph but I couldn't parse the svg path to get the data

        :param response: http response
        :returns: saves information in .txt file
        """
        query_year = '//ul[@id="popFacts"]//span[contains(., "A primeira vez")]/strong/text()'
        year_showup = response.xpath(query_year).extract_first()
        singer_name = response.css('h1.darkBG > a::text').extract_first()

        popularity = {'singer_name': singer_name,
                      'year': year_showup}

        with open(self.path_popularity, 'a+') as outfile:
            outfile.write(json.dumps(popularity) + '\n')

    def parse_songs(self, response):
        """
        Parses http response and extracts the music lyrics and details

        :param response: http response
        :returns: saves information in .txt file
        """
        query_name = '//div[@id="lyricContent"]/div[@class="col1-2-1"]/h1/text()'
        name = response.xpath(query_name).extract_first()
        lyrics = response.xpath('//div[@id="lyrics"]/text()').extract()
        music_details = json.loads(response.xpath('head/script[@id="vData"]/text()')
                                   .extract_first().replace('window.vData=', ''))
        music_details['language'] = LANG_LOOKUP.get(music_details['langID'])

        songs_info = {
            'song_name': name,
            'lyrics': lyrics,
            'details': music_details
        }

        with open(self.path_songs, 'a+') as outfile:
            outfile.write(json.dumps(songs_info) + '\n')

    def parse_singers(self, response):
        """
        Parses http response and extracts information about the singer
        such as: musics, photo, style

        :param response: http response
        :returns: saves information in .txt file
        """
        name = response.css('h1.darkBG > a::text').extract_first()

        query_top = '//ol[@id="topMusicList"]/li/div[@class="flexSpcBet"]/div[@class="lineColLeft"]/a/@href'
        top_musics = response.xpath(query_top).extract()
        top_musics = list(zip([i + 1 for i in range(0, len(top_musics))],
                              top_musics))
        all_styles = response.css('ul.subHeaderTags > li > a::text').extract()
        photo_url = response.xpath(
            '//div[@id="artHeaderImg"]//img/@src').extract_first()
        photo_url = response.urljoin(photo_url)

        query_all_musics = '//ol[@id="alfabetMusicList"]/li/div[@class="flexSpcBet"]/div[@class="lineColLeft"]/a/@href'
        all_musics = response.xpath(query_all_musics).extract()

        singer_info = {
            'singer_name': name,
            'singer_styles': all_styles,
            'photo_url': photo_url,
            'top_songs': top_musics,
            'song_names': all_musics
        }

        with open(self.path_singers, 'a+') as outfile:
            outfile.write(json.dumps(singer_info) + '\n')

        query_popularity = '//a[(@class="menuArtistLink") and (.="Popularidade")]/@href'
        url_popularity = response.xpath(query_popularity).extract_first()
        yield scrapy.Request(response.urljoin(url_popularity),
                             callback=self.parse_popularity,
                             errback=self.error)

        join_musics = list(set(all_musics + list(map(lambda x: x[1],
                                                     top_musics))))
        for url in join_musics:
            url = response.urljoin(url)
            yield scrapy.Request(response.urljoin(url),
                                 callback=self.parse_songs,
                                 errback=self.error)

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

    def parse(self, response):
        u.clean_folder(self.path_data)

        query_singers = '//div[@class="moreNamesContainer h16"]/ul/li/a/@href'
        singer_urls = response.xpath(query_singers).extract()

        for url in singer_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url,
                                 callback=self.parse_singers,
                                 errback=self.error)
