import asyncio
import json
import threading
from time import time

import requests
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
from sample import message_queue, main as blivedm_main


def send_message_to_chatbot(message):
    base_url = "http://127.0.0.1:7861/chat"
    data = {
        "messages": [
            {"role": "user", "content": message},
        ],
        "model": "qwen1.5-chat",
        "tool_choice": "search_local_knowledgebase",
        "tool_input": {"database": "samples", "query": message},
        "stream": True,
    }

    response = requests.post(f"{base_url}/chat/completions", json=data, stream=True)
    concatenated_content = ""

    try:
        for line in response.iter_content(chunk_size=None, decode_unicode=True):
            if line:  # 忽略空行
                stripped_line = line.strip().lstrip('data: ')  # 去除前缀并去除尾随空白
                if stripped_line:
                    try:
                        data_block = json.loads(stripped_line)  # 尝试解析为JSON
                        if 'choices' in data_block and data_block['choices']:
                            delta = data_block['choices'][0]['delta']  # 假设每个choices列表至少有一个元素
                            if 'content' in delta:
                                concatenated_content += delta['content']  # 拼接content
                    except json.JSONDecodeError:
                        # 如果无法解析为JSON，则忽略这一行（可能是不完整的数据块）
                        continue

                        # 在这个例子中，我们没有等待特定的结束信号，因为API可能不是通过这种方式发送完整消息的
        # 但如果API确实发送了包含结束信号的数据块，您应该在这里添加逻辑来处理它

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")

    parts = concatenated_content.strip().split('\n\n')

    # 如果 parts 不为空，则取最后一个元素
    if parts:
        last_part = parts[-1]
        # 可能还需要进一步处理 last_part，比如去除前后的空白字符
        trimmed_last_part = last_part.strip()
        return trimmed_last_part
    else:
        print("没有找到文本部分")

def handle_input():
    while True:
        # 阻塞直到队列有数据
        danmaku_message = message_queue.get()
        print(f"Received Danmaku: {danmaku_message}")
        user_input = danmaku_message

        time1 = time()

        response = send_message_to_chatbot(user_input)
        #response = "你好"
        print(response)
        if response:
            data = {
                "refer_wav_path": "E:/downloads/GPT-SoVITS-beta/GPT-SoVITS-beta0706/test.wav",#修改为示例音频地址
                "prompt_text": "这个小小的玻璃球，就代表了巴巴托斯大人对可莉的肯定吗？",#修改为示例音频文字
                "prompt_language": "zh",
                "text": response,
                "text_language": "zh"
            }

            print(time() - time1)
            time1 = time()
            response2 = requests.post("http://127.0.0.1:9880", json=data)
            if response2.status_code == 400:
                raise Exception(f"请求出现错误")
            # 保存响应内容到文件
            output_path = "success.wav"
            with open(output_path, "wb") as f:
                f.write(response2.content)
                print("Successfully downloaded to", output_path)
            print(time() - time1)
            time1 = time()

            # 检查文件内容是否为有效的音频数据
            try:
                import wave

                with wave.open(output_path, "rb") as audio_file:
                    print(f"Audio file parameters: {audio_file.getparams()}")
                wave_obj = sa.WaveObject.from_wave_file(output_path)
                print(time() - time1)
                time1 = time()

                play_obj = wave_obj.play()
                play_obj.wait_done()  # 等待播放完成

            except wave.Error as e:
                print(f"Error reading audio file: {e}")

# 启动一个线程来运行blivedm_main
blivedm_thread = threading.Thread(target=lambda: asyncio.run(blivedm_main()))
blivedm_thread.start()

# 启动一个线程来处理用户输入
input_thread = threading.Thread(target=handle_input)
input_thread.start()

if __name__ == "__main__":
    handle_input()
