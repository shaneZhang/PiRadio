# coding=utf-8
# !flask/bin/python
from flask import Flask
from flask import request
from flask import jsonify
import httplib
import json
import commands
import os
import time
import random
import sys
from subprocess import call
from multiprocessing import Pool

reload (sys)
sys.setdefaultencoding('utf8')


music_search_host = 'api.5288z.com'
music_search_port = 10080
music_search_file = '/weixin/musicapi.php'

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


# 拦截一下search请求
@app.route('/search', methods=['GET'])
def get_search():
    if 'name' in request.args:
        return search_music(request.args['name'])
    else:
        return jsonify(get_result(-1, 'error params with name'))


# 封装统一返回的格式
def get_result(code, msg):
    return {'code': code, 'msg': msg}


# 网络请求,获取mp3的网络url
def search_music(name):
    print 'name is :' + name
    httpClient = None

    try:
        httpClient = httplib.HTTPSConnection(music_search_host)
#        httpClient = httplib.HTTPConnection(music_search_host, music_search_port, timeout=50)
        url_path = music_search_file + '?q=' + name;
        httpClient.request('GET', str(url_path))
        response = httpClient.getresponse()
        return handle_network_result(response)
    except Exception, e:
        print e
        return jsonify(get_result(-1, 'error with network requet'))
    finally:
        if httpClient:
            httpClient.close()


# 处理网络请求音乐返回的结果
def handle_network_result(response):
    result = response.read()
    result = result.decode('unicode_escape')
    result = result.encode('utf-8')
    print result
    json_result = json.loads(result)
    status_code = json_result['status']
    if status_code == 200:
        music_model = json_result['content']
        music_url = music_model['MusicUrl']
        return zyq_exec_cmd(music_url)
    else:
        errMsg = '网络请求返回数据错误'
        return jsonify(get_result(-1, errMsg))


# 树莓派执行操作系统的命令
def zyq_exec_cmd(music_url):
    curDir = os.getcwd()
    check_cmd = str( curDir + '/check.sh sox')
    stop_cmd = str(curDir + '/stop.sh sox')
    tmp = commands.getoutput(check_cmd)
    if tmp == 'Running':
        print 'kill the music playing'
        os.system(stop_cmd)
        time.sleep(1)
        background_thread_play_music(music_url)
    else:
        print 'no music is playing'
        background_thread_play_music(music_url)
    return jsonify(get_result(0, str(music_url + 'now is playing')))

#后台线程播放音乐
def background_thread_play_music(music_url):
    curDir = os.getcwd()
    play_cmd = str('sudo ' + curDir + '/play.sh ' + music_url + ' &')
    print 'play commond:' + play_cmd
    os.system(play_cmd)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=1234)
