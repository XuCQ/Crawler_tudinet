# Crawler_tudinet

- 数据爬取
- 目标：www.tudinet.com
- 代码作用
  - crawler.py 爬取主函数
    - 数据获取
    - 地址解析
  - crawl_funs.py：爬虫辅助功能包（杂七杂八，有些是其他项目的，并没用到）
  - AgainCrawler.py：反爬虫
    - 判断是否为爬虫
    - 验证码对抗
      - 验证码截图
      - 验证码输入（目前为人工，OCR未添加（忙+穷+菜））
      - cookies获取并更新