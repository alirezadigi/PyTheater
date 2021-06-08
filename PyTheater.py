from flask import Flask, request, render_template, abort, jsonify, redirect, url_for, send_from_directory
from flask_basicauth import BasicAuth
import json
import pickle
import os
from os import listdir , getcwd , popen
import sys
import socket
import requests
import time
import re
from videotools import *

PASSWORD_PROTECTED = False
USERNAME = 'admin'
PASSWORD = 'password'






def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    print(IP)


def create_app():
    app = Flask(__name__ , static_url_path='/static_m',)
    try:
        get_ip()
    except:
        pass
    return app


app = create_app()  


if PASSWORD_PROTECTED == True:
    app.config['BASIC_AUTH_USERNAME'] = USERNAME
    app.config['BASIC_AUTH_PASSWORD'] = PASSWORD
    basic_auth = BasicAuth(app)
    app.config['BASIC_AUTH_FORCE'] = True




with open(getcdir() + '/static.txt') as static_txt_file:
    static_folders = static_txt_file.read().split('\n')
    static_folders.append(getcdir()+'/static')
    static_folders = [i.replace('\\','/').replace('//','/') for i in static_folders]


@app.route('/static/<path:filename>')
def base_static(filename):
    for static_folder in static_folders:
        file_path = static_folder + '/' + filename
        print(file_path)
        if os.path.exists(file_path) == True:
            out = send_from_directory(
                '/'.join(file_path.split('/')[:-1]), file_path.split('/')[-1])
            break
        else:
            out = '404'
    return out


@app.route('/videos/')
@app.route('/videos/<int:pnum>')
def home(pnum=0):
    videos_db = sorted((pickle.load(open(
        getcdir()+'/database.dat', 'rb'))), key=lambda x: x['name'])
    return render_template('home.html', videos=split(videos_db[(6*pnum):(6*pnum+6)], 3))


@app.route('/videos/bytime/')
@app.route('/videos/bytime/<int:pnum>')
def home_bytime(pnum=0):
    videos_db = sorted((pickle.load(open(
        getcdir()+'/database.dat', 'rb'))), key=lambda x: x['time'])[::-1]
    return render_template('home_bytime.html', videos=split(videos_db[(6*pnum):(6*pnum+6)], 3))


@app.route('/videos/search/', methods=['POST'])
@app.route('/videos/search/<string:url>/', methods=['POST', 'GET'])
@app.route('/videos/search/<string:url>/<int:pnum>/', methods=['POST', 'GET'])
def search(pnum=0, url=''):
    if 'url' in request.form:
        thingtosearch = request.form['url']
        return redirect((url_for('search', pnum=0, url=thingtosearch)))
    elif url != '':
        thingtosearch = url
        videos_db = sorted(list(filter(lambda db_item: True if thingtosearch in db_item['name'] else False, pickle.load(
            open(getcdir()+'/database.dat', 'rb')))), key=lambda x: x['name'])
        return render_template('home_search.html', videos=split(videos_db[(6*pnum):(6*pnum+6)], 3))


@app.route('/videos/play/<string:file_id>/')
def play_video(file_id=''):
    browser = request.user_agent.browser
    version = request.user_agent.version and int(
        request.user_agent.version.split('.')[0])
    platform = request.user_agent.platform
    uas = request.user_agent.string
    if browser and version:
        print(browser,version)
        if (browser == 'msie' and version < 9) \
                or (browser == 'firefox' and version < 4) \
                or (platform == 'android' and browser == 'safari' and version < 534) \
                or (platform == 'iphone' and browser == 'safari' and version < 7000) \
                or ((platform == 'macos' or platform == 'windows') and browser == 'safari' and not re.search('Mobile', uas) and version < 534) \
                or (re.search('iPad', uas) and browser == 'safari' and version < 7000) \
                or (platform == 'windows' and re.search('Windows Phone OS', uas)) \
                or (browser == 'opera') \
                or (browser == 'chrome' and version < 40) \
                or (re.search('BlackBerry', uas)):
            if file_id != '':
                return render_template('video_player2.html', video=list(filter(lambda db_item: True if file_id in db_item['name'] else False, pickle.load(open(getcdir()+'/database.dat', 'rb')))))
            else:
                return '404'
        elif browser == 'msie':
            if file_id != '':
                return render_template('video_player2.html', video=list(filter(lambda db_item: True if file_id in db_item['name'] else False, pickle.load(open(getcdir()+'/database.dat', 'rb')))))
            else:
                return '404'

        else:
            if file_id != '':
                return render_template('video_player.html', video=list(filter(lambda db_item: True if file_id in db_item['name'] else False, pickle.load(open(getcdir()+'/database.dat', 'rb')))))
            else:
                return '404'


@app.route('/set_seen/<string:file_id>/')
def set_seen(file_id=''):
    database = pickle.load(open(getcdir()+'/database.dat', 'rb'))
    for db_item in database:
        if file_id in db_item['name']:
            db_item['seen'] = True
            break
    video=list(filter(lambda db_item: True if file_id in db_item['name'] else False,database))
    pickle.dump(database,open(getcdir()+'/database.dat', 'wb'))
    return render_template('video_player.html', video=video)

@app.route('/set_unseen/<string:file_id>/')
def set_unseen(file_id=''):
    database = pickle.load(open(getcdir()+'/database.dat', 'rb'))
    for db_item in database:
        if file_id in db_item['name']:
            db_item['seen'] = False
            break

    video=list(filter(lambda db_item: True if file_id in db_item['name'] else False,database))
    pickle.dump(database,open(getcdir()+'/database.dat', 'wb'))
    return render_template('video_player.html', video=video)




app.run(host='0.0.0.0', port=9995)
