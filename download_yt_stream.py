from pytubefix import YouTube
from pytubefix.cli import on_progress
# from pytubefix.exceptions import VideoUnavailable
import streamlit as st
import pandas as pd
import csv
import re
import os
from collections import defaultdict
# import numpy as np



yt_fields=['URL']


def check_file_exist(path,file_path):
    err=" "
    if(os.path.exists(path)):
        print("exist")
        # try:
        #     os.mkdir(path,0o666)
        #         # try:
        #         #    os.chmod(path, 0o666)
        #         #    print("File permissions modified successfully!")
        #         # except PermissionError:
        #         #     print("Permission denied: You don't have the necessary permissions to change the permissions of this file.")
        #             # os.chmod(path,mode)
        #     print('created folder')
        # except OSError as e:
        #     print(e)
        #     err=f'{e}'
        # else:
        #     pass
    else:
        print("not found")
        try:
            os.mkdir(path,0o666)
            # try:
            #    os.chmod(path, 0o666)
            #    print("File permissions modified successfully!")
            # except PermissionError:
            #     print("Permission denied: You don't have the necessary permissions to change the permissions of this file.")
                # os.chmod(path,mode)
            print('created folder')
        except OSError as e:
            print(e)
            err=f'{e}'
        else:
            pass


    if(os.path.exists(path)):
        if(not os.path.exists(file_path)):
            # yt_fields=['URL']
            f=open(file_path,'w+',newline='')
            writer=csv.DictWriter(f,fieldnames=yt_fields,delimiter=',')
            print('file created ')
            writer.writeheader()
            f.close()

    lt=[err,'file']
    # lt="file"
    return lt

    



# check_file_exist()



# os.path
#----------------------------------------->
def write_data_in_csv(file_path,url):
    err=[]
    d='NA'
    file=open(file_path,'a+', newline='')
    writer=csv.DictWriter(file,fieldnames=yt_fields,delimiter=',')

    # writer.writeheader()
    count=0
    while True:
        print(url)    #=input("enter the url: ")  #first check the url validity
        if url == "end":
            file.close()
            break
        yt_pattern='^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
        check=re.match(yt_pattern,url) !=None
        print(f"check1: {check}")

        if (not check):
            print(f'check2: {check} .Youtube URL is not valid')
            url=''
            err.append('Youtube URL is not valid')
            break
        else:
            
            try:
                yt=YouTube(url)
            except Exception as e:
                print(f'Video {url} is unavailable, private video or region restricted. Cannot download. Skipping. Error: {e}')
                err.append(f'{e}')
            else:

                new_url={'URL':url}

                writer.writerow(new_url)
                d='done'
                break
        
        url=''

        # if(count==5):
        #     break
        # else:
        #     count+=1
    try:
        file.close()
    except Exception as e:
        print(f'{e}')
        err.append(f'{e}')
    else:
        pass

    write_lt=[err,d]
    url=''

    return write_lt

    
#------------------------------------------------->
def get_csv_file(file_path):
    csvFile=pd.read_csv(file_path)
    print('read csv')
    return csvFile

# yt_file=get_csv_file()

# # https://www.youtube.com/watch?v=AzV3EA-1-yM&list=WL&index=11&pp=g
# # https://www.youtube.com/watch?v=VvlCNvA_wEo
# # https://www.youtube.com/watch?v=rLkKMcMo5RU


# print(yt_file)
# # ind=yt_file.head(1).index[0]
# # print(ind)
# # print("\n after drop\n")
# # yt_file.drop([ind],inplace=True)
# # print(yt_file)
# # print(yt_file.head(1).index[0])


# # st=yt_file.head(1).values
# # print(type(yt_file.head(1).values))


# # print(np.frombuffer(st))


def download_from_csv(file_df,path):
    yt_file=file_df
    count=0
    err=[]
    # yt_file_empty=False
    done=''
    # while not yt_file.empty:
        
    #     break
        # print("1st sec")
        # yt_index=yt_file.head(1).index[0]

        # print(f'func1.0 : {yt_index} ')
        # url=yt_file['URL'][yt_index]
        # print("2nd sec ")
        # #    print(url)
        # try:
        #     yt = YouTube(url, on_progress_callback = on_progress)
        # except Exception as e:
        #     print(f'Video is unavailable, private video or region restricted. Cannot download. Skipping. Error :{e}')
        #     err.append(f'{e}')
        # else:
        #     #    print('go on')
        #     pass
        
        # print("...continuing")

        # try:    
        #     print(yt.title)

        #     print(yt.author,'\n')
        #     ys = yt.streams.get_highest_resolution()
        #     ys.download(output_path=path)

        #     yt_file.drop([yt_index],inplace=True)
        #     #    print("\nNew\n",yt_file)             #last check for the empty dataframe
        #     st.toast(f'No. {yt_index} \"{yt.title}\" downloaded ')
        #     done='downloaded!'
        # except Exception as e:
        #     print(f'Download() error: {e}')
        #     err.append(f'e')
        # else:
        #     pass
        # url=''
    #---------------------------------------->
    # if(yt_file.empty):
    #     yt_file_empty=True


        
        # if count==7:
        #     break
        # else:
        #     count+=1
        # print(count)
    
    down_lt=[err,done]
    return down_lt

def delete_file(path,name_file):
    # file_path.close()

    folder_path_2 = path

# Step 4: Create a dictionary to store files by prefix
    prefix_dict = defaultdict(list)

    file_list=[]
    print("call delete func")
# Step 3: Scan the directory
    for filename in os.listdir(folder_path_2):
        if os.path.isfile(os.path.join(folder_path_2, filename)):
            # Get the prefix (assuming the prefix is everything before the first '_')
            # print(f'filename: {os.path.basename(filename)}')
            if filename.endswith('.csv'):
                prefix = filename.split('You')[0]
                print(f'prefix: {prefix} type: {type(prefix)}')
            # Group files by prefix
            
                prefix_dict[prefix].append(filename)
                print('sorting done')
                print(f'in dict: {prefix_dict[prefix]}')


    # file_for_remove='students.csv'
    for prefix, files in prefix_dict.items():
        if len(files) >= 1:
            print(f"Prefix: {prefix}")
            for file in files:
                print(f"    {file}")
                if(os.path.exists(os.path.join(path,file)) or os.path.isfile(file)):

                    file_name=os.path.basename(file)
                    print(f"file basename: {file_name}")
                    file_list.append(file_name)

                    # os.remove(file)
                    print(f'{file} deleted')
                else:
                    print(f"{file} file not found")

    return file_list

    

# download_from_csv()
# # delete_file()

