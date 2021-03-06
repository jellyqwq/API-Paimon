# Paimon API  

## All standard status codes in this project  

| status code   | means                 |
|---------------|-----------------------|
|0|request success|
|-1|request failure|
|-2|missing request paramenter|
|-3|abcode error|
|-4|bili error|
|-5|failed to match|

## Project structure

- [ClassBili](/ClassBili.py)
    - [getHotWord](/ClassBili.py#L28)
    - [toBiliShortUrl](/ClassBili.py#L63)
    - [biliVideoInfo](/ClassBili.py#L87)
    - [getDynamicInfo](/ClassBili.py#L141)
- [ClassRegular](/ClassRegular.py)
    - [biliVideoUrl](/ClassRegular.py#L12)

## API documentation

- [/bili](/ClassBili.md)
    - [x] [/hotword](/ClassBili.md#gethotword) 获取b站热搜
    - [x] [/shortlink?url=](/ClassBili.md#toBiliShortUrl) 生成b站短链
    - [x] [/videoinfo?abcode=](/ClassBili.md#biliVideoInfo) 通过abcode获取视频信息
    - [x] [/dynamicinfo?id=](/ClassBili.md#getDynamicInfo) 通过动态id获取动态信息
- [/weibo](/ClassWeiBo.md)
    - [x] [/hotword](/ClassWeiBo.md#gethotword) 获取微博热搜
- [/parse](/README.md)
    <!-- - [x] [/geturl?message=](/README.md) 从消息中提取url -->
    - [x] [/abcode?message=](/README.md) 从字符串中提取视频abcode
    - [x] [/b23?message=](/README.md) 从字符串中提取b23.tv的链接并返回其重定向地址
    - [x] [/bdynamic?message=](/README.md) 从消息>message<中匹配出动态id
    - [x] [/cqimgurl?message=](/README.md) 从图片消息中提取图片url
    - [x] [/cqimginfo](/README.md) 获取当月保存图片张数

