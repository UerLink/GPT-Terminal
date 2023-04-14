import openai

# 填写api_key
api_key = "sk-"
# ai扮演的角色
role = ""

def Load_Config():
    file = open('config.txt', 'r')
    config_dict = eval(file.read())
    file.close()
    api_key = config_dict.get("apikey",0)
    role = config_dict.get("role",0)


def chatgpt():
    openai.api_key = api_key
    print("您好! 我是ChatGPT，请输入您的问题")
    question: str = input("> ")
    question = role + question  # 将扮演信息和问题绑定
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      stream=True,
      messages=[{"role": "user", "content": question}]
    )

    collected_events = []   # 响应接收区
    stream_result = ''      # 保存流式输出的总结果
    for event in completion:
        collected_events.append(event)  # 保存事件响应
        data_dict = event.to_dict()     # 转换响应为字典
        data_openai_object = data_dict['choices'][0]    # 获取choices的值
        data_json = data_openai_object.to_dict()    # 转换openai_object为字典
        data_openai_object = data_json['delta']     # 获取delta的值
        finish_reason = data_json['finish_reason']  # 获取finish的值,用于判断是否传输结束
        data_json = data_openai_object.to_dict()    # 转换openai_object为字典
        segmental_result = data_json.get('content', "null")  # 获取content的值，如果没有就返回null

        if(segmental_result != "null"):     # 判断“分段结果”内是否有内容，有就输出
            print(segmental_result, end="")     # 输出“分段结果“的内容
        else:
            if (finish_reason == "stop"):   # 检测到stop值就表示流式传输发送完成
                print("\n")

# 运行
if __name__ == "__main__":
    chatgpt()