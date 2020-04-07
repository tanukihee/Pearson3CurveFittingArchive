import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import probscale
import scipy.stats as stats
from scipy.optimize import curve_fit
from scipy.stats import pearson3

matplotlib.use("pgf")
plt.rcParams.update({
    "pgf.rcfonts":
    False,
    "pgf.preamble": [
        "\\usepackage{xeCJK}",
        "\\usepackage{amsmath}",
        "\\usepackage{siunitx}",
        "\\sisetup{detect-all}"
        "\\usepackage{unicode-math}",
        "\\setsansfont{FiraGO}"
        "\\setmathfont{Fira Math}"
        "\\setCJKsansfont{Source Han Sans CN}",
    ],
})


class Data:
    """
    # 水文数据类

    ## 构造函数参数
    
    + `arr`：实测水文数据
    """
    def __init__(self, arr):
        self.arr = np.sort(arr)[::-1]
        # 降序排序输入数组
        self.n = len(arr)
        # 实测期长度
        self.extremeNum = 0
        # 特大洪水数

    def history(self, arr, length, num=0):
        """
        # 历史洪水数据
        
        ## 输入参数
        
        + `arr` 历史特大洪水序列，均为特大洪水

        + `length` 调查期长度
        
        + `num` 特大洪水数，包括历史特大洪水与实测特大洪水，默认为历史特大洪水数
        """
        self.historia = np.sort(arr)[::-1]
        # 历史洪水序列
        self.length = length
        # 调查期长度
        self.extremeNum = np.max(len(self.historia), num)
        # 特大洪水数
        self.extremeNumInMeasure = self.extremeNum - len(arr)
        # 实测期特大洪水数

        # 特大洪水序列与一般洪水序列
        self.extreme = self.historia
        self.ordinary = self.arr
        if self.extremeNumInMeasure > 0:
            for i in range(self.extremeNumInMeasure):
                self.extreme = np.append(self.extreme, self.arr[i])
            self.ordinary = np.delete(self.arr,
                                      range(self.extremeNumInMeasure))

        self.arr = np.sort(np.append(self.extreme, self.ordinary))[::-1]

    def figure(self, grid=True, logVert=False):
        """
        # 绘制图形
        
        ## 输入参数
        
        + `gird`：是否显示背景网格，默认为 `True`
        
        + `logVert`：纵坐标是否为对数坐标，默认为 `False`
        
        + `font`：标签字体，默认为更纱黑体 CL
        """
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        # 创建「画板」与「画布」

        self.ax.set_xscale("prob")
        # 横坐标改为概率坐标

        self.ax.set_xlabel(r"频率 $P$（%）")
        self.ax.set_ylabel(r"流量 $Q$（\si{m\cubed /s}）")

        self.ax.grid(grid)
        # 背景网格

        if logVert:
            self.ax.set_yscale("log")

    def empiScatter(self):
        """
        # 点绘经验概率点
        """
        # 数学期望公式计算经验概率
        if self.extremeNum == 0:
            self.empiProb = (np.arange(self.n) + 1) / (self.n + 1) * 100
        else:
            self.extremeProb = (np.arange(self.extremeNum) +
                                1) / (self.length + 1) * 100
            self.ordinaryProb = self.extremeProb[-1] + (
                100 - self.extremeProb[-1]) * (
                    np.arange(self.n - self.extremeNumInMeasure) +
                    1) / (self.n - self.extremeNumInMeasure + 1)
            self.empiProb = np.append(self.extremeProb, self.ordinaryProb)

        # 画布坐标轴设置
        if self.empiProb[0] > 1:
            self.probLimLeft = 1
        else:
            self.probLimLeft = 10**(np.ceil(np.log10(self.empiProb[0])) - 1)
        self.probLimRight = 100 - self.probLimLeft
        self.ax.set_xlim(self.probLimLeft, self.probLimRight)

        # 点绘经验概率
        if self.extremeNum == 0:
            self.ax.scatter(self.empiProb,
                            self.arr,
                            marker="o",
                            c="none",
                            edgecolors="k",
                            label="经验概率点")
        else:
            self.ax.scatter(self.ordinaryProb,
                            self.ordinary,
                            marker="o",
                            c="none",
                            edgecolors="k",
                            label="一般洪水经验概率点")
            self.ax.scatter(self.extremeProb,
                            self.extreme,
                            marker="x",
                            c="k",
                            label="特大洪水经验概率点")

    def statParams(self, output=True):
        """
        # 输出数据的统计参数
        
        ## 输入参数
        
        + `output`：是否在控制台输出参数，默认为 True
        """
        if self.extremeNum == 0:
            self.expectation = np.mean(self.arr)
            # 期望
            self.modulusRatio = self.arr / self.expectation
            # 模比系数
            self.coeffOfVar = np.sqrt(
                np.sum((self.modulusRatio - 1)**2) / (self.n - 1))
            # 变差系数

        else:
            self.expectation = (np.sum(self.extreme) +
                                (self.length - self.extremeNum) /
                                (self.n - self.extremeNumInMeasure) *
                                np.sum(self.ordinary)) / self.length
            self.coeffOfVar = (np.sqrt(
                (np.sum((self.extreme - self.expectation)**2) +
                 (self.length - self.extremeNum) /
                 (self.n - self.extremeNumInMeasure) * np.sum(
                     (self.ordinary - self.expectation)**2)) /
                (self.length - 1))) / self.expectation

        self.coeffOfSkew = stats.skew(self.arr, bias=False)
        # 偏态系数
        if output:
            print("期望 EX 为 %.2f" % self.expectation)
            print("变差系数 Cv 为 %.4f" % self.coeffOfVar)
            print("偏态系数 Cs 为 %.4f" % self.coeffOfSkew)

    def momentPlot(self):
        """
        # 绘制矩法估计参数理论概率曲线
        """
        x = np.linspace(self.probLimLeft, self.probLimRight, 1000)
        theoY = (pearson3.ppf(1 - x / 100, self.coeffOfSkew) * self.coeffOfVar
                 + 1) * self.expectation

        self.ax.plot(x, theoY, "--", lw=1, label="矩法估计参数概率曲线")
        # 绘制理论曲线

    def plotFitting(self, svRatio=0, EXFitting=True, output=True):
        """
        # 优化适线
        
        ## 输入参数

        + `svRatio`：倍比系数，即偏态系数 `Cs` 与 变差系数 `Cv` 之比。
        
            默认为 0，即关闭倍比系数功能。
        
            - 当 `svRatio` ≠ 0 时，Cs 不参与适线运算中，且 `Cs` = `svRatio` × `Cv`；

            - 当 `svRatio` = 0 时，Cs 正常参与适线运算。

        + `EXFitting`：适线时是否调整 EX，默认为 True

        + `output`：是否在控制台输出参数，默认为 True
        """

        if svRatio == 0:
            if EXFitting:
                p3 = lambda prob, ex, cv, cs: (pearson3.ppf(
                    1 - prob / 100, cs) * cv + 1) * ex

                [self.fitEX, self.fitCV, self.fitCS], pcov = curve_fit(
                    p3, self.empiProb, self.arr,
                    [self.expectation, self.coeffOfVar, self.coeffOfSkew])

            else:
                p3 = lambda prob, cv, cs: (pearson3.ppf(1 - prob / 100, cs) *
                                           cv + 1) * self.expectation

                [self.fitCV, self.fitCS
                 ], pcov = curve_fit(p3, self.empiProb, self.arr,
                                     [self.coeffOfVar, self.coeffOfSkew])

                self.fitEX = self.expectation

        else:
            if EXFitting:
                p3 = lambda prob, ex, cv: (pearson3.ppf(
                    1 - prob / 100, cv * svRatio) * cv + 1) * ex

                [self.fitEX, self.fitCV
                 ], pcov = curve_fit(p3, self.empiProb, self.arr,
                                     [self.expectation, self.coeffOfVar])

            else:
                p3 = lambda prob, cv: (pearson3.ppf(
                    1 - prob / 100, cv * svRatio) * cv + 1) * self.expectation

                [self.fitCV], pcov = curve_fit(p3, self.empiProb, self.arr,
                                               [self.coeffOfVar])

                self.fitEX = self.expectation

            self.fitCS = self.fitCV * svRatio

        if output:
            print("适线后")
            print("期望 EX 为 %.2f" % self.fitEX)
            print("变差系数 Cv 为 %.4f" % self.fitCV)
            print("偏态系数 Cs 为 %.4f" % self.fitCS)

    def fittedPlot(self):
        """
        # 绘制适线后的概率曲线
        
        """

        x = np.linspace(self.probLimLeft, self.probLimRight, 1000)
        theoY = (pearson3.ppf(1 - x / 100, self.fitCS) * self.fitCV +
                 1) * self.fitEX

        self.ax.plot(x, theoY, lw=2, label="适线后概率曲线")
        # 绘制理论曲线

    def prob2Value(self, prob):
        """
        # 由设计频率转换设计值
        
        ## 输入参数
        
        + `prob`：设计频率，单位百分数
        
        ## 输出参数
        
        + `value`：设计值
        """

        value = (pearson3.ppf(1 - prob / 100, self.fitCS) * self.fitCV +
                 1) * self.fitEX

        print("%.4f%% 的设计频率对应的设计值为 %.2f" % (prob, value))

        return value

    def value2Prob(self, value):
        """
        # 由设计值转换设计参数
        
        ## 输入参数
        
        + `value`：设计值
        
        ## 输出参数
        
        + `prob`：设计频率，单位百分数
        """
        prob = 100 - pearson3.cdf(
            (value / self.fitEX - 1) / self.fitCV, self.fitCS) * 100

        print("%.2f 的设计值对应的设计频率为 %.4f%%" % (value, prob))

        return prob


def successive():
    data = Data(
        np.array([
            680.6, 468.4, 489.2, 450.6, 436.8, 586.2, 567.9, 473.9, 357.8,
            650.9, 391, 201.2, 452.4, 750.9, 585.2, 304.5, 370.5, 351, 294.8,
            360.9, 276, 549.1, 534, 349, 350, 372, 292, 485, 427, 620.8, 539,
            474, 292, 228, 357, 425, 365, 241, 267, 305, 306, 238.9, 277.3,
            170.8, 217.9, 208.5, 187.9
        ]))
    # 本例取自《工程水文学》（2010 年第 4 版，詹道江 徐向阳 陈元芳 主编）P150～151 表 6-3

    data.figure()
    data.empiScatter()
    data.statParams()
    data.momentPlot()
    data.plotFitting()
    data.fittedPlot()

    data.ax.legend()

    plt.tight_layout(0.5)
    plt.savefig("successive.pdf")


def nonsuccessive():
    data = Data(
        np.array([
            1800, 530, 590, 1460, 2440, 490, 1060, 1790, 1480, 2770, 1420, 410,
            7100, 2200, 3400, 1300, 3080, 946, 430, 857, 421, 4500, 2800, 846,
            1400, 1100, 740, 3600, 1470, 690
        ]))
    data.history(np.array([9200]), 100, 2)
    # 本例取自《工程水文学》（1992 年第 2 版，王燕生 主编）P203 例 10-2

    data.figure()
    data.empiScatter()
    data.statParams()
    data.momentPlot()
    data.plotFitting()
    data.fittedPlot()

    data.ax.legend()

    plt.tight_layout(0.5)
    plt.savefig("nonsuccessive.pdf")


if __name__ == "__main__":
    successive()
    nonsuccessive()