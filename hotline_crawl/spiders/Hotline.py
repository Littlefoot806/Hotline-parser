# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from user_agent import generate_user_agent
from time import sleep
import logging
import csv
from random import randint


class HotlineSpider(scrapy.Spider):
    name = 'Hotline'
    allowed_domains = ['hotline.ua/']
    start_urls = ['...'] # 
    
    def parse(self, response):

        with open("1k.txt") as file:
            list_of_links = [row.strip() for row in file]

        for link in list_of_links:
            yield Request( url = link, callback=self.parse_page, 
                            headers={'User-Agent' : generate_user_agent(), 
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en',
                                'Upgrade-Insecure-Requests':1},
                            dont_filter=True)
    
    def parse_page(self, response):
        # captcha = response.xpath('//body/div/div[@class = "g-recaptcha"]').extract()

        f = open('errorUrls.txt', 'a')
        title = response.xpath('//h1/text()').extract_first()
        if title is None:
            f.write(response.url + '\n')
            logging.info('sleeping 20')
            sleep(20)
        title = title.strip()

        foto = response.xpath('//div[@class = "cell-list"]//img/@src').extract_first()
        if foto is None:
            f.write(response.url + '\n')
 
        desc1 = response.xpath('//div[@class = "app-nav-scroll"]//p/text()').extract_first()
        desc2 = response.xpath('//div[@class = "app-nav-scroll"]//p/span[1]/text()').extract_first()
        if desc2 is not None:
            description = desc1 + desc2
        else:
            description = desc1
            if description is None:
                f.write(response.url + '\n')

        proizvoditel = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Производ")]/..//p/a/text()').extract_first()
        if proizvoditel is None:
            f.write(response.url + '\n')
  
        type_shyni = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Тип")]/..//p/a/text()').extract_first()
        if type_shyni is None:
            type_shyni = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Тип")]/..//p/text()').extract_first()
        if type_shyni is None:
            f.write(response.url + '\n')
        type_shyni = type_shyni.strip()
 
        naznachenie = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Назначе")]/..//p/text()').extract_first()
        if naznachenie is None:
            f.write(response.url + '\n')
        naznachenie = naznachenie.strip()

        konstruction_shyni = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Конструкция")]/..//p/text()').extract_first()
        if konstruction_shyni is None:
            f.write(response.url + '\n')
        konstruction_shyni = konstruction_shyni.strip()

        shyrina_profilya_mm = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Ширина")]/..//p/text()').extract_first()
        if shyrina_profilya_mm is None:
            f.write(response.url + '\n')
        shyrina_profilya_mm = shyrina_profilya_mm.strip()
 
        vysota_profile_v_percent =  response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Высота")]/..//p/text()').extract_first()
        if vysota_profile_v_percent is None:
            f.write(response.url + '\n')
        vysota_profile_v_percent = vysota_profile_v_percent.strip()

        vnutreniy_diametr_v_duim = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Внутренний")]/..//p/text()').extract_first()
        if vnutreniy_diametr_v_duim is None:
            f.write(response.url + '\n')
        vnutreniy_diametr_v_duim = vnutreniy_diametr_v_duim.strip()
    
        gruzopodemnost_v_kg = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Грузоподъемность")]/..//p/text()').extract_first()
        if gruzopodemnost_v_kg is None:
            f.write(response.url + '\n')
        gruzopodemnost_v_kg = gruzopodemnost_v_kg.strip()
    
        max_speed_v_km_in_hour = response.xpath('//div[@class = "table-type-1"]//div[contains(text(), "Скорость")]/..//p/text()').extract_first()
        if max_speed_v_km_in_hour is None:
            f.write(response.url + '\n')
        max_speed_v_km_in_hour = max_speed_v_km_in_hour.strip()
   
        review1 = response.xpath('(//div[@class = "viewbox"]//div[@class = "row text"])[1]//following-sibling::*/p/text()').extract()
        review1 = "\n".join(review1)
        review2 = response.xpath('(//div[@class = "viewbox"]//div[@class = "row text"])[2]//following-sibling::*/p/text()').extract()
        review2 = "\n".join(review2)
        review3 = response.xpath('(//div[@class = "viewbox"]//div[@class = "row text"])[3]//following-sibling::*/p/text()').extract()
        review3 = "\n".join(review3)

        f.close()

        yield {
            "URL_to_item" : response.url,
            "Название" : title,
            "Фото" : foto,
            "Описание" : description,
            "Производитель" : proizvoditel,
            "Тип" : type_shyni,
            "Назначение" : naznachenie,
            "Конструкция шины" : konstruction_shyni,
            "Ширина профиля шины, мм" : shyrina_profilya_mm,
            "Высота профиля шины в процентах к ширине покрышки" : vysota_profile_v_percent ,
            "Внутренний диаметр покрышки, дюймы" : vnutreniy_diametr_v_duim,
            "Грузоподъемность, кг" : gruzopodemnost_v_kg,
            "Скорость максимальная, км/ч" : max_speed_v_km_in_hour,
            "Отзыв 1" : review1,
            "Отзыв 2" : review2,
            "Отзыв 3" : review3,
        }