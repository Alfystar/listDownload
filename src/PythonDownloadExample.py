#source: https://stackoverflow.com/questions/40126334/get-the-speed-of-downloading-a-file-using-python
import requests
import sys
import time

link = "https://www.easydeath.net/DDL/ANIME/BokuNoHeroAcademia5/BokuNoHeroAcademia5_Ep_01_SUB_ITA.mp4"
file_name = "BokuNoHeroAcademia5_Ep_01_SUB_ITA.mp4"
#link = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
#file_name = "downloaded.png"
start = time.perf_counter()
response = requests.get(link, stream=True)
with open(file_name, "wb") as f:
    print ("Downloading " + file_name)
    response = requests.get(link, stream=True)
    total_length = int(response.headers.get('content-length'))
    print (response.headers["content-type"])
    print (str(total_length / 1024) + "Kb")
    #print (str(int(response.headers["Age"]) * (10 ** -6))+"Sec") # Time of the cached object, not important for us
    print (response.headers["date"])
    print(response.headers)
    
    if total_length is None: # no content length header
        f.write(response.content)
    else:
        dl = 0
        # Connection never close, but "interrupt" is send every chunk, efficient and able to get statistics
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s>%s] %s bps" % ('=' * (done-1), ' ' * (50-done), dl//(time.perf_counter() - start)))
            sys.stdout.flush()
    print()
