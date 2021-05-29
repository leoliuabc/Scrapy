from scrapy import cmdline

# 运行此文件代替命令行运行scrapy项目
cmdline.execute("scrapy crawl ImgSpider".split(" "))