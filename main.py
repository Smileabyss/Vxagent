from wxauto import *
from client import agent_answer
import time
import os
import glob
import base64
# 读取图像文件并转换为二进制数据
def read_image_file(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def find_latest_image(folder_path):
    # 指定图片格式，可以根据需要扩展，比如支持更多格式
    image_types = ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp')

    # 使用 glob 搜索匹配的文件
    image_files = []
    for ext in image_types:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))

    # 如果没有找到图片，返回 None
    if not image_files:
        return None

    # 找到最新修改的图片文件
    latest_image = max(image_files, key=os.path.getmtime)
    
    return latest_image




def get_listen_list(address):
        # 初始化一个空列表来存储恢复的对话历史
        conversation_history = []
        # 从文本文件中读取数据
        with open(address, 'r', encoding='utf-8') as file:
            for line in file:
                # 去除行末的换行符
                line = line.strip()
                conversation_history.append(line)
        return conversation_history



class llm_agent():
    def __init__(self, address):
        self.wx = WeChat()
        self.listen_list = get_listen_list(address)
        print(self.listen_list)

    def listening(self, model):
        i = 0
        while i<5:
            i = 1+i
            for who in self.listen_list:
                self.wx.ChatWith(who)
                #获取user的最后一条信息
                messages = self.wx.GetAllMessage(
                            savepic   = False,   # 保存图片
                            savefile  = False,   # 保存文件
                            savevoice = True    # 保存语音转文字内容
                        )
                # print(messages)
                if len(messages) == 0:
                    continue
                all = len(messages)
                if messages[-1][0] == who:
                    i = -2
                    new_messages = messages[-1][1]
                    while i > -all:
                        if messages[i][0] == 'Self':
                            break
                        if messages[i][0] == 'SYS':
                            i= i-1
                            continue
                        # if messages[i][1][-3:0] == 'jpg':
                        #     x = find_latest_image('D:\vxagent\wxauto')
                        #     x = read_image_file(x)
                        #     new_messages = new_messages + '  描述图片内容:' + x
                        # else:
                        new_messages = new_messages + ' ' + messages[i][1]
                        i= i-1
                    # print(new_messages)
                    self.wx.SendMsg(msg=agent_answer("conversation.txt", new_messages, model) , who=who)
            time.sleep(5)

A = llm_agent(address = 'listen_list.txt')
A.listening('llava:latest')

