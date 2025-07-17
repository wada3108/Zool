import multiprocessing
import threading
import queue
import time

from threads.transcriptor import transcriptor as tscript
from threads.word_detector import detector
from threads.summarizer import summarizer
from threads.heygen_mgr import heygenmgr

from utils.transcript_queue import TranscriptQueue


keyword = "杉山"
qlen = 50


tscript_q = TranscriptQueue()
question_q = queue.Queue()
summary_q = multiprocessing.Queue()


def main():
    tscript_t = threading.Thread(target=tscript, args=(tscript_q,), daemon=True)
    detector_t = threading.Thread(target=detector, args=(tscript_q, question_q, keyword, qlen), daemon=True)
    summarizer_t = threading.Thread(target=summarizer, args=(keyword, question_q, summary_q), daemon=True)
    heygen_t = threading.Thread(target=heygenmgr, args=(summary_q,), daemon=True)

    tscript_t.start()
    detector_t.start()
    summarizer_t.start()
    heygen_t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tscript_t.join()
        detector_t.join()
        summarizer_t.join()
        heygen_t.join()

if __name__ == "__main__":
    main()
