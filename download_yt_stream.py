from pytubefix import YouTube
from pytubefix.cli import on_progress
# from pytubefix.exceptions import VideoUnavailable
# import streamlit as st
import pandas as pd
import csv
import re
import os
from collections import defaultdict
# import numpy as np

yt_fields=['URL']

# os.path

file=open('Youtube_download.csv','a+', newline='')
writer=csv.DictWriter(file,fieldnames=yt_fields,delimiter=',')

# writer.writeheader()

while True:
    url=input("enter the url: ")  #first check the url validity
    if url == "end":
        file.close()
        break
    yt_pattern='^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
    check=re.match(yt_pattern,url)
    if not check:
        print(f'Youtube URL is not valid')
        url=''
    # else:
    #     pass
        
    try:
        yt=YouTube(url)
    except Exception as e:
        print(f'Video {url} is unavailable, private video or region restricted. Cannot download. Skipping. Error: {e}')
    else:
        pass

    new_url={'URL':url}

    writer.writerow(new_url)
    

def get_csv_file():
    csvFile=pd.read_csv('Youtube_download.csv')
    print('read csv')
    return csvFile

yt_file=get_csv_file()

# https://www.youtube.com/watch?v=AzV3EA-1-yM&list=WL&index=11&pp=g
# https://www.youtube.com/watch?v=VvlCNvA_wEo
# https://www.youtube.com/watch?v=rLkKMcMo5RU


print(yt_file)
# ind=yt_file.head(1).index[0]
# print(ind)
# print("\n after drop\n")
# yt_file.drop([ind],inplace=True)
# print(yt_file)
# print(yt_file.head(1).index[0])


# st=yt_file.head(1).values
# print(type(yt_file.head(1).values))


# print(np.frombuffer(st))
def download_from_csv():
    count=0
    while not yt_file.empty:
        print("1st sec")
        yt_index=yt_file.head(1).index[0]

        print(f'func1.0 : {yt_index} ')
        url=yt_file['URL'][yt_index]
        print("2nd sec ")
        #    print(url)
        try:
            yt = YouTube(url, on_progress_callback = on_progress)
        except Exception as e:
            print(f'Video is unavailable, private video or region restricted. Cannot download. Skipping. Error :{e}')
        else:
            #    print('go on')
            pass
        
        print("...continuing")
            
        print(yt.title)
        print(yt.author)
        ys = yt.streams.get_highest_resolution()
        ys.download()

        yt_file.drop([yt_index],inplace=True)
        #    print("\nNew\n",yt_file)             #last check for the empty dataframe
        url=''

        
        if count==7:
            break
        else:
            count+=1
        print(count)

def delete_file():
    folder_path = 'C:\\Users\\HP\\Desktop\\Practice\\python'

# Step 4: Create a dictionary to store files by prefix
    prefix_dict = defaultdict(list)

# Step 3: Scan the directory
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Get the prefix (assuming the prefix is everything before the first '_')
            if filename.endswith('.csv'):
                prefix = filename.split('student')[0]
            # Group files by prefix
            
                prefix_dict[prefix].append(filename)


    # file_for_remove='students.csv'
    for prefix, files in prefix_dict.items():
        if len(files) > 1:
            # print(f"Prefix: {prefix}")
            for file in files:
                print(f"    {file}")
                if(os.path.exists(file) and os.path.isfile(file)):
                    os.remove(file)
                    print(f'{file} deleted')
                else:
                    print(f"{file} file not found")

download_from_csv()
# delete_file()

