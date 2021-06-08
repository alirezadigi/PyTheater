#786
from os import listdir , getcwd , popen
from os.path import isfile, join
import os
import sys
import cv2
import subprocess
from ffmpy import FFmpeg , FFprobe



def list_files(mypath):
    try:
        return [mypath+'\\'+f for f in listdir(mypath) if isfile(join(mypath, f))]
    except:
        return []

get_format_files = lambda mypath , file_type: filter(lambda x:True if x.split('.')[-1] == file_type else False,list_files(mypath))

    
def get_file_duration(filename):
    video = cv2.VideoCapture(filename)

    #duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps
    return duration

def make_thumbnail(input_video_path,thumbnail_path):
    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    #cap.set(1, get_file_duration(input_video_path)/60/6*60*fps)
    cap.set(1, get_file_duration(input_video_path)/60/6*60*fps)
    print(get_file_duration(input_video_path)/60/6*60*fps)
    ret, frame = cap.read()
    cv2.imwrite(thumbnail_path, frame)



def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs
    

def getcdir():
    if getattr(sys, 'frozen', False):
        script_directory = os.path.dirname(sys.executable)
    elif __file__:
        try:
            script_directory = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        except:
            script_directory = os.getcwd().replace('\\','/')
    return script_directory