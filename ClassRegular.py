# -*- coding: utf-8 -*-

import re
import logging
import requests
import os
import time
import random

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Regular(object):
    def __init__(self):
        self.GNAME_TO_GID = {
            'nmg': '649451770',
            'qwq': '980514385',
            'ys': '130516740',
            'gal': '605650659',
            }
        self.GID_TO_GNAME = {
            '649451770': 'nmg',
            '980514385': 'qwq',
            '130516740': 'ys',
            '605650659': 'gal',
        }
        
    # 将b站域名下的视频url提取av或bv号
    def biliVideoUrl(self, message):
        try:
            # logging.info(message)
            abcode = re.findall(r'video/([a-zA-Z0-9]+)', message)[0]
            # logging.info('abcode:{}'.format(abcode))
            return {
                'status': 0, 
                'data': abcode
                }
        except:
            logging.error('biliVideoUrl match failed(+_+)?')
            return {
                'status': -5,
                'data': 'biliVideoUrl match failed(+_+)?',
                'error': '{}'.format(message)
                }

    # 将b23.tv域名下的重定向地址返回
    def biliShortUrl(self, message):
        try:
            biliShortLinkUrl = re.findall(r'http(?:s)://b23.tv/[a-zA-Z0-9]+', message)[0]
            # logging.info('biliShortLinkUrl:{}'.format(biliShortLinkUrl))
            response = requests.get(biliShortLinkUrl, allow_redirects=False) #关闭重定向,取请求标头
            response = dict(response.headers)
            response = response['Location']
            logging.info('biliShortUrl Redirects:{}'.format(response))
            return {
                'status': 0, 
                'data': response
                }
        except:
            logging.error('biliShortUrl match failed(+_+)?')
            return {
                'status': -5,
                'data': 'biliShortUrl match failed(+_+)?'
                }
    
    # 动态url地址
    def biliDynamicId(self, message):
        try:
            patternBiliDynamicId = re.compile(r'(?:t|m).bilibili.com/(?:dynamic/)?([0-9]+)')
            BiliDynamicId = re.findall(patternBiliDynamicId, message)[0]
            return {
                'status': 0,
                'data': BiliDynamicId
                }
        except:
            logging.error('biliDynamic match failed(+_+)?')
            return {
                'status': -5,
                'data': 'biliDynamic match failed(+_+)'
                }

    def saveCQImageUrl(self, message, gid):
        try:
            urlList = re.findall(r'https://gchat.qpic.cn/gchatpic_new/(.*?/.*?)/0\?term=3',message)
            os.makedirs('./CQImageUrl/{}/'.format(gid), exist_ok=True)
            with open('./CQImageUrl/{}/{}.txt'.format(gid, time.strftime("%Y-%m", time.localtime(time.time()))), mode='a+', encoding='utf-8') as f:
                for url in urlList:
                    f.seek(0)
                    if f.read(1) != '':
                        f.seek(0)
                        count = False
                        for line in f:
                            if url[-32:] == line[-33:-1] and count == False:
                                logging.info('图片已存在')
                                count = True
                                break
                        if count == False:
                            f.seek(0,2)
                            f.write(url)
                            f.write('\n')
                    else:
                        f.write(url)
                        f.write('\n')
                return {
                    'status': 0,
                    'data': '保存成功'
                }
        except:
            logging.error('CQ图url匹配失败')
            return {
                'status': -5,
                'data': 'CQ图url匹配失败'
            }
    
    def getCQImageUrlInfo(self, gid=None, groupname=None):
        from itertools import (takewhile, repeat)
        buffer = 1024 * 1024
        if gid != None:
            if groupname != None:
                os.makedirs('./CQImageUrl/{}/'.format(self.GNAME_TO_GID[groupname]), exist_ok=True)
                imgFolderList = os.listdir('./CQImageUrl/{}/'.format(self.GNAME_TO_GID[groupname]))
                count = 0
                for imgfoldername in imgFolderList:
                    with open('./CQImageUrl/{}/{}'.format(self.GNAME_TO_GID[groupname], imgfoldername), encoding='utf-8') as f:
                        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                        count += sum(buf.count('\n') for buf in buf_gen)
                message = '群聊{}收录图片:'.format(groupname) + str(count) + '张'
                return {
                    'status': 0,
                    'count': count,
                    'data': message,
                }

            else:
                groupList = os.listdir('./CQImageUrl/')
                count = 0
                for i in groupList:
                    imgFolderList = os.listdir('./CQImageUrl/{}/'.format(i))
                    for imgfoldername in imgFolderList:
                        with open('./CQImageUrl/{}/{}'.format(i, imgfoldername), encoding='utf-8') as f:
                            buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                            count += sum(buf.count('\n') for buf in buf_gen)
                count += sum(buf.count('\n') for buf in buf_gen)
                message = '所有群收录图片:' + str(count) + '张'
                return {
                    'status': 0,
                    'count': count,
                    'data': message,
                }

        else:
            return {
                'status': -5,
                'data': '查询失败'
            }
    
    def getCQImage(self, gid, imgnum):
        CQImageList = os.listdir('./CQImageUrl/{}/'.format(gid))
        from itertools import (takewhile, repeat)
        buffer = 1024 * 1024
        imgDict = {}
        count = self.getCQImageUrlInfo(gid, self.GID_TO_GNAME[gid])['count']
        if count < int(imgnum):
            return {
                'status': -5,
                'data': '群{}图库数量不足'.format(self.GID_TO_GNAME[gid])
            }
        while len(imgDict) != int(imgnum) and count >= int(imgnum):
            imgList = []
            r = random.randint(0,len(CQImageList)-1)
            with open('./CQImageUrl/{}/{}'.format(gid, CQImageList[r]), 'r', encoding='utf-8') as f:
                buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
                x = random.randint(0,sum(buf.count('\n') for buf in buf_gen)-1)
                num = 0
                f.seek(0)
                line = f.readline()
                while line:
                    if num == x:
                        hashv = line.strip('\n')[-32:]
                        imgurl = 'https://gchat.qpic.cn/gchatpic_new/'+line.strip('\n')+'/0?term=3'
                        if hashv not in imgDict.keys():
                            logging.info(hashv)
                            this = f.tell()
                            logging.info(this)
                            path = './CQImageUrl/{}/{}'.format(gid, CQImageList[r])
                            imgList = [imgurl, path, this]
                            imgDict[hashv] = imgList
                            break
                        else:
                            break
                    else:
                        num += 1
                    line = f.readline()
        return {
                'status': 0,
                'data': imgDict
            }
        
    def getGroupInfo(self):
        os.makedirs('./CQImageUrl/', exist_ok=True)
        groupList = os.listdir('./CQImageUrl/')
        if groupList != []:
            # 详细信息
            m = '基本信息:\n'
            m += '总数: {}张\n'.format(self.getCQImageUrlInfo(True)['count'])
            for gid in groupList:
                if gid in self.GID_TO_GNAME.keys():
                    m += self.GID_TO_GNAME[gid]
                    m += ': '
                    m += str(self.getCQImageUrlInfo(gid, self.GID_TO_GNAME[gid])['count'])
                    m += '张\n'
            
            m += '''\n基本功能:
1.派蒙图库->获取全部群代号的图片总张数以及每个群的张数
2.派蒙图库#群代号->获取这个群的图片总数
3.消息中含有关键词 派蒙 图 即可获取图片
4.向上述消息中加入关键词 群代号可发指定群的图片
5.还能向消息中添加如 3张 这样的关键词获取指定数量的图片'''
            return {
                'status': 0,
                'data': m
            }
        else:
            return {
                'status': -5,
                'data': '没有群信息哦'
            }
        
    # def deleteImage(self, path, this):
    def deleteImage(self, path, hashv):
        try:
            # with open(path, 'r+', encoding='utf-8') as f:
            #     count = 0
            #     s = ''
            #     default_this = int(this)
            #     f.seek(default_this)
            #     while True:
            #         default_this -= 1
            #         if default_this < 0:
            #             break
            #         f.seek(default_this)
            #         x = f.read(1)
            #         if x == '\n' and count == 1:
            #             break
            #         elif x == '\n':
            #             s = x + s
            #             count += 1
            #         else:
            #             s = x + s

            f = open(path, 'r', encoding='utf-8')
            lines = f.readlines()
            print(lines)
            f.close()

            f = open(path, 'w', encoding='utf-8')
            for line in lines:
                if hashv not in line:
                    f.write(line)
            f.close()
            return {
                'status': 0,
                'data': '删除成功',
            }
        except:
            return {
                'status': -5,
                'data': '删除失败'
            }
    
    def new_words_save(self, word):
        with open('new_words.txt', 'a+', encoding='utf-8') as f:
            f.write(word)


if __name__ == '__main__':
    pass
    x = '&#91;&#91;QQ小程序&#93;哔哩哔哩&#93;请使用最新版本手机QQ 查看[CQ:json,data={"app":"com.tencent.miniapp_01"&#44;"desc":""&#44;"view":"view_8C8E89B49BE609866298ADDFF2DBABA4"&#44;"ver":"1.0.0.19"&#44;"prompt":"&#91;QQ小程序&#93;哔哩哔哩"&#44;"meta":{"detail_1":{"appid":"1109937557"&#44;"appType":0&#44;"title":"哔哩哔哩"&#44;"desc":"【科普速递】M1 Ultra真的只是两个M1 Max复制粘贴吗？UltraFusion技术详解"&#44;"icon":"https:\/\/miniapp.gtimg.cn\/public\/appicon\/51f90239b78a2e4994c11215f4c4ba15_200.jpg"&#44;"preview":"https:\/\/i2.hdslb.com\/bfs\/archive\/26ab17f035b51e37cc6af696dcc600bf5a6fd23f.jpg@500w_400h_1e_1c.webp"&#44;"url":"m.q.qq.com\/a\/s\/6c1aeb68437b7f5e751657f06103535d"&#44;"scene":0&#44;"host":{"uin":577430840&#44;"nick":"Jelly"}&#44;"shareTemplateId":"8C8E89B49BE609866298ADDFF2DBABA4"&#44;"shareTemplateData":{}&#44;"qqdocurl":"https:\/\/www.bilibili.com\/video\/BV1TY411V78p"&#44;"showLittleTail":""&#44;"gamePoints":""&#44;"gamePointsUrl":""}}&#44;"config":{"type":"normal"&#44;"width":0&#44;"height":0&#44;"forward":1&#44;"autoSize":0&#44;"ctime":1646824549&#44;"token":"4f35afcfb6b58f87f051d52e58df9a31"}}]'
    # message = '[CQ:reply,id=645016453][CQ:at,qq=2980293094] del'
    # m = re.findall(r'')
    # print(m)
    print(Regular().biliVideoUrl(x))
    # print(Regular().biliShortUrl('https://b23.tv/gVcQEc8'))