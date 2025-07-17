import time

def detector(tscript_q, question_q, keyword, qlen):
    while True:
        question = tscript_q.check_buffer(keyword, qlen)
        if question != "":
            question_q.put(question)
        time.sleep(1)