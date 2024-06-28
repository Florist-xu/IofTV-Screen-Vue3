import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Origin": "https://y.qq.com",
        "Referer": "https://y.qq.com/",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "'Windows'",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Priority": "u=1, i",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"'
    }


@app.route('/get_diss_by_tag', methods=['GET'])
def get_diss_by_tag():
    params = request.args.to_dict()  # 获取请求参数并转换成字典

    # 确保正确转换参数类型
    params_a = {
        'picmid': int(params.get('picmid', 1)),
        'rnd': random.random(),  # 每次请求生成随机数
        'g_tk': int(params.get('g_tk', 732560869)),
        'loginUin': int(params.get('loginUin', 0)),
        'hostUin': int(params.get('hostUin', 0)),
        'format': params.get('format', 'json'),
        'inCharset': params.get('inCharset', 'utf8'),
        'outCharset': params.get('outCharset', 'utf-8'),
        'notice': int(params.get('notice', 0)),
        'platform': params.get('platform', 'yqq.json'),
        'needNewCode': int(params.get('needNewCode', 0)),
        'categoryId': int(params.get('categoryId', 10000000)),
        'sortId': int(params.get('sortId', 5)),
        'sin': int(params.get('sin')),
        'ein': int(params.get('ein'))
    }
    try:
        response = requests.get(
            "https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg", params=params_a, headers=headers)
        response.raise_for_status()

        data = response.json()
        return jsonify(data['data']['list'])
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return jsonify({"error": "HTTP Error", "message": str(errh)}), 500
    
# 获取歌单
@app.route('/get_play_list', methods=['GET'])
def get_play_list():
    params = request.args.to_dict() 
    # https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg
    params_a={
        "type": 1,
        "json": 1,
        "utf8": 1,
        "onlysong": 0,
        "nosign":1,
        "disstid": params.get('disstid'),
        "g_tk": 5831,
        "loginUin": 0,
        "hostUin": 0,
        "format": "json",
        "inCharset": "GB2312",
        "outCharset": "utf-8",
        "notice": 0,
        "platform": "yqq",
        "needNewCode": 0
    }
    try:
        response = requests.get(
            "https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg", params=params_a, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data['cdlist'][0]['songlist'])   
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return jsonify({"error": "HTTP Error", "message": str(errh)}), 500

# 获取歌曲mp3链接
@app.route('/get_song_url', methods=['GET'])
def get_song_url():
    params = request.args.to_dict() 
    params_a={
        "guid":10000,
        "vkey":params.get('vkey'),
        "uin":"",
        "fromtag":120042,
        "src":"M5000048rF4k1LcL1V.mp3"
    }
    url=params_a['src']
    try:
        response = requests.get(
            f'http://ws.stream.qqmusic.qq.com/{url}', params=params_a, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data['data']['items'][0]['vkey'])
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return jsonify({"error": "HTTP Error", "message": str(errh)}), 500
    

# 运行Flask应用，端口8080
if __name__ == '__main__':
    app.run(port=8080)
