#786
from videotools import *
import json
import pickle
import time

try:
    videos_database = pickle.load(open(getcdir()+'/database.dat','rb'))
    print('previous datavbase loaded!')
except:
    videos_database = []
    print('new databse built!')



with open(getcdir() + '/static.txt') as static_txt_file:
    videos_pathes = static_txt_file.read().split('\n')
    videos_pathes = [i.replace('\\','/').replace('//','/') for i in videos_pathes]

videos_pathes = [i + '/videos' for i in videos_pathes]



for videos_path in videos_pathes:
    continue_to_rest = True
    try:
        videos_list = [i.replace('\\','/').replace('//','/') for i in get_format_files(videos_path,'mp4')]
    except:
        continue_to_rest = False

    if continue_to_rest == True:
        database_videos_names = [i['name'] for i in videos_database]
        if videos_list != database_videos_names:
            #print('New Files!')
            for video in videos_list:
                video = video.replace('\\','/').replace('//','/')
                for i in range(1):
                    try:
                        if video not in database_videos_names:
                            print(video)
                            if os.path.isfile(video.replace('mp4','jpg')) == False:
                                make_thumbnail(video,video.replace('mp4','jpg'))
                            videos_database.append({'name':video,'duration':get_file_duration(video),'thumbnail':video.replace('mp4','jpg'),'more_info':video.replace('mp4','txt'),'time':str(time.time()),"d_name":'','d_info':'','seen':False})
                        break
                    except Exception as error:
                        print('error',error)
                        pass


            pickle.dump(videos_database,open(getcdir()+'/database.dat','wb'))


        database_videos_names = [i['name'] for i in videos_database]
        videos_list = [i.replace('\\','/').replace('//','/') for i in get_format_files(videos_path,'mp4')]




videos_list = []

for videos_path in videos_pathes:
    videos_list.extend([i.replace('\\','/').replace('//','/') for i in get_format_files(videos_path,'mp4')])

for video in database_videos_names:
    if video not in videos_list:
        print(video,'not found in folder!')
        videos_database.pop(videos_database.index(list(filter(lambda x: True if video in x['name'] else False, videos_database))[0]))
        print(video,'deleted!')




pickle.dump(videos_database,open(getcdir()+'/database.dat','wb'))



