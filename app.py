import streamlit as st
import download_yt_stream as dy
import os

st.title('Youtube Video downloader')

#folder and file paths
folder_path='C:\\Users\\HP\\Desktop'
folder='New1'
file='Youtube_download.csv'

path=os.path.join(folder_path,folder)
file_path=os.path.join(path,file)

result_lt=dy.check_file_exist(path,file_path)  #check whether file exist or if not then, create one

if(len(result_lt[0])>1):                #display warning 
    st.warning(result_lt[0])

# st.write(result_lt[1])      write "file" if check_file_exist has no errors and created the file

if "my_text" not in st.session_state:           
    st.session_state.my_text=""

def clear_input_box():          #function to clear the input box after submitting the URL
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""


st.text_input("Write the URL",key="widget",on_change=clear_input_box)       #input box to enter the URL

url= st.session_state.my_text

btn=st.button("Click to store the URL")                 #button to start writitng into the csv file and storing the URLs

if(btn):                                        #when 1st button is clicked
    write_lt=dy.write_data_in_csv(file_path,url)
    if(write_lt[1]=='done'):
        st.toast("URL stored into the csv file")

    if(len(write_lt[0])):
        st.warning(write_lt[0])

file_df=dy.get_csv_file(file_path)              #storing the data in the file in form of Dataframe

st.dataframe(file_df)                           #display Dataframe

container1=st.container(border=True)
container1.subheader("Download")
btn2=container1.button("Download videos")           #button to start downloading the videos into the given folder, or path mentioned in 'path' string

if(btn2):                               #when 2nd button is clicked

    down_lt=dy.download_from_csv(file_df,path)            #call function to start downloading the videos

    if(len(down_lt[0])):                        #if there is an error
        container1.warning(down_lt[0])

    container1.write(down_lt[1])                #display "downloaded" as video is successfully downloaded

    container1.dataframe(file_df)               #display the dataframe

    delete_files=dy.delete_file(path)               #call function to delete the csv file

    for file_del in delete_files:                   #print names of deleted files

        container1.write(f'{file_del} Deleted')         




