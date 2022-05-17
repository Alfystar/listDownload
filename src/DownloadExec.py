import queue
import threading

nDownload: int = 0


def downloadList(items: list, pDW: int = 10) -> int:
    """
    @items  : Array of DownloadItem
    @pDW    : Number of max parallel Connection openable
    return  : Number of file real downloaded
    """
    global nDownload

    # Creo una coda degli item così da ripartirla tra i thread
    q = queue.SimpleQueue()
    for it in items:
        q.put(it)

    # Apro tanti thread quanti richiesti, se gli elementi sono meno, evito la fatica inutile
    for dwInfo in range(min(q.qsize(), pDW)):
        t = threading.Thread(target=run_thread, args=[q])
        t.start()

    # while not q.empty():
    #     time.sleep(1)
    # return nDownload


def run_thread(q: queue.SimpleQueue):
    global nDownload
    while not q.empty():
        it = q.get()
        # nDownload += it.download()
        nDownload += it.myDownload()
