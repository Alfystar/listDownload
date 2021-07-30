import time

# import DownloadItem
# import AtomicInteger
from .DownloadItem import *
from .AtomicInteger import *

# Thread active counter
activeThread = AtomicInteger(0)
semActiveTread = threading.Semaphore()
nDownload: int = 0

def downloadList(items: list, pDW:int = 5) -> int:
    """
    @items  : Array of DownloadItem
    @pDW    : Number of max parallel Connection openable
    return  : Number of file real downloaded
    """
    global activeThread, semActiveTread, nDownload
    activeThread = AtomicInteger()
    semActiveTread = threading.Semaphore(pDW)
    for item in items:
        semActiveTread.acquire()
        activeThread.inc()
        t = threading.Thread(target=thread_downloader, args=item)
        t.start()

    while activeThread.value != 0:
        time.sleep(1)
    return nDownload


def thread_downloader(item: DownloadItem):
    global activeThread, semActiveTread, nDownload
    nDownload += item.download()
    activeThread.dec()
    semActiveTread.release()
