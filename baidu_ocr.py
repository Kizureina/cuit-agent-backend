#!/usr/bin/python
# -*- coding: utf-8 -*-
from aip import AipOcr
from aip import AipImageClassify

'''
百度云:https://console.bce.baidu.com/
接口说明:http://ai.baidu.com/ai-doc/OCR/3k3h7yeqa
'''

APP_ID = '32310457'
API_KEY = '6YZjabqXPVz3IpplymQ9ujHz'
SECRET_KEY = 'bDjlMGXWGs2nAtIBCu5k6U9LPk7Cr1IP'

# 文字识别
class word:
    def __init__(self, filePath='', options='', url='', idCardSide='front'):
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        # 图片完整URL，URL长度不超过1024字节，URL对应的图片base64编码后大小不超过4M，
        # 最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式，当image字段存在时url字段失效
        self.url = url
        # 本地图像数据，base64编码，要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式
        self.image = ''
        # 可选参数
        self.options = options
        self.idCardSide = idCardSide
        if filePath:
            # 读取图片
            with open(filePath, 'rb') as fp:
                self.image = fp.read()

    def General(self):
        """ 调用通用文字识别, 50000次/天免费 """
        return self.client.basicGeneral(self.image, self.options)  # 还可以使用身份证驾驶证模板，直接得到字典对应所需字段

    def GeneralUrl(self):
        """ 调用通用文字识别, 图片参数为远程url图片 500次/天免费 """
        return self.client.basicGeneralUrl(self.url, self.options)

    def GeneralLocation(self):
        """ 调用通用文字识别（含位置信息版）, 图片参数为本地图片 500次/天免费 """
        return self.client.general(self.url, self.options)

    def GeneralUrlLocation(self):
        """ 调用通用文字识别, 图片参数为远程url图片 500次/天免费 """
        return self.client.generalUrl(self.url, self.options)

    def Accurate(self):
        """ 调用通用文字识别（高精度版） 500次/天免费 """
        return self.client.basicAccurate(self.image, self.options)

    def AccurateLocation(self):
        """ 调用通用文字识别（含位置高精度版） 50次/天免费 """
        return self.client.accurate(self.image, self.options)

    def EnhancedGeneral(self):
        """ 调用通用文字识别（含生僻字版）, 图片参数为本地图片 """
        return self.client.enhancedGeneral(self.image, self.options)

    def EnhancedGeneralUrl(self):
        """ 调用通用文字识别（含生僻字版）, 图片参数为远程url图片 """
        return self.client.enhancedGeneralUrl(self.image, self.options)

    def Idcard(self):
        """ 调用身份证识别, 图片参数为本地图片 front：身份证含照片的一面；back：身份证带国徽的一面 """
        return self.client.idcard(self.image, self.idCardSide, self.options)

    def Bankcard(self):
        """ 调用银行卡识别 """
        return self.client.bankcard(self.image)

    def DrivingLicense(self):
        """ 调用驾驶证识别 """
        return self.client.drivingLicense(self.image, self.options)

    def VehicleLicense(self):
        """ 调用行驶证识别 """
        return self.client.vehicleLicense(self.image, self.options)

    def LicensePlate(self):
        """ 调用车牌识别 """
        return self.client.licensePlate(self.image, self.options)

    def BusinessLicense(self):
        """ 调用营业执照识别 """
        return self.client.businessLicense(self.image, self.options)

    def Receipt(self):
        """ 调用通用票据识别 """
        return self.client.idcard(self.image, self.options)

# 图像识别
class image:
    def __init__(self, filePath='', options='', url=''):
        self.client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
        # 图片完整URL，URL长度不超过1024字节，URL对应的图片base64编码后大小不超过4M，
        # 最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式，当image字段存在时url字段失效
        self.url = url
        # 本地图像数据，base64编码，要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式
        self.image = ''
        # 可选参数
        self.options = options
        if filePath:
            # 读取图片
            with open(filePath, 'rb') as fp:
                self.image = fp.read()

    def Recognition(self):
        """ 调用通用物体识别 500次/天免费 """
        return self.client.advancedGeneral(self.image, self.options)
