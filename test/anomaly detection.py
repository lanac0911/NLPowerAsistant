import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# 从CSV文件中读取数据
data = pd.read_csv('./P_BME.csv', header=None, squeeze=True).tolist()

# 定义环境状态
class Environment:
    def __init__(self, data):
        self.data = data
        self.state = 0
        self.threshold = 1  # 1表示开，0表示关
        self.max_steps = len(data)
        self.steps = 0
        self.window_size = 3  # 窗口大小，单位为分钟
        self.anomaly_steps = []  # 存储异常步骤的数组
        self.results = [0] * self.max_steps  # 初始化结果数组

    # 获取当前状态
    def get_state(self):
        return self.state

    # 获取所有异常步骤
    def get_anomaly_steps(self):
        return self.anomaly_steps

    # 执行动作
    def step(self, action):
        self.steps += 1
        reward = 0
        done = False
        
        anomaly_detected = 0
        # 如果当前状态为开
        if action == 1:
            # 检查前后各3分钟的状态
            if (self.state - self.window_size >= 0 and 
                self.state + self.window_size < self.max_steps):
                if all(self.data[i] == 0 for i in range(self.state - self.window_size, self.state)) and all(self.data[i] == 0 for i in range(self.state + 1, self.state + self.window_size + 1)):
                    reward = -1  # 异常状态的奖励设为负值
                    anomaly_detected = 1
                    self.anomaly_steps.append(self.state)  # 将异常步骤添加到数组中

        self.results[self.state] = anomaly_detected
        
        # 更新状态
        self.state += 1
        if self.state >= self.max_steps:
            done = True
        
        return self.state, reward, done

# 定义智能体
class Agent:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.q_table = np.zeros((num_states, num_actions))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    # 选择动作
    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_rate:
            return np.random.choice(self.q_table.shape[1])
        else:
            return np.argmax(self.q_table[state, :])

    # 更新Q值
    def update_q_table(self, state, action, reward, next_state):
        if next_state < self.q_table.shape[0]:  # 确保索引在边界之内
            predict = self.q_table[state, action]
            target = reward + self.discount_factor * np.max(self.q_table[next_state, :])
            self.q_table[state, action] += self.learning_rate * (target - predict)

# 定义训练函数
def train(env, agent, num_episodes=10):  # 先尝试10个回合
    for episode in range(num_episodes):
        start_time = time.time()
        env.state = 0  # 重置环境状态
        total_reward = 0
        done = False
        steps = 0
        while not done and steps < env.max_steps:
            state = env.get_state()
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            total_reward += reward
            steps += 1
        end_time = time.time()
        if episode % 1 == 0:  # 每个回合打印一次
            print(f"Episode {episode}/{num_episodes} - Total Reward: {total_reward} - Time taken: {end_time - start_time:.2f} seconds")
    print("Training finished.")

# 创建环境和智能体
env = Environment(data)
num_states = len(data)
num_actions = 2  # 0表示关，1表示开
agent = Agent(num_states, num_actions)

# 训练智能体
train(env, agent)

# 使用智能体进行预测
env.state = 0  # 重置环境状态
done = False
steps = 0
while not done and steps < env.max_steps:
    state = env.get_state()
    action = agent.choose_action(state)
    next_state, reward, done = env.step(action)
    steps += 1

# 保存结果为txt文件
start_time = datetime(2012, 4, 1, 7, 0, 0)
with open('results.txt', 'w') as f:
    for i, result in enumerate(env.results):
        current_time = start_time + timedelta(minutes=i)
        f.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} {result}\n")

print("Detected anomalies at steps:", env.get_anomaly_steps())
