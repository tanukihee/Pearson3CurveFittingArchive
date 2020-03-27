# 海森概率格纸

海森概率格纸的绘制，主要用于水文分析中的经验频率点与 P-III 曲线的绘制。

感谢[叶浩](https://github.com/yehao1999)同学，格纸的产生离不开他的帮助。本身能凑合着用就行，只是 MATLAB 为商业软件，源代码亦可能有著作权纠纷，只能用 py 重构，也算是响应科研 py 化的号召吧。

## 使用之前

环境配置。 [ `numpy` ](https://numpy.org/) 、 [ `matplotlib` ](https://matplotlib.org/) 和 [ `scipy` ](https://scipy.org/) 较为常见不说，仅介绍 [ `probscale` ](https://matplotlib.org/mpl-probscale/)的安装方法。

控制台里

``` powershell
conda install mpl-probscale --channel=conda-forge
```

或

``` powershell
pip install probscale
```

即可。

## 更新日志

* 1.0

    原 MATLAB 代码的 copy，py 上有 `scipy.stats.pearson3()` 的轮子，至少不用像 MATLAB 里用 gamma 分布 `gaminv()` 倒推 P-III 分布了。

    但是概率格纸仍要手动绘制，即对横坐标值进行变换，还要去掉原 x 轴的标注。

    本来还想试试 R 语言，但不知道 R 语言里有没有成熟的轮子。

* 2.0

    python 里已有成熟的概率格纸的轮子，只是在 2800 页的文档之中确实不太好找😁。

* 2.1

    姑且把除适线外的基本功能做出来了，自拟合还要再看看（这时候又开始怀念 MATLAB 的 curve fitting 了？）……

    可视化界面有机会也会做的。

* 3.0

    适线也做出来了（只有离差平方和 OLS），暂时先摸了。

    适线谁有好算法啊……

* 3.1

    用队列重写了一下适线，原来的应该有问题。

    精度高了还是很吃内存（小数点后三位应该够了吧）。

* 3.2

    参照[这篇文章](https://zhuanlan.zhihu.com/p/93423829)与 `matplotlib` 的手册，绘图相关的代码变得更准确、更优雅？了（笑）。

* 4.0

    没错，我们至今为止所做的一切**全部木大**。只要我们不断造轮子，前方就会有别人造好的轮子。所以，不要停下来啊！

    适线部分重写，直接用 `scipy.optimize.curve_fit()` 成熟的轮子（速度和精度不知道高到哪里去了）。发现以前是我不会用而不是不好用，哭了。在此诚挚地向 `scipy` 道歉😢。

    ~~啥？你说原来 TODO 里的其他优化适线法（离差绝对值 ABS 和相对离差平方和 WLS）？别人都有轮子了还问我干嘛？~~

* 4.1

    添加设定倍比系数功能。

## TODO

* 可视化界面与封装

* 不连续样本（有特大值）

