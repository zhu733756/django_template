# -*- coding:utf-8 -*-
import os
from concurrent.futures import ThreadPoolExecutor
from sys import getsizeof
from datetime import datetime, timedelta
from PIL import Image
import requests
from lxml import etree
from io import BytesIO


class TestData(object):
    title = '习近平出席中缅建交70周年系列庆祝活动暨中缅文化旅游年启动仪式'
    publish_date = datetime(2020, 1, 18, 4, 22, 51)
    author = ''
    images = '\n'.join([
        'https://img-xhpfm.zhongguowangshi.com/News/202001/41e8c48c85e949d7a729dd4f2e97c8b4.jpg@1000w_1e_1c_80Q_1x.jpg',
        'https://img-xhpfm.zhongguowangshi.com/News/202001/7137eaa6fc284de49695fdaeeeb80772.jpg@1000w_1e_1c_80Q_1x.jpg',
        'https://img-xhpfm.zhongguowangshi.com/News/202001/cdd27dca1baf4bc9b975c62af6c09e3c.jpg@1000w_1e_1c_80Q_1x.jpg',
        'https://img-xhpfm.zhongguowangshi.com/News/202001/c9be4414b96c483bb5b2f86c858f7eb7.jpg@1000w_1e_1c_80Q_1x.jpg',
        'https://img-xhpfm.zhongguowangshi.com/News/202001/17f560ff5e444b5881d1de0f80eaeb1d.jpg@1000w_1e_1c_80Q_1x.jpg',
        'https://img-xhpfm.zhongguowangshi.com/News/202001/8be4d553fc7348d6a4c6a62a3ef48df8.jpg@1000w_1e_1c_80Q_1x.jpg'])
    content = '<p style="text-indent:2em;">\r\n\t<a href="https://img-xhpfm.zhongguowangshi.com/News/202001/41e8c48c85e949d7a729dd4f2e97c8b4.jpg" class="link-image" target="_blank"><img src="https://img-xhpfm.zhongguowangshi.com/News/202001/41e8c48c85e949d7a729dd4f2e97c8b4.jpg@1000w_1e_1c_80Q_1x.jpg" /></a> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span style="color:#337FE5;">↑当地时间1月17日晚，国家主席习近平在内比都第二国际会议中心出席中缅建交70周年庆祝活动暨中缅文化旅游年启动仪式。这是习近平和缅甸总统温敏共同按下按钮，正式启动中缅文化旅游年。新华社记者 鞠鹏 摄</span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<a href="https://img-xhpfm.zhongguowangshi.com/News/202001/7137eaa6fc284de49695fdaeeeb80772.jpg" class="link-image" target="_blank"><img src="https://img-xhpfm.zhongguowangshi.com/News/202001/7137eaa6fc284de49695fdaeeeb80772.jpg@1000w_1e_1c_80Q_1x.jpg" /></a> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span style="color:#337FE5;">↑当地时间1月17日晚，国家主席习近平在内比都第二国际会议中心出席中缅建交70周年庆祝活动暨中缅文化旅游年启动仪式。这是仪式开始前，习近平在缅方领导人陪同下，观看庆祝中缅建交70周年图片展。</span><span style="color:#337FE5;">新华社记者 黄敬文 摄</span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><a href="https://img-xhpfm.zhongguowangshi.com/News/202001/cdd27dca1baf4bc9b975c62af6c09e3c.jpg" class="link-image" target="_blank"><img src="https://img-xhpfm.zhongguowangshi.com/News/202001/cdd27dca1baf4bc9b975c62af6c09e3c.jpg@1000w_1e_1c_80Q_1x.jpg" /></a></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;">↑当地时间1月17日晚，国家主席习近平在内比都第二国际会议中心出席中缅建交70周年庆祝活动暨中缅文化旅游年启动仪式。这是习近平在仪式上致辞。</span><span style="color:#337FE5;">新华社记者 黄敬文 摄</span><br />\r\n</span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;"><a href="https://img-xhpfm.zhongguowangshi.com/News/202001/c9be4414b96c483bb5b2f86c858f7eb7.jpg" class="link-image" target="_blank"><img src="https://img-xhpfm.zhongguowangshi.com/News/202001/c9be4414b96c483bb5b2f86c858f7eb7.jpg@1000w_1e_1c_80Q_1x.jpg" /></a></span></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;">↑当地时间1月17日晚，国家主席习近平在内比都第二国际会议中心出席中缅建交70周年庆祝活动暨中缅文化旅游年启动仪式。这是习近平在仪式上致辞。新华社记者 刘彬 摄<br />\r\n</span></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;"><a href="https://img-xhpfm.zhongguowangshi.com/News/202001/17f560ff5e444b5881d1de0f80eaeb1d.jpg" class="link-image" target="_blank"><img src="https://img-xhpfm.zhongguowangshi.com/News/202001/17f560ff5e444b5881d1de0f80eaeb1d.jpg@1000w_1e_1c_80Q_1x.jpg" /></a></span></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;">↑当地时间1月17日晚，国家主席习近平在内比都第二国际会议中心出席中缅建交70周年庆祝活动暨中缅文化旅游年启动仪式。这是习近平在仪式上致辞。新华社记者 费茂华 摄<br />\r\n</span></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;"><a href="https://img-xhpfm.zhongguowangshi.com/News/202001/8be4d553fc7348d6a4c6a62a3ef48df8.jpg" class="link-image" target="_blank"><img src="https://img-xhpfm.zhongguowangshi.com/News/202001/8be4d553fc7348d6a4c6a62a3ef48df8.jpg@1000w_1e_1c_80Q_1x.jpg" /></a></span></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span><span style="color:#337FE5;">↑当地时间1月17日晚，国家主席习近平在内比都第二国际会议中心出席中缅建交70周年庆祝活动暨中缅文化旅游年启动仪式。这是习近平和缅甸总统温敏共同按下按钮，正式启动中缅文化旅游年。新华社记者 黄敬文 摄<br />\r\n</span></span> \r\n</p>\r\n<p style="text-indent:2em;">\r\n\t<span style="color:#000000;"><span style="color:#000000;">编辑：李瑜</span></span> \r\n</p>'
    article_type = 'MultimediaCIType'
    xml_file = 'XxhappC000029_20200118_XHMFN0N0A.xml'
    xml_content = ''


def genernate_xml(data):
    if data.xml_content:
        return data.xml_content
    else:
        params = {
            'title': data.title,
            'publish_date': data.publish_date,
            'author': data.author,
            'images': (data.images or "").split('\n'),
            'content': data.content,
            'article_type': data.article_type,
            'xml_file': data.xml_file,
        }
        xml = GenerateXmlStr(data=params)
        return xml.get_xml_content()


class XMLNamespaces(object):
    xmlns = 'http://www.cnml.org.cn/2005/CNMLSchema'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'


class GenerateXmlStr(object):

    def __init__(self, data):
        self.data = data
        self.file_number = 1
        self.media_id = 1
        xml_name = self.data.get('xml_file')
        self.xml_name = xml_name

    def get_calendar_time(self):
        # 获取格林威治时间
        #   "releasedate": "2020-02-07 13:57:00",
        date = self.data.get('publish_date') - timedelta(hours=8)
        return date.strftime('%Y-%m-%dT%H:%M:%S+08:00')

    def get_xml_content(self):
        CNML = etree.Element('CNML',
                             {etree.QName(XMLNamespaces.xsi,
                                          "schemaLocation"): 'http://www.cnml.org.cn/2005/CNMLSchema http://www.cnml.org.cn/2005/CNMLSchema/CNML_v1.020070208.xsd',
                              "schemaVersion": "",
                              "template": "",
                              "templateVersion": "", },
                             nsmap={None: 'http://www.cnml.org.cn/2005/CNMLSchema'}
                             )
        CNML.append(self.generate_envelop_element())
        CNML.append(self.generate_contentItems_element())
        CNML.append(self.generate_relation_element())
        xml_str = etree.tostring(CNML, encoding='utf-8', xml_declaration=True, pretty_print=True)
        return xml_str

    def generate_envelop_element(self):
        Envelop = etree.Element('Envelop')
        etree.SubElement(Envelop, 'TransferTime').text = self.get_calendar_time()
        Products = etree.SubElement(Envelop, 'Products')
        Product = etree.SubElement(Products, 'Product', productID="xhs")
        ProductName = etree.SubElement(Product, 'ProductName')
        etree.SubElement(ProductName, 'Name').text = '新华社客户端'
        return Envelop

    def generate_contentItems_element(self):
        Items = etree.Element('Items')
        Item = etree.SubElement(Items, 'Item')

        # 添加 标题
        MetaInfo = etree.SubElement(Item, 'MetaInfo')
        DescriptionMetaGroup = etree.SubElement(MetaInfo, 'DescriptionMetaGroup')
        Titles = etree.SubElement(DescriptionMetaGroup, 'Titles')
        HeadLine = etree.SubElement(Titles, 'HeadLine')
        HeadLine.text = etree.CDATA(self.data.get('title'))
        # 添加作者
        Creators = etree.SubElement(DescriptionMetaGroup, 'Creators')
        Name = etree.SubElement(Creators, 'Name')
        FullName = etree.SubElement(Name, 'FullName')
        FullName.text = self.data.get('author')

        # 图片 需要替换正文的图片url
        images = self.data.get('images')
        images_info = self.handle_image(images)

        # 添加 Contents
        Contents = etree.SubElement(Item, 'Contents')
        # 添加 正文
        if self.data.get('article_type') == 'MultimediaCIType':
            ContentItem = etree.SubElement(Contents, 'ContentItem', id='c01',
                                           attrib={etree.QName(XMLNamespaces.xsi, "type"): 'MultimediaCIType'})
        else:
            ContentItem = etree.SubElement(Contents, 'ContentItem', id='c01',
                                           attrib={etree.QName(XMLNamespaces.xsi, "type"): 'TextCIType'})
        ContentMetaInfo = etree.SubElement(ContentItem, 'MetaInfo')
        ContentCharacteristicMetaGroup = etree.SubElement(ContentMetaInfo, 'CharacteristicMetaGroup')
        ContentDataContent = etree.SubElement(ContentItem, 'DataContent')
        content = self.data.get('content', '')
        for i in images_info:
            content = content.replace(i.get('img_url', ''), i.get('file_name', ''))
        ContentDataContent.text = etree.CDATA(content)

        # 图片
        for image in images_info:
            self.media_id += 1
            ImageItem = etree.SubElement(Contents, 'ContentItem',
                                         attrib={etree.QName(XMLNamespaces.xsi, "type"): 'ImageCIType',
                                                 'id': 'c{:0>2d}'.format(self.media_id),
                                                 'href': image.get('file_name')})
            ImageMetaInfo = etree.SubElement(ImageItem, 'MetaInfo')
            ImageCharacteristicMetaGroup = etree.SubElement(ImageMetaInfo, 'CharacteristicMetaGroup')
            SizeInBytes = etree.SubElement(ImageCharacteristicMetaGroup, 'SizeInBytes')
            SizeInBytes.text = image.get('SizeInBytes', '')
            PixelWidth = etree.SubElement(ImageCharacteristicMetaGroup, 'PixelWidth')
            PixelWidth.text = image.get('PixelWidth', '')
            PixelHeight = etree.SubElement(ImageCharacteristicMetaGroup, 'PixelHeight')
            PixelHeight.text = image.get('PixelHeight', '')
        return Items

    def generate_relation_element(self):
        Relations = etree.Element('Relations')

        # hasEmbeding
        Relation = etree.SubElement(Relations, 'Relation', name="hasEmbedding")
        Source = etree.SubElement(Relation, 'Source')
        SourceRole = etree.SubElement(Source, 'Role')
        SourceRole.set('xpath', 'ContentItem[1]')
        Target = etree.SubElement(Relation, 'Target')
        RoleSet = etree.SubElement(Target, 'RoleSet')
        for i in range(2, self.media_id):
            etree.SubElement(RoleSet, 'Role', xpath="ContentItem[{}]".format(i))
        return Relations

    def get_cnml_file_name(self, file_type):
        # 文件名称可能需要预先定义
        file_name = self.xml_name[:-4] + 'A{:0>3d}'.format(self.file_number) + '.' + file_type.lower()
        self.file_number += 1
        return file_name

    def handle_image(self, images):
        images = [url for url in images if url.strip() != '']
        images_info = []
        if len(images):
            executor = ThreadPoolExecutor(max_workers=4)
            for result in executor.map(self._thread_down_image, images):
                images_info.append(result)
            return images_info
        return images_info

    def _thread_down_image(self, url):
        headers = {'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'}
        resp = requests.get(url=url, headers=headers, timeout=60)
        img = Image.open(BytesIO(resp.content))
        PixelWidth, PixelHeight = img.size
        SizeInBytes = getsizeof(resp.content)
        file_name = self.get_cnml_file_name(file_type=img.format)
        data = {'img_url': url,
                'PixelWidth': str(PixelWidth),
                'PixelHeight': str(PixelHeight),
                'SizeInBytes': str(SizeInBytes),
                'file_name': file_name
                }
        return data


if __name__ == '__main__':
    xml_str = genernate_xml(TestData)
    print(xml_str)
