# -*- coding:utf-8 -*-
# author:Changing Xu
# file:Crawler_tudinet-crawler
# datetime:2019/12/6 9:56
# software: PyCharm
from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent
import re
from crawl_funs import getHtml_text, judgenet, loadinfo
import http.cookiejar as cj  # cookie
import random
import numpy as np
from reCoordinate.baidumap import xBaiduMap
from reCoordinate.coordTransform_utils import bd09_to_wgs84


URL_PAGE = 'https://www.tudinet.com/market-84-0-0-0/list-pg{page}.html'
LIST_VIEW_URL = []
re_bd_x = r'var bd_x =(.*?);'
re_bd_y = r'var bd_y =(.*?);'
ROW_Name = ['名称', '状态', '所在地', '规划用途', '总面积', '建设用地面积', '规划建筑面积', '容积率', '商业比例', '建筑密度', '出让年限', '位置', '四至', '交易状况', '竞得方', '起始日期', '截至日期', '成交日期', '交易地点',
            '起始价', '成交价', '土地单价', '溢价率', '推出楼面价', '成交楼面价', '保证金', '最小加价幅度', '公告日期', '公告编号', '备注', '咨询电话', 'bd_x', 'bd_y', '页面坐标', 'lng_wgs84', 'lat_wgs84']
CITY = '常州'

if (judgenet() == "ok"):
    for page in range(100):  # 页码页面爬取 获得详情页链接
        try:
            list_pg_html = BeautifulSoup(getHtml_text(URL_PAGE.format(page=page + 1)), 'html5lib')
        except Exception as e:
            print('ERROE: page {0} error : {1}'.format(page, e))
            continue
        try:
            list_view_dt = list_pg_html.find_all('dt')
            for info_view in list_view_dt:
                url_view = info_view.find('a')['href']
                LIST_VIEW_URL.append(url_view)
            print('Page {0} view_url load'.format(page))
            time.sleep(random.random() * 3)
        except Exception as e:
            print('ERROE: page {0} list_view_info error : {1}'.format(page, e))
            continue
    # print(LIST_VIEW_URL)
    # np.save('CZ_view_url', LIST_VIEW_URL)
    # LIST_VIEW_URL = np.load('CZ_view_url.npy')
    nGetPage = 0
    for url_view in LIST_VIEW_URL:  # 获取详情页
        view_info = dict(zip(ROW_Name, ['' for _ in ROW_Name]))
        try:
            view_html = BeautifulSoup(getHtml_text(url_view), 'html5lib')
            detail_info = view_html.find(class_='hh-box-b hh-detail-info')
            hh_name, hh_state = view_html.find(class_='hh-name').text.split('\xa0\xa0\xa0\xa0')
            view_info['名称'] = hh_name
            view_info['状态'] = hh_state
            list_hh_sort_text = view_html.find_all(class_='hh-sort-text')
            for info_hh_sort_text in list_hh_sort_text:
                list_hh_sort_text_li = info_hh_sort_text.find_all('li')
                for info_hh_sort_text_li in list_hh_sort_text_li:
                    name_hh_sort_text_li = info_hh_sort_text_li.find('b').text.replace('：', '')
                    content_hh_sort_text_li = info_hh_sort_text_li.find('span').text.replace('\n', '')
                    if name_hh_sort_text_li in ROW_Name:
                        view_info[name_hh_sort_text_li] = content_hh_sort_text_li.replace(' ', '')
            # 位置信息
            try:
                getXYJudge = True
                re_bd_x_find = re.findall(re_bd_x, view_html.text)
                re_bd_y_find = re.findall(re_bd_y, view_html.text)
                if len(re_bd_x_find) == 1 and len(re_bd_y_find) == 1:
                    view_info['bd_x'] = re_bd_x_find[0]
                    view_info['bd_y'] = re_bd_y_find[0]
                    view_info['页面坐标'] = True
                else:
                    bm = xBaiduMap()
                    newcoordinate = bm.getLocation(view_info['所在地'].replace('>', ' ') + view_info['位置'].replace('，', ' '), CITY)
                    if newcoordinate.__str__() == "None":
                        getXYJudge = False
                    else:
                        view_info['bd_x'] = newcoordinate[1]
                        view_info['bd_y'] = newcoordinate[0]
                        view_info['页面坐标'] = False
                if getXYJudge:
                    view_info['lng_wgs84'], view_info['lat_wgs84'] = bd09_to_wgs84(float(view_info['bd_x']), float(view_info['bd_y']))
            except Exception as e:
                print('coordinate error ', e, url_view)
        except Exception as e:
            print('GET HTML ERROR {0} '.format(url_view), e)
            continue
        loadinfo(view_info, 'projinfo', nGetPage)
        nGetPage += 1
        print(view_info['名称'], 'Done\t', nGetPage)
        time.sleep(random.random() * 3)
