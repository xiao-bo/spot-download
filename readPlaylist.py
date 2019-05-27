import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import json
from json import JSONDecoder
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import subprocess
import os
import youtube_dl
import threading
#from lxml import etree
def parse_object_pairs(pairs):
    return pairs


def readPlaylistOfUser():
    ## 
    client_credentials_manager = SpotifyClientCredentials(client_id='a54b43879cd84e20958d1f5d19779098',
                                                          client_secret='6fe136a6d2354c95bcb2cc65c03bf50c')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    uri = 'spotify:user:11100108479:playlist:3r5g0eS6qm3lbSnNsHHMIR' ## test
    #uri = 'spotify:user:11100108479:playlist:2wzBhTA7cY6Q9FKqT7iP0Y' ## favorite 14 
    #uri = 'spotify:user:11100108479:playlist:0Zssx2bVXVIY39Ky8Qpr9C' ## favorite 13
    #uri = 'spotify:user:11100108479:playlist:1DE6KQxKyxbj0ZcFj0tjND' ##chinese
    ## read data
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
    dataOfPlaylist = sp.user_playlist(username, playlist_id)


    result = []
    ## parse name of songs and singers


    tracks = dataOfPlaylist["tracks"]
    tracks_items = tracks['items']
    countofsongs = len(tracks_items)
    for x in range(0,countofsongs): 
        artists = (tracks_items[x])['track']['artists']
        nameOfSong = (tracks_items[x])['track']['name']
        result.append([])
        for element in artists:
            #print (element['name'].encode('utf-8'))
            ## append name of singer 
            result[x].append(element['name'])
        #print (nameOfSong.encode('utf-8'))
        result[x].append(nameOfSong)
    print ("========")
    for x in result:
        print (str(x).encode('utf-8'))

    return result
def get_url(name):
    nameofsongs = ""
    ## get the url of the song
    print ("========")
    print(name[0])
    print(len(name[0]))
    for x in range(0,len(name)):
        nameofsongs = nameofsongs+name[x]+"+"
    nameofsongs = nameofsongs+"lyrics"
        #nameofsongs = name[0][0]+"+"+name[0][1]+"+"+name[0][2]+"+ lyrics"
    print(nameofsongs)
    #print('https://www.youtube.com/results?search_query=lady+gaga+shallow')
    #res = requests.get('https://www.youtube.com/results?search_query=lady+gaga+shallow')
    res = requests.get("https://www.youtube.com/results?search_query="+nameofsongs)
    

    content = res.content.decode()
    #print(content)

    #html = etree.HTML(content)
    bs = BeautifulSoup(content,'html.parser')
    #print(bs.prettify())
    print("=============\n===================\n==========\n\n\n\n")
    for x in bs.find_all('a'):
        if (x.get('aria-describedby')): 
        ## because tag name of aria-describedby has video href
        ## remain part do not have href 
            #print (x.get('href'))
            url = x.get('href')
            break

    return url
    
def youtubeDownload(url):
    prefix = "https://www.youtube.com"
    url = prefix + url

    
    print (url)
   
    '''
    subprocess.call(['ffmpeg', '-i',                # or subprocess.run (Python 3.5+)
    os.path.join(parent_dir, default_filename),
    os.path.join(parent_dir, new_filename)
    ])
    ''' 
            
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',}],
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    
    print('Task Completed!')  

if __name__ == '__main__':
    playlist = readPlaylistOfUser()
    url = []
    threads=[]
    for x in range(0,len(playlist)):
        url.append(get_url(playlist[x]))

    for x in range(0,len(url)):
        threads.append(threading.Thread(target = youtubeDownload,args = (url[x],)))
        threads[x].start()
        #youtubeDownload(url[x])
    print (url)
    #

    