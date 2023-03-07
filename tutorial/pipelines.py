# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tutorial.utils import getpdf_content
from scrapy.pipelines.files import FilesPipeline

class TutorialPipeline:
    def process_item(self, item, spider):
        url = item['url']
        content = item['pdf']
        print(url)
        c = getpdf_content(content)
        if c:
            with open('url.txt','a',encoding='utf-8') as f:
                f.write(url+'\t'+str(c)+'\n')
        
        return item
