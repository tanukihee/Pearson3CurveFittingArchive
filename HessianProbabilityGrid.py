import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats

from scipy.stats import pearson3
from scipy.stats import gamma
from scipy.stats import norm

plt.rcParams['font.sans-serif'] = ['Sarasa Gothic CL']
# 更纱黑体

fig, ax = plt.subplots()

# 定义横坐标标线
# ！可以自己改
axisProb = np.array([.01, .1, .2, .5, 1, 2, 5, 10, 20,
                     50, 80, 90, 95, 98, 99, 99.5, 99.8, 99.9, 99.99])
axisX = norm.ppf(axisProb/100)

# 画横向分划线
for i in np.arange(len(axisX)):
    plt.axvline(axisX[i], lw=0.5, color='grey')

plt.grid(True, axis='y')
# y 轴坐标线
ax.set_xticks([])
# 去掉 x 轴刻度

ax.set_xticks(axisX)
ax.set_xticklabels(axisProb, fontsize='smaller')
ax.tick_params(axis='x', rotation=45)
# 重新设置 x 轴坐标刻度

plt.xlabel('$P$ (%)')
plt.ylabel('$Q$ (m$^3$/s)')
# 横纵坐标标签


def probGrid(dataArr, estCV, estCS):
    sortedData = np.sort(dataArr)[::-1]
    # 逆序排序输入数组
    expProb = np.arange(1, len(sortedData)+1)/(len(sortedData)+1)
    # 计算经验概率
    dataX = norm.ppf(expProb)
    # 转换横坐标
    plt.scatter(dataX, sortedData, c='k', marker='x',
                label='经验概率', linewidths=0.5)
    # 点绘经验概率

    eX = np.average(dataArr)  # 期望
    K = sortedData / eX  # 模比系数
    cV = math.sqrt(np.sum((K-1)**2))/(len(sortedData)-1)  # 变差系数
    cS = np.sum((K-1)**3)/((len(sortedData)-3)*cV**3)  # 偏态系数

    x = np.linspace(0.0001, 0.9999, 10000)
    p3X = norm.ppf(x)
    # 横坐标变换
    theoY = (pearson3.ppf((1-x), estCS)*estCV+1)*eX
    plt.plot(p3X, theoY, 'r-', label='理论概率曲线')
    # 画出理论概率曲线

    # print(eX)
    # TODO 输入数据的统计参数输出


data = np.array([538.3, 624.9, 663.2, 591.7, 557.2, 998, 641.5, 341.1, 964.2, 687.3, 546.7,
                 509.9, 769.2, 615.5, 417.1, 789.3, 732.9, 1064.5, 606.7, 586.7, 567.4, 587.7, 709, 883.5])

probGrid(data, 0.3, 1)
# 6.3 题的数据

plt.legend()
plt.show()
