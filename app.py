import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
import time
import spacy
from datetime import datetime, timedelta
import pandas as pd
import re

# 导入已经训练好的模型
nlp = spacy.load("./model-best")

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)

messages = []

def threshold_table (code: str): 
    if code == 'B1E': return 10
    elif code == 'FRE': return 0 # 冰箱一直在運行
    elif code == 'HPE': return 1000
    elif code == 'BME': return 300
    elif code == 'CDE': return 500
    elif code == 'TVE': return 50
    else: return 0
    

def appliance_table (code: str): 
    if str == 'B1E': return '房間'
    elif str == 'FRE': return '冰箱'
    elif str == 'HPE': return '加熱器'
    elif str == 'BME': return '地下室'
    elif str == 'CDE': return '乾衣機'
    elif str == 'TVE': return '電視'
    
def reverse_appliance_table(name: str): 
    print('!!!!!!!!!!!!!!!!!!test', name)
    if name == '房間': return 'B1E'
    elif name == '冰箱': return 'FRE'
    elif name == '加熱器': return 'HPE'
    elif name == '熱器': return 'HPE'
    elif name == '地下室': return 'BME'
    elif name == '烘乾機': return 'CDE'
    elif name == '電視': return 'TVE'

    
def get_year_from_2013():
    # 抓取現在時間
    now = datetime.now()
    # 格式化現在時間
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # 将输入的时间字符串解析为datetime对象
    current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    
    # 使用replace方法将年份修改为2013，并将秒数设为00
    current_time2 = current_time.replace(year=2013, second=0)
    
    # 将修改后的datetime对象格式化为字符串
    current_time2_str = current_time2.strftime("%Y-%m-%d %H:%M:%S")
    
    return current_time2_str

def parse_time_string(time_str):
    now = get_year_from_2013()
    time = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    # 檢查並處理“昨天”
    if '今天' in time_str:
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 檢查並處理“昨天”
    if '昨天' in time_str:
        time = time - timedelta(days=1)
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 檢查並處理“前天”
    if '前天' in time_str:
        time = time - timedelta(days=2)
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 檢查並處理“上個月”
    if '上個月' in time_str:
        time = time - timedelta(days=30)
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 處理“YYYY-MM-DD”格式
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})', time_str)
    if match:
        time = datetime.strptime(time_str, "%Y-%m-%d")
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 處理“YYYY/M/D”格式
    match = re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})', time_str)
    if match:
        time = datetime.strptime(time_str, "%Y/%m/%d")
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 處理“X月X號”格式
    match = re.match(r'(\d{1,2})月(\d{1,2})號', time_str)
    if match:
        month, day = match.groups()
        year = time.year
        time = datetime(year, int(month), int(day))
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 處理“X/X”格式
    match = re.match(r'(\d{1,2})/(\d{1,2})', time_str)
    if match:
        month, day = match.groups()
        year = time.year
        time = datetime(year, int(month), int(day))
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    raise ValueError("未知的時間格式: " + time_str)


def get_anomaly_from_csv(date, appliance):
    print('近來得', date, type(date))
    # 打开对应设备的 txt 文件
    with open(f'./predict_list/anomaly/{appliance}_results.txt', 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 将每行按照空格分割，并取出日期和值
            parts = line.strip().split(' ')
            row_date = parts[0]
            value = parts[1]
            
            # 如果找到了对应日期的数值，则返回该数值
            if row_date + ' ' + value == date:
                return parts[2]
    
    # 如果未找到对应日期的数值，则返回 None
    return None

def get_power_from_csv(date, appliance):
    # 读取对应设备的 txt 文件
    with open(f'./predict_list/power/p_{appliance}.txt', 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 将每行按照空格分割，并取出日期和值
            parts = line.strip().split(' ')
            row_date = parts[0]
            value = parts[1]
            # print(row_date)
            # print(value)
            # print('---------')
            
            
            # 如果找到了对应日期的数值，则返回该数值
            if row_date + ' ' + value == date:
                return parts[2]
            
    # 如果未找到对应日期的数值，则返回 None
    return -1

def contains_open_or_close(text):
    # 将文本转换为小写，以便不区分大小写进行匹配
    
    # 检查字符串中是否包含'開'或'關'
    if '開' in text or '關' in text:
        return True
    else:
        return False


def return_ans (time, power, query, code, ifAnomaly):
    answer_power = ''
    answer_ano = ''
    if code == None:
        answer_power = '無此電器，請確認'
        return answer_power, answer_ano
    
    # --- 開關問題 or 功率問題 ---
    ifOpenQuery = contains_open_or_close(query)
    # 如果是開關問題：
    if ifOpenQuery:
        threshold = threshold_table(code)
        if power > threshold: answer_power = '開啟'
        else: answer_power = '關閉'
    # 如果是功率問題：
    else: 
        answer_power = power
        
        
    # --- 是否有異常 ---
    if ifAnomaly == 1 : answer_ano = '有異常'
    else: answer_ano = '無異常'
    
    return answer_power, answer_ano

# 查看数据的路由
@app.route('/members')
def members():
    return { "members": ["Member1", "Member2", "Member3"] }

# 发送消息的路由
@app.route('/send-message', methods=['POST'])
def send_message():
    # 會用到的
    # time：格式＝2013-06-03 16:18:00
    # appliance：電器中文名
    # appliance_code：對影的電器 code
    

    # --- 取得時間 ---
    now_time = get_year_from_2013() # 格式：2013-06-03 16:18:00
    print("年份改為2013的時間是:", now_time)

    # --- client 傳來的 ---
    data = request.get_json()
    message = data.get('message')
    messages.append(message)
    
    # --- 處理 NER ---
    doc = nlp(message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print('===' ,entities)
    print(entities[0])
    # --- 取出電器 NER ---
    appliance = None
    query = '使用狀況' # 預設
    time = now_time # !!!!!! 之後要套模型
    appliance_code = None
    for entity in entities:
        if entity[1] == 'Time':
            time = parse_time_string(entity[0])
            print('time:',time)
        # 如果元组的第二个元素是'Appliance'
        if entity[1] == 'Appliance':
            appliance = entity[0]
        if entity[1] == 'Query':
            query = entity[0]
    if appliance != None :
        appliance_code = reverse_appliance_table(appliance)
    else :
        print('沒有該電器')

    # --- 取出功率＆異常 ---
    extend_result = ''
    
    if appliance_code != None: 
        print('code-', appliance_code)
        power = float(get_power_from_csv(time, appliance_code))
        ifAnomaly = get_anomaly_from_csv(time, appliance_code)
        # --- get answer---
        answer_power, answer_ano = return_ans(time, power, query, appliance_code, ifAnomaly)
        extend_result = extend_message(answer_power,answer_ano, appliance, query, time)
    else :
        extend_result = '無此電器，請確認'
        answer_ano = -1
    
    to_client = {
        'message': extend_result, 
        'entities': entities, 
        'ano': answer_ano
    }
        
    # 返回预测结果给客户端
    return jsonify(to_client), 200


# 淳昇 part
## answer_power: 瓦數 or 開起/關閉
## answer_ano: ‘有異常’ or ‘無異常’
## appliance: NER- 電氣中文名稱
## query: NER- 需求
## time: NER- ex. 2013-06-03 22:40:00

def extend_message(answer_power: str, answer_ano:str , appliance: str, query: str, time: str):
    response = f"根據您的查詢，以下是 {time.replace('2013','2024')} 的 {appliance} 使用狀況：\n\n"
    response += f"使用狀況: {answer_power} 瓦\n"
    response += f"異常情況: {answer_ano}\n\n"
    response += "希望這些訊息對您有幫助。如果有其他問題，請隨時告訴我！"

    return response

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
