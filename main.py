# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


# -*- coding: utf-8 -*-
# time: 2019-03-14
# place: Xinbeiqiao, Beijing
import time,requests
import json as js
import base64,hashlib


# 上传文件并进行base64位编码

def xunfeiOCR():
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    outfile:    输出文件
    """

    # from urllib import parse
    # 印刷文字识别 webapi 接口地址
    # URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
    URL = "https://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"  # 手写体识别12.11过期
    # 应用ID (必须为webapi类型应用，并印刷文字识别服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
    APPID = "5f436f46"
    # 接口密钥(webapi类型应用开通印刷文字识别服务后，控制台--我的应用---印刷文字识别---服务的apikey)
    API_KEY = "6b45a944ea1c599b343403992ef7879e"

    def getHeader():
        #  当前时间戳
        curTime = str(int(time.time()))
        #  支持语言类型和是否开启位置定位(默认否)
        param = {"language": "cn|en", "location": "false"}
        param = js.dumps(param)
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    # 上传文件并进行base64位编码
    with open(r'D:\Pythonstore\中学\微信截图_20210922104750.png', 'rb') as f:
        f1 = f.read()

    f1_base64 = str(base64.b64encode(f1), 'utf-8')

    data = {
        'image': f1_base64
    }
    try:
        r = requests.post(URL, data=data, headers=getHeader())
        result = js.loads(str(r.content, 'utf-8'))
    except:
        time.sleep(5)
        r = requests.post(URL, data=data, headers=getHeader())
        result = js.loads(str(r.content, 'utf-8'))
    # 错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)

    text_list = []
    # text = self.reader.readtext(picfile, detail=0)
    # text = text[0]
    if result['data']['block'][0]['line']:
        text = result['data']['block'][0]['line'][0]['word'][0]['content']

        print(text)


xunfeiOCR()
#baiduOCR(f1)
