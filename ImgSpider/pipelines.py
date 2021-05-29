# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from scrapy.pipelines.images import ImagesPipeline
from . import settings

class ImgspiderPipeline(ImagesPipeline):
    # 此方法是在发送下载请求之前调用，其实此方法本身就是去发送下载请求
    def get_media_requests(self, item, info):
        # 调用原父类方法，发送下载请求并获取返回的结果(request的列表)
        request_objs = super().get_media_requests(item, info)
        # 给每个request对象带上meta属性传入hero_name、pf_name参数，并返回
        for request_obj, num in zip(request_objs, range(0, len(item['img_name']))):
            request_obj.meta['product_name'] = item['product_name']
            request_obj.meta['img_name'] = item['img_name'][num]
        return request_objs

    # 此方法是在图片将要被存储的时候调用，用来获取这个图片存储的全部路径
    def file_path(self, request, response=None, info=None):
        # 获取request的meta属性的hero_name作为文件夹名称
        product_name = request.meta.get('product_name')
        # 获取request的meta属性的pf_name并拼接作为文件名称
        image_name = request.meta.get('img_name') + '.jpg'
        # 获取IMAGES_STORE图片的默认地址并拼接
        image_store = settings.IMAGES_STORE
        hero_name_path = os.path.join(image_store, product_name)
        # 判断地址是否存在，不存则创建
        # if not os.path.exists(hero_name_path):
        #     os.makedirs(hero_name_path)
        # 拼接文件夹地址与图片名图片存储的全部路径并返回
        image_path = os.path.join(hero_name_path, image_name)
        return image_path
