import yt_dlp

def download_save_audio(link):
  
  print("Downloading audio")
  
  filename = link[-11:]+'.mp3'

  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': filename}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)

    return filename