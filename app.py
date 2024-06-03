import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
import time
import spacy
from datetime import datetime
import pandas as pd

# 导入已经训练好的模型
nlp = spacy.load("./model-best")

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)

messages = []

def threshold_table (code: str): 
    if code == 'B1E': return 0
    elif code == 'FRE': return 500
    elif code == 'HPE': return 0
    elif code == 'BME': return 0
    elif code == 'CDE': return 0
    elif code == 'TVE': return 0
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
            # 将每行按照制表符分割，并取出日期和值
            parts = line.strip().split('\t')
            row_date = parts[0]
            value = parts[1]
            
            # 如果找到了对应日期的数值，则返回该数值
            if row_date == date:
                return value
    
    # 如果未找到对应日期的数值，则返回 None
    return -1

def contains_open_or_close(text):
    # 将文本转换为小写，以便不区分大小写进行匹配
    
    # 检查字符串中是否包含'開'或'關'
    if '開' in text or '關' in text:
        return True
    else:
        return False

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
    time = get_year_from_2013() # 格式：2013-06-03 16:18:00
    print("年份改為2013的時間是:", time)

    # --- client 傳來的 ---
    data = request.get_json()
    message = data.get('message')
    messages.append(message)
    
    # --- 處理 NER ---
    doc = nlp(message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print('===' ,entities)
    
    # --- 取出電器 NER ---
    appliance = None
    query = None
    appliance_code = None
    for entity in entities:
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
    if appliance_code != None: 
        print('code-', appliance_code)
        power = float(get_power_from_csv(time, appliance_code))
        ifAnomaly = get_anomaly_from_csv(time, appliance_code)
    else :
        print('沒有該電器，所以無法找值')
        
    # --- DEFINE 要回傳的 ---
    answer_power = ''
    answer_ano = ''

    # --- 回傳 開關 or 功率 ---
    ifOpenQuery = contains_open_or_close(query)
    
    
    # answer_power: 如果是問開/關的話
    if ifOpenQuery:
        threshold = threshold_table(appliance_code)
        if power > threshold: answer_power = '開啟'
        else: answer_power = '關閉'
    else: 
        answer_power = power
        
    # answer_ano: 
    if ifAnomaly : answer_ano = '有異常'
    else: answer_ano = '無異常'
    
    print("result==", answer_power,answer_ano)
    
    
    # 返回预测结果给客户端
    return jsonify({'message': answer_power, 'entities': entities, 'ano': answer_ano}), 200


# 淳昇 part
@app.route('/extend-message', methods=['POST'])
def extend_message():
    # 這裡會拿到 (messages)
    # 1. 結果，如：120w, 開/關...
    # 2. ner 結果，如：[('昨天', 'Time'), ('冰箱', 'Appliance'), ('使用狀況', 'Query')]
    data = request.get_json()
    message = data.get('message')
    messages.append(message)

   
    extend_result = '' ### 處理好的內容
    # 返回预测结果给客户端
    return extend_result

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
