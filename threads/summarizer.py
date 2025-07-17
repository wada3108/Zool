import asyncio
from multiprocessing import Process
import openai
import os
import time

client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# 同期 GPT 呼び出し
def sync_gpt_call(name, context):
    prompt = f"""
以下の文章は、人物の名前の前後50文字の文脈です。この人物に振られた現在の質問の内容がわかるように、短く自然な日本語で要約してください。HeyGen のインタラクティブアバターが理解しやすく返事できるような内容にしてください。
文脈: \"\"\"{name}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは日本語で文脈を要約する優秀なAIです。"},
            {"role": "user", "content": context}
        ],
        temperature=0.7,
        max_tokens=200
    )
    print(response)
    return response.choices[0].message.content

# 非同期で GPT API を呼び出す
async def call_gpt_api_async(name, context):
    reply = await asyncio.to_thread(sync_gpt_call, name, context)
    print(f"GPT Response: {reply}")
    return reply

# gpt_worker_process の引数に Queue を追加
def gpt_worker_process(name, context, result_queue):
    print("CALLING GPT API")
    async def async_main():
        reply = await call_gpt_api_async(name, context)
        result_queue.put(reply)  # GPT の応答を Queue に投入
    asyncio.run(async_main())

def summarizer(name, questions_q, summary_q):
    while True:
        while not questions_q.empty():
            print(questions_q.qsize())
            question = questions_q.get()
            print(f"SUMMARIZER: {question}")
            p = Process(target=gpt_worker_process, args=(name, question, summary_q))
            p.start()
            # p.join()  # 必要に応じて非同期化
        time.sleep(1)
