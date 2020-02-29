import matplotlib.pyplot as plt
import probscale
import numpy as np
import scipy.stats as stats

from scipy.stats import pearson3

fig, ax = plt.subplots()

plt.rcParams['font.sans-serif'] = ['Sarasa Gothic CL']
# 更纱黑体

ax.set_xlim(0.5, 99.5)
# ！设置横坐标极限，可以更改
ax.set_xscale('prob')
# 横坐标改为概率坐标
plt.grid(True)
# 背景网格


def probGrid(dataArr, estCV, estCS):
    '''
    dataArr：水文数据
    estCV：变差系数估值
    estCS：偏态系数估值
    '''
    sortedData = np.sort(data)[::-1]
    # 逆序排序输入数组
    expProb = np.arange(1, len(sortedData)+1)/(len(sortedData)+1)*100
    # 计算经验概率
    plt.scatter(expProb, sortedData, marker='x', label='经验概率点')
    # 点绘经验概率

    eX = np.average(data)
    # 期望
    K = sortedData/eX
    # 模比系数
    cV = np.sqrt(np.sum((K-1)**2))/(len(sortedData)-1)
    # 变差系数
    cS = np.sum((K-1)**3)/((len(sortedData)-3)*cV**3)
    # 偏态系数

    x = np.linspace(1, 99, 1000)
    theoY = (pearson3.ppf(1-x/100, estCS)*estCV+1)*eX

    plt.plot(x, theoY, 'r-', lw=2, label='理论概率曲线')
    # 绘制理论曲线

    plt.legend()
    plt.show()

    # TODO 统计参数的输出


data = np.array([538.3, 624.9, 663.2, 591.7, 557.2, 998, 641.5, 341.1, 964.2, 687.3, 546.7,
                 509.9, 769.2, 615.5, 417.1, 789.3, 732.9, 1064.5, 606.7, 586.7, 567.4, 587.7, 709, 883.5])
# 6.3 题的数据

probGrid(data, 0.3, 1)
