import ollama
import base64

def chat_with_model(address, model):
    
    # 初始化一个空列表来存储恢复的对话历史
    conversation_history = []
    # 从文本文件中读取数据
    with open(address, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行末的换行符
            line = line.strip()
            # 查找第一个冒号的位置
            colon_index = line.find(':')
            if colon_index != -1:
                # 提取 role 和 content
                role = line[:colon_index].strip()
                content = line[colon_index + 1:].strip()
                # 将解析后的数据添加到列表中
                conversation_history.append({"role": role, "content": content})


    # 模拟用户输入的循环
    while True:
        user_input = input("你: ")

        # 用户输入 'exit' 结束对话
        if user_input.lower() in ["exit", "quit"]:
            print("对话结束")
            break

        # 将用户输入添加到对话历史
        conversation_history.append({"role": "user", "content": user_input})

        # 获取模型响应
        response = ollama.chat(
            model=model,  # 使用 gemma2:2b 模型
            stream=False,  # 将 stream=True 可实现流式输出
            messages=conversation_history,  # 传递对话历史作为列表
            options={"temperature": 0.7}
        )

        # 将模型响应添加到对话历史
        conversation_history.append({"role": "assistant", "content": response['message']['content']})

        # 输出模型响应
        print("模型:", response['message']['content'])


    #对话完成之后存储历史对话文件
    # 转换为字符串
    data = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])
    # 存储为文本文件
    with open(address, 'w', encoding='utf-8') as file:
        file.write(data)
    print("数据已存储为文本文件。")



def agent_answer(address, user_input, model):
    
    # 初始化一个空列表来存储恢复的对话历史
    conversation_history = []
    # 从文本文件中读取数据
    with open(address, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行末的换行符
            line = line.strip()
            # 查找第一个冒号的位置
            colon_index = line.find(':')
            if colon_index != -1:
                # 提取 role 和 content
                role = line[:colon_index].strip()
                content = line[colon_index + 1:].strip()
                # 将解析后的数据添加到列表中
                conversation_history.append({"role": role, "content": content})



    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 获取模型响应
    response = ollama.chat(
        model=model,  # 使用 gemma2:2b 模型
        stream=False,  # 将 stream=True 可实现流式输出
        messages=conversation_history,  # 传递对话历史作为列表
        options={"temperature": 0.7}
    )

    # 将模型响应添加到对话历史
    conversation_history.append({"role": "assistant", "content": response['message']['content']})



    #对话完成之后存储历史对话文件
    # 转换为字符串
    data = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])
    # 存储为文本文件
    with open(address, 'w', encoding='utf-8') as file:
        file.write(data)
    print("数据已存储为文本文件。")


    return response['message']['content']

# chat_with_model(address='conversation.txt', model='llava:latest')

# agent_answer(address='conversation.txt',user_input=encode_image_to_base64("wxauto文件\微信图片_20240820144758.jpg"), model='llava:latest')

