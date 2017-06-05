from datetime import datetime


# the class is the item pipeline that yield the item of the crawler
class CrawlerPipeline(object):

    # add two properties to items
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
