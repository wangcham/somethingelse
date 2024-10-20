from quart import send_from_directory, render_template
from quart import Quart, request, Blueprint,jsonify
import os
import asyncio
from openai import OpenAI
from quart_cors import cors


app = Quart(__name__, template_folder="./frontend/dist", static_folder="./frontend/dist", static_url_path="")
cors(app)

@app.route('/')
async def index():
    return await render_template("index.html")

@app.route('/hello', methods=['POST'])
async def hello():
    print('Hello function called')  # 修改打印信息
    client = OpenAI(
        api_key="sk-Okxk8QPdikCkOfcn2k92D1FWnH2QYakVK8CFffxxX6xyRLrv",
        base_url="https://api.moonshot.cn/v1",
    )
    response = "No response"  # 给 response 一个默认值
    try:
        data = await request.get_json()  # 确保异步获取请求数据
        print('Received data:', data)  # 打印收到的数据，便于调试
        
        # 安全获取 'input'，因为前端发送的数据是 { input: inputValue.value }
        question = data.get('input', None)
        
        if question is None:
            return jsonify({'status': 'error', 'message': 'No input provided'}), 400

        messages = [
            {"role": "system", "content": "你是一个答题机器人，现在我告诉你一些问题，你只需要给我正确的答案选项就行"},
            {"role": "user", "content": question}
        ]
        
        # 异步调用
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.3,
        )
        
        response = completion.choices[0].message.content  # 如果成功，赋值 response
        print('response:')
        print(response)
    except Exception as e:
        print('Error:', str(e))  # 打印具体的错误信息
        
    return jsonify({'status': 'ok', 'result': response})






if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(app.run_task(host='0.0.0.0', port=5000))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()