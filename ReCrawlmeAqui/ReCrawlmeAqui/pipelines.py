# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class RecrawlmeaquiPipeline(object):
    def process_item(self, item, spider):
        # Save item as a pickled file with a MOE name.chan

        return item