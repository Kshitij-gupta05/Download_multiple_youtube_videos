from pytubefix import YouTube
from pytubefix.cli import on_progress
import streamlit as st
import pandas as pd
import csv
import re
import os
from collections import defaultdict

yt_fields=['URL']

def check_file_exist(path,file_path):           #function to check if file or folder exist. If not, then create the new ones
    err=" "
    if(os.path.exists(path)):
        print("exist")
    else:
        print("not found")
        try:
            os.mkdir(path,0o666)            #create new folder
            print('created folder')
        except OSError as e:
            print(e)
            err=f'{e}'
        else:
            pass


    if(os.path.exists(path)):
        if(not os.path.exists(file_path)):
            f=open(file_path,'w+',newline='')   #open new file 
            writer=csv.DictWriter(f,fieldnames=yt_fields,delimiter=',')     #create a new csv file
            print('file created ')
            writer.writeheader()                #write the header of the column in the csv file
            f.close()

    lt=[err,'file']             #return error and "file" message
    
    return lt

def write_data_in_csv(file_path,url):         #function to enter the new URLs into the file
    err=[]
    d='NA'
    file=open(file_path,'a+', newline='')       #opening the file with file mode="a+" ,i.e., append and
    writer=csv.DictWriter(file,fieldnames=yt_fields,delimiter=',')

    while True:
        print(url)    #=input("enter the url: ")  #first check the url validity
        if url == "end":
            file.close()
            break
        yt_pattern='^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
        check=re.match(yt_pattern,url) !=None       #returns true if check =/= none
        print(f"check1: {check}")

        if (not check):
            print(f'check2: {check} .Youtube URL is not valid')
            url=''
            err.append('Youtube URL is not valid')          #append error into err list
            break
        else:
            
            try:                # try catch block to check whether the youtube video is accessible by the Youtube() function
                yt=YouTube(url)             
            except Exception as e:
                print(f'Video {url} is unavailable, private video or region restricted. Cannot download. Skipping. Error: {e}')
                err.append(f'{e}')
            else:

                new_url={'URL':url}

                writer.writerow(new_url)        #write the new URl into the file under 'URL' key
                d='done'
                break
        
        url=''

    try:
        file.close()                #closing the file after the work is done
    except Exception as e:
        print(f'{e}')
        err.append(f'{e}')
    else:
        pass

    write_lt=[err,d]
    url=''

    return write_lt

def get_csv_file(file_path):            #function to read the file and storing its data into a Dataframe
    csvFile=pd.read_csv(file_path)
    print('read csv')
   
    return csvFile

def download_from_csv(file_df,path):        #function to download Youtube videos with the help of URLs stored in the Dataframe
    yt_file=file_df
    count=0
    err=[]
    done=''

    while not yt_file.empty:        #while loop until the new Dataframe yt_file gets empty 
        print("1st sec")
        yt_index=yt_file.head(1).index[0]
        print(f'func1.0 : {yt_index} ')
        url=yt_file['URL'][yt_index]        #URL of a video
        print("2nd sec ")

        try:
            yt = YouTube(url, on_progress_callback = on_progress)   
        except Exception as e:
            print(f'Video is unavailable, private video or region restricted. Cannot download. Skipping. Error :{e}')
            err.append(f'{e}')
        else:
            pass
        
        print("...continuing")

        try:    
            print(yt.title)
            print(yt.author,'\n')
            ys = yt.streams.get_highest_resolution()
            ys.download(output_path=path)       #downloading the video

            yt_file.drop([yt_index],inplace=True)       #removing the URL from the Dataframe
            st.toast(f'SNo. {yt_index} \"{yt.title}\" downloaded ')         #message which tells which video got downloaded
            done='downloaded!'
        except Exception as e:
            print(f'Download() error: {e}')
            err.append(f'{e}')
        else:
            pass
        url=''
    
    down_lt=[err,done]

    return down_lt

def delete_file(path):
    folder_path_2 = path

# Step 1: Create a dictionary to store files by prefix
    prefix_dict = defaultdict(list)

    file_list=[]
    print("call delete func")
# Step 2: Scan the directory
    for filename in os.listdir(folder_path_2):          #scan throught the folder and looping through all present file
        if os.path.isfile(os.path.join(folder_path_2, filename)):           #check whether file exist or not
            prefix=None
            if(filename.endswith('.csv')):
                prefix=filename.find('Youtube_download')

                if(prefix==0):                  #if file "Youtube_download" or any other variation exist, put them in prefix_dict dictionary
                    prefix_dict[prefix].append(filename)
                    print(f'in dict: {prefix_dict[prefix]}')
                print('sorting done')

    for prefix, files in prefix_dict.items():       #loop through dictionary
        if len(files) >= 1:
            print(f"Prefix: {prefix}")
            for file in files:
                print(f"    {file}")
                if(os.path.exists(os.path.join(path,file)) or os.path.isfile(file)):        #check whether file is exist

                    file_list.append(file)          #append the name of the file in the file_list
                    print(f'{file} deleted')
                    os.remove(os.path.join(path,file))      #delete the csv files with URLs
                    
                else:
                    print(f"{file} file not found")

    return file_list

