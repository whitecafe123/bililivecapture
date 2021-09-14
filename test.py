import urllib.parse
import urllib.request

import time
import gzip
import io
import json
import os


# https://js.live-play.acgvideo.com/live-js/750661/live_4505367_8136424.flv?wsSecret=4aae142722bed050a1ea1338e08444b9&wsTime=1552585763&trid=c337cb1c86dc4474aa5993b2929a578e&sig=no&platform=web&pSession=Y36S0hJG-BcS7-4Y3K-eS4p-f7KEBp9YJYFJ
# https://js.live-play.acgvideo.com/live-js/902508/live_4505367_8136424.flv?wsSecret=f7f9eb1febe32c0f2160c7f8d997bf97&wsTime=1552589774&trid=5447a61f9f2a4d9bb643b42b9cd9f5bb&sig=no&platform=web&pSession=dwQ3pzN9-hWFi-4BYn-kTKB-fpc3ynk047R2
# https://js.live-play.acgvideo.com/live-js/827890/live_4505367_8136424.flv?wsSecret=f6cf3c2fc493c1479d4ae3cfe0d9fecf&wsTime=1552590031&trid=61f3793bcebb43b0a742f84b335ee01d&sig=no&platform=web&pSession=TfBdm0Wf-RNH9-4DbN-jb70-hJGkFYCG7r7k
# https://js.live-play.acgvideo.com/live-js/900307/live_4505367_8136424.flv?wsSecret=fa921184c858a96aac13f06b16d6c5b7&wsTime=1552590082&trid=f561bf877bc942988be8b16659587c5f&sig=no&platform=web&pSession=5bMjG3AG-0D6B-47MG-Ych6-2YGPxyh8F2f2
# https://js.live-play.acgvideo.com/live-js/295546/live_4505367_8136424.flv?wsSecret=a432c442ee4b9f83f116699b2ca44ac8&wsTime=1552613629&trid=b9f60735196042b891b67751136cb8f2&sig=no&platform=web&pSession=a49e8RJC-w1hy-4F3A-r3Jd-0KPdSmA5psim
# https://js.live-play.acgvideo.com/live-js/823077/live_4505367_8136424.flv?wsSecret=b2306917eae0579d8cdcc8a8a008ab33&wsTime=1552614065&trid=70607ca117ef4072a09e18aed1b89834&sig=no&platform=web&pSession=yMnXAAeC-Xfxz-47sW-Pwe0-a2tBWC0YjwPM
# https://js.live-play.acgvideo.com/live-js/466568/live_4505367_8136424.flv?wsSecret=b1f06bd6daebcfe9771b6645f6a293f7&wsTime=1552615490&trid=7deb978486b04ffa8a48c6ebe1b3283f&sig=no&platform=web&pSession=2ZK5Ajxd-QAmD-4taT-8KtC-jnCTx9225NeS
# https://js.live-play.acgvideo.com/live-js/217685/live_4505367_8136424.flv?wsSecret=de661825a0099ef0a6c9c68d9ad4e2ba&wsTime=1552615618&trid=110b3a4a74104b9088372d1b2ab8060e&sig=no&platform=web&pSession=pnSANHfM-6EzF-4bmn-WyZ4-Ekz49MscpGGN
# https://js.live-play.acgvideo.com/live-js/101924/live_4505367_8136424.flv?wsSecret=dcc87a6ae326ccd9b5f9958d49a6607c&wsTime=1552615640&trid=51cf654607604da3b61e79d0cfa525ab&sig=no&platform=web&pSession=0D1DH60J-GQh5-4SZ8-B3aT-efH5dCBp6Y3m
# https://js.live-play.acgvideo.com/live-js/818303/live_4505367_8136424.flv?wsSecret=cd792cb3c041bb65ef14fb05157741c9&wsTime=1552615834&trid=08c8d37d2c8145f18ead898339e28940&sig=no&platform=web&pSession=c8kX8m8E-kG1f-414x-RAKd-hFCfJDPh2s0d
# https://js.live-play.acgvideo.com/live-js/517521/live_4505367_8136424.flv?wsSecret=cffb19f43bb349ef89881b7dd81ddf06&wsTime=1552615897&trid=22db4826b12d4c59a6b1060d4794961f&sig=no&platform=web&pSession=YhFik8xc-JzfH-49aR-x2Xy-s8acF4KH1AJn

video_file_size_end = 354856  # end in 7 mb
block_size = 1024
capture_loop_sleep = 30

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) Gecko/20100101 Firefox/65.0",
    "Cookie": "buvid3=41E78D7E-7E8C-4774-A10444c1f946fd1145094889866e50192b",
    "Host": "live.bilibili.com",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": r"text/html,application/xhtml+xml;q=0.9,image/webp,*/*;q=0.8",
}


def CaptureVideo(address):
    response = urllib.request.urlopen(address)
    filename = time.strftime("video/%Y%m%d%H%M%S", time.localtime())+".avi"
    f = open(filename, 'wb')
    video_file_size_start = 0

    while True:
        try:
            buffer = response.read(block_size)
            if not buffer:
                break
            video_file_size_start += len(buffer)
            if video_file_size_start > video_file_size_end:
                break
            f.write(buffer)


        except Exception as e:
            print(e)
    f.close()
    return filename


def decodeImage(filename):
    timestr = time.strftime("%Y%m%d%H%M%S", time.localtime())
    os.system("ffmpeg -i "+filename+" -f image2 -vf fps=fps=1 video/"+timestr+"_%d.png")
    # videoReader = cv2.VideoCapture(filename)
    # try:
    #     gotImage, image = videoReader.read()
    #     if (gotImage):
    #         cv2.imwrite("video/%sFrame%d.jpg" %(time.strftime("%Y%m%d%H%M%S", time.localtime()), 1), image)
    #
    # except Exception as e:
    #     print(e)


def searchAndPrint(resstr, n):
    laste = 0
    str1 = r"<script>window.__NEPTUNE_IS_MY_WAIFU__="
    str2 = r"</script>"
    results = []
    for i in range(n):
        try:
            s = resstr.index(str1, laste)
        except:
            break

        try:
            e = resstr.index(str2, s)
            laste = e
        except:
            e = len(resstr)
            break

        result = resstr[s+len(str1):e]
        result = result.replace("\\\\", "\\")
        # print(result)
        results.append(result)
    return results


def parseWeb(url):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    # try:
    buffer = response.read()
    resstr = ""
    Enc = response.info()["Content-Encoding"] == "gzip" or response.info()["content-encoding"] == "gzip"
    if Enc:
        ydata = io.BytesIO(buffer)
        ygz = gzip.GzipFile(fileobj=ydata)
        yread = ygz.read()
        ygz.close()
        resstr = yread.decode('utf8', 'ignore')
    else:
        resstr = buffer.decode('utf8', 'ignore')

    # print(resstr)
    jsons = searchAndPrint(resstr, 3)
    print(jsons)
    results = []
    if jsons is not None and len(jsons) > 0:
        jsonObj = json.loads(jsons[0])
        for item in jsonObj["playUrlRes"]["data"]["durl"]:
            results.append(item["url"])

    # except Exception as e:
    #     print(e)
    return results


def mainLoop():
    try:
        # 获取直播间首页，解析得到视频流地址
        urls = parseWeb(r"http://live.bilibili.com/1092")
        addr = urls[0]
        print(addr)
        # 获取视频片段，保存avi文件
        file = CaptureVideo(addr)
        # 获取avi的第一帧图像保存jpg
        decodeImage(file)
        # 干掉avi
        os.remove(file)
    except Exception as e:
        print("error in Mainloop:", e)


if __name__ == '__main__':
    while True:
        mainLoop()
        time.sleep(capture_loop_sleep)

