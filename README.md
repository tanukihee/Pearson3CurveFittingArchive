# 皮尔逊 III 型曲线绘制与适线

## **_注意：[`pearson3curve`](https://github.com/tanukihee/pearson3curve) v1.0.0 已更新，此仓库将作为旧版本仓库归档，并不再更新。旧版本的版本号统一视作v0.x.y_**

皮尔逊 III 型曲线绘制与适线，主要用于水文分析与水利计算。

感谢[叶浩](https://github.com/yehao1999)同学，概率格纸的产生离不开他的帮助。本身能凑合着用就行，只是 MATLAB 为商业软件，源代码亦可能有著作权纠纷，只能用 py 重构，也算是响应科研 py 化的号召吧。

## 使用之前

环境配置。 [ `numpy` ](https://numpy.org/) 、 [ `matplotlib` ](https://matplotlib.org/) 和 [ `scipy` ](https://scipy.org/) 较为常见不说，仅介绍 [ `probscale` ](https://matplotlib.org/mpl-probscale/)的安装方法。

控制台里

```powershell
conda install mpl-probscale --channel=conda-forge
```

或

```powershell
pip install probscale
```

即可。

4.2 版本后另需要 LaTeX 引擎，推荐使用 Tex Live。

## 更新日志

- 1.0

  原 MATLAB 代码的 copy，py 上有 `scipy.stats.pearson3()` 的轮子，至少不用像 MATLAB 里用 gamma 分布 `gaminv()` 倒推 P-III 分布了。

  但是概率格纸仍要手动绘制，即对横坐标值进行变换，还要去掉原 x 轴的标注。

  本来还想试试 R 语言，但不知道 R 语言里有没有成熟的轮子。

- 2.0

  python 里已有成熟的概率格纸的轮子，只是在 2800 页的文档之中确实不太好找 😁。

- 2.1

  姑且把除适线外的基本功能做出来了，自拟合还要再看看（这时候又开始怀念 MATLAB 的 curve fitting 了？）……

  可视化界面有机会也会做的。

- 3.0

  适线也做出来了（只有离差平方和 OLS），暂时先摸了。

  适线谁有好算法啊……

- 3.1

  用队列重写了一下适线，原来的应该有问题。

  精度高了还是很吃内存（小数点后三位应该够了吧）。

- 3.2

  参照[这篇文章](https://zhuanlan.zhihu.com/p/93423829)与 `matplotlib` 的手册，绘图相关的代码变得更准确、更优雅？了（笑）。

- 4.0

  没错，我们至今为止所做的一切**全部木大**。只要我们不断造轮子，前方就会有别人造好的轮子。所以，不要停下来啊！

  适线部分重写，直接用 `scipy.optimize.curve_fit()` 成熟的轮子（速度和精度不知道高到哪里去了）。发现以前是我不会用而不是不好用，哭了。在此诚挚地向 `scipy` 道歉 😢。

  ~~啥？你说原来 TODO 里的其他优化适线法（离差绝对值 ABS 和相对离差平方和 WLS）？别人都有轮子了还问我干嘛？~~

- 4.1

  添加设定倍比系数功能。

- 4.2

  为更加美观地显示中文，将 TeX 引擎更换为 pgf 的 XeLaTeX。生成的 pdf 文件可以使用终端的 `dvisvgm` 命令转化为 svg 文件（该命令不支持中文路径与中文文件名）。

  中文字体使用[思源黑体 SC](https://github.com/adobe-fonts/source-han-sans)，西文字体使用 [FiraGO](https://github.com/bBoxType/FiraGO)，数学字体使用 [Fira Math](https://github.com/firamath/firamath)。

- 4.3

  添加设定是否对期望 _EX_ 进行调整的功能。去掉数学期望公式外的其他经验频率计算方法。

- 5.0

  添加对不连序样本（有特大值）进行计算功能。更换示例。

- 5.1

  添加实验性功能 `constrained_layout` 。

- 5.2

  不一定对称的坐标轴极限。

- 5.3

  增加 `transparent=True` 选项，绘制出透明背景图像。

- 5.4

  现有的设定 `rcParams` 语法即将失效，改而使用更新的 `self[key] = other[key]` 语法。

- 5.5

  修复 v4.2 使用 pgf 引擎所带来的不兼容性问题。现可以在代码开始处通过设定 `USE_TEX` 进行引擎选择。使用自带引擎时请注意修改坐标轴标签。

- 5.6

  使用字符串设定 `rcParams` ，放弃元组。

- 6.0

  修正命名规范

- 6.1

  增加手动设置所有洪水频率功能。

## TODO

- 可视化界面与封装

- 设置部分洪水频率功能

---

Copyright (c) 2020 -- 2021 ListLee
