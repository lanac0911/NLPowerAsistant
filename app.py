import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
import time
import spacy

# 导入已经训练好的模型
nlp = spacy.load("./model-best")

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)

messages = []

# 查看数据的路由
@app.route('/members')
def members():
    return { "members": ["Member1", "Member2", "Member3"] }

# 发送消息的路由
@app.route('/send-message', methods=['POST'])
def send_message():
    print('收倒')
    data = request.get_json()
    message = data.get('message')
    print('===messages1' ,message)
    messages.append(message)
    print('===messages2' ,message)

    # 处理消息并获取模型的预测结果
    doc = nlp(message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print('===' ,entities)
    
    result = {
        'nerResult': entities,
        'answer': ''
    }
    
    # 返回预测结果给客户端
    return jsonify({'message': '120w', 'entities': entities}), 200


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
