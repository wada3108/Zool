import threading


class TranscriptQueue:
    def __init__(self):
        self.buffer = ""
        self.last_checked_index = 0
        self.lock = threading.Lock()

    def add_buffer(self, new_text):
        with self.lock:
            self.buffer += new_text

    def check_buffer(self, keywords, qlen):
        for kw in keywords:
            pos = self.buffer.find(kw)
            if pos != -1:
                if len(self.buffer) > pos + qlen:
                    question = self.buffer[pos - qlen: pos + qlen]
                    self.buffer = self.buffer[pos + qlen:]
                    self.last_checked_index = len(self.buffer)
                    return question
                else:
                    return ""
            else:
                self.buffer = self.buffer[-50:]
                self.last_checked_index = len(self.buffer)
                return ""
