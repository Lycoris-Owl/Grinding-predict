import numpy as np
import pandas as pd

np.random.seed(26)

num_samples = 30

# 先以软铝合金进行精磨为例生成数据
# 硬度
x1 = np.random.uniform(20, 40, num_samples)
# 原始粗糙度
x2 = np.random.uniform(0.5, 1.5, num_samples)
# 热导率
x3 = np.random.uniform(150, 200, num_samples)
# 弹性模量
x4 = np.random.normal(70, 1, num_samples)
# 屈服强度
x5 = np.random.uniform(30, 100, num_samples)
# 延伸性
x6 = np.random.uniform(15, 25, num_samples)
# 期望粗糙度 取0.1-1.0随机值但小于对应原始粗糙度
x7 = []
for x2_one in x2:
    while True:
        x7_one = np.random.uniform(0.1, 1.0)
        if x7_one < x2_one:
            break
    x7.append(x7_one)
x7 = np.array(x7)

# 给定每一个因变量满足的映射

# 磨料粒度
y2_raw = 0.8*x2 + 0.5*np.sqrt(x5) + 0.8*(x6**2) + 1.0*x7 - 0.3

# 打磨力度
y3_raw = 1.1*np.sqrt(x1) + 0.8*x2 + 0.1*x3 + 0.2*x4 + 0.5*x5 - 0.8*np.sqrt(x6) - 0.3*x7 + 0.2

# 打磨表面速度
y4_raw = 0.5*x1 + 0.1*x2 + 0.8*np.sqrt(x3) + 0.1*x5 - 0.1*x6 - 0.7*np.sqrt(x7) + 10.0

# 磨料选择 离散值，使用输入的加权来确定，给出每种磨料的权重函数
# x / x_mean
unit_x1 = x1 / np.mean(x1)
unit_x2 = x2 / np.mean(x2)
unit_x3 = x3 / np.mean(x3)
unit_x4 = x4 / np.mean(x4)
unit_x5 = x5 / np.mean(x5)
unit_x6 = x6 / np.mean(x6)
unit_x7 = x7 / np.mean(x7)
# 1 2 3 4 5磨料权重
y1_1 = unit_x1 + unit_x3 + unit_x5
y1_2 = unit_x1 + unit_x2 + unit_x3
y1_3 = unit_x2 + unit_x4 + unit_x6
y1_4 = unit_x5 + unit_x6 + unit_x7
y1_5 = unit_x2 + unit_x4 + unit_x5 + unit_x7 - unit_x6
# y1取权重最高的磨料编号
y1 = []
for i in range(0, num_samples):
    y1_list = np.array([y1_1[i], y1_2[i], y1_3[i], y1_4[i], y1_5[i]])
    y1_max = y1_list.max()
    for ii in range(0, 5):
        if y1_max == y1_list[ii]:
            y1.append(ii+1)
            break

# 整理成np数组
y1 = np.array(y1)
y2 = np.array([])
y3 = np.array([])
y4 = np.array([])
# 添加噪声构成实际标签值
for i in range(0, num_samples):
    y2_noise = y2_raw[i] + np.random.uniform(-0.1, 0.1)
    y3_noise = y3_raw[i] + np.random.uniform(-0.01, 0.01)
    y4_noise = y4_raw[i] + np.random.uniform(-0.01, 0.01)
    y2 = np.append(y2, y2_noise)
    y3 = np.append(y3, y3_noise)
    y4 = np.append(y4, y4_noise)

print("x1:", '\n', x1)
print("x2:", '\n', x2)
print("x3:", '\n', x3)
print("x4:", '\n', x4)
print("x5:", '\n', x5)
print("x6:", '\n', x6)
print("x7:", '\n', x7)
print("y1:", '\n', y1)
print("y2:", '\n', y2)
print("y3:", '\n', y3)
print("y4:", '\n', y4)

data = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3, "x4": x4, "x5": x5, "x6": x6, "x7": x7, "y1": y1, "y2": y2, "y3": y3, "y4": y4})
print(data.head())
