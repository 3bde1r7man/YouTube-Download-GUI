#-----------------------------------------------------------------------------
# YouTube (Video/Playlist/Audio) Download.
# Authors       : Ahmed Hanfy Bekheet &&  Abdelrhman Mostafa Hessain
# Version       : 1.0
# Python Version: 3.9.10
# Date          : 3 / 9 /2022
#-----------------------------------------------------------------------------
# Pesuado Code:
#  1. Make the APP window and change the title
#  2. Make a start Button to start the APP
#  3. Make Buttons with Video, Playlist, Audio or Playlist As Audio to choose from
#  4. After that take the url from the user
#  5. Check if the url is Type and if video or playlist he will choose the Quality
#  6. Choose the Path
#  7. If audio he will download the video automatic 
#    1. If playlist he will choose from the list the vidoes that he want to download or select all
#-----------------------------------------------------------------------------


from tkinter import *
from tkinter import filedialog
from pytube import Playlist
from pytube import YouTube
import os


# To create the window
root = Tk()
root.geometry("500x300")
root.title("YouTube Download")


Start_Button = Button(root, text= "Press To Start", command= lambda: choose()).pack(pady=80)
lis_1 = []

def choose(): # To choosse What You Want To Download ?
    for x in root.winfo_children(): # To Destroy any thing in the window to add into a clean window 
        x.destroy()
    rows = 0
    col = 0
    lis = ["Video", "Playlist", "Audio", "Playlist As Audio"]
    for i in range(1,5): # To make Buttons with numbers from 1 to 4 and Label with the choose
        Button(root, text= i, command= lambda i = i: URL(i) , width= 20).grid(row=rows, column=col)
        Label (root, text=lis[i-1], width=20).grid(row=rows, column=1)
        rows += 1
    

def URL(i):
    global entry_box
    for x in root.winfo_children(): # To Destroy any thing in the window to add into a clean window 
        x.destroy()
    entry_box = Entry(root, width =85) # To create a box you can enter a text in
    entry_box.insert(0,"enter the video URL Here")
    entry_box.grid(row=0 , column=0)
    entry_box.bind("<FocusIn>", temp_text) # To disappeared the text in the box once it selected
    Button(root, text="Next", command= lambda: download_video(i) , width=20).grid(row=1,column=0)


def temp_text(e): 
    '''To distroy the text in the entry box if focusin'''
    entry_box.delete(0,"end")


def download_video(Type):
    '''To get the url from the box and if it available'''
    global video, video_type, url
    video_type = Type
    url = entry_box.get()
    if Type == 1:
        try:
            video = YouTube(url) 
            choose_quality()
        except:
            return URL(Type)
    if Type == 2:
        try:
            video = Playlist(url)
            play_list()    
        except:
            return URL(Type)
    elif Type == 3 or Type == 4:
        audio()


def audio():
    '''to avoid choose Qulaity we make this def'''
    global video
    for x in root.winfo_children(): 
        x.destroy()
    if video_type == 4:
        try:
            video = Playlist(url)
            Button(root, text="Next",command=lambda:[play_list(), choose_path()],width=20).pack()
        except:
            return URL(video_type)
    elif video_type == 3:
        try:
            video = YouTube(url)
            Button(root, text="Next",command=lambda:[choose_path() ,download()],width=20).pack()
        except:
            return URL(video_type)


def play_list():
    '''To add each video url to a list to make leater a Button with each title'''
    global lis
    for x in root.winfo_children(): 
        x.destroy()
    videos_title = video.video_urls #To get each video URl in the play list
    lis = []
    for i in videos_title:
        lis.append (i)    
    

def choose_quality():
    global vid_res
    for x in root.winfo_children():  
        x.destroy()
    vid_res = ["144p","360p","720p"]
    rows = 0
    col = 0
    for i in vid_res: #To make Buttons with each Quality to choose
        Button(root, text= i, command= lambda i = i: [vid_quality(i), download()] , width= 20).grid(row=rows, column=col)
        rows += 1


def click():
    '''To appear each video as a button if clicked add this video URL to a list to download'''
    rows = 0
    col = 0
    for i in lis:
        Button(root, text=YouTube(i).title,command= lambda i=i: lis_1.append(i),width= 70).grid(row=rows, column=col)
        rows +=1    
    Button(root, text="Select All", command=lambda: lis_1.extend(lis),width=20).grid(row=len(lis),column=0) 
    # This Button to selcet all the videos from playlist 
    download()


def vid_quality(i):
    '''Define the Quality of the video rhat he chooses'''
    global quality
    quality = i
    choose_path()


def choose_path(): 
    '''This To  make the user select a folder path'''
    path = filedialog.askdirectory()
    os.chdir(path)
    if video_type == 2 or video_type == 4: # If playlist go for click to apppear each video to the user 
        click()
        

def last():
    '''To get each video he clicked and filter the list if he clicked the Button twice'''
    for x in root.winfo_children():  
        x.destroy()
    last_list = set(lis_1)
    if video_type == 2:
        for video in last_list:
            YouTube(video).streams.filter(res=quality,progressive=True).last().download()
    elif video_type == 4:
        for video in last_list:
            YouTube(video).streams.filter(type="audio").last().download()
    root.destroy()


def download():
    '''To download each if video or list'''
    if video_type == 1:   
        video.streams.filter(res=quality,progressive=True).last().download()
        root.destroy()
    if video_type == 2 or video_type == 4:
        Button(root,text="Next",command=lambda:last(),width=20).grid(row=len(lis)+1,column=0)    
    elif video_type == 3:
        video.streams.filter(type = "audio").last().download()
        root.destroy()

if __name__ == '__main__':
    root.mainloop() # To start the window loop