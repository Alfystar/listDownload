import time
import threading
import queue
# import DownloadItem
from src.listDownloadSrc.downloadSubSystem import *

nDownload: int = 0


def downloadList(items: list, pDW: int = 10) -> int:
    """
    @items  : Array of DownloadItem
    @pDW    : Number of max parallel Connection openable
    return  : Number of file real downloaded
    """
    global nDownload
    q = queue.SimpleQueue()
    for it in items:
        q.put(it)

    for dwInfo in range(pDW):
        t = threading.Thread(target=run_thread, args=[q])
        t.start()

    while not q.empty():
        time.sleep(1)
    return nDownload


def run_thread(q: queue.SimpleQueue, di: DownloadInfo):
    global nDownload
    while not q.empty():
        it = q.get()
        nDownload += it.download(di)
