# 一、YOLOv1输出结构概述

将输入图片分成 $S \times S$ 个网格，每个网格预测（$B$个）bounding box（边界框）及其置信度，并预测类别概率。

每个 grid cell 输出：

- $B$ 个Box，每个包含：($x$, $y$, $w$, $h$, $confidence$)
    - $(x, y)$: bbox中心在cell内的相对坐标
    - $(w, h)$: bbox的宽高相对于整张图进行归一化
    - $confidence$: 置信度=有无物体 × IoU(预测框, 真值框)
- $C$种类别的概率（classification）

总输出向量维数：$S \times S \times [B \times 5 + C]$

#  二、YOLOv1总损失函数公式

YOLOv1损失函数是多任务损失（回归+分类+置信度），它有四部分：

$$

\begin{aligned}
L = &\; \lambda_{coord} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{obj} \left[ (x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2 \right]  \\
+ &\; \lambda_{coord} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{obj} \left[ (\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2 \right]  \\
+ &\; \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{obj} (C_i - \hat{C}_i)^2  \\
+ &\; \lambda_{noobj} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{noobj} (C_i - \hat{C}_i)^2 \\
+ &\; \sum_{i=0}^{S^2} \mathbb{1}_i^{obj} \sum_{c=1}^{C} (p_i(c) - \hat{p}_i(c))^2
  \end{aligned}
$$

**变量说明：**

- $\mathbb{1}_{ij}^{obj}$：第i个cell的第j个box是否负责 本cell内的目标（只有一个box负责），为1时计算该损失
- $\mathbb{1}_{ij}^{noobj}$：没有目标时为1
- $\hat{x}_i, \hat{y}_i, \hat{w}_i, \hat{h}_i, \hat{C}_i, \hat{p}_i(c)$：预测值
- $x_i, y_i, w_i, h_i, C_i, p_i(c)$：真实值
- $\lambda_{coord}$：位置损失的权重（默认5）
- $\lambda_{noobj}$：无目标置信度损失的权重（默认0.5）
- $C_i$：预测置信度（有物体 × IoU）
- $p_i(c)$：预测类别概率


# 三、每项损失的推导依据及公式细节

1. **坐标回归损失**
    - 只计算负责预测真实物体的box（IoU最大的box）。
    - 采用MSE对(x, y)和($\sqrt{w}$, $\sqrt{h}$)，注意宽高用开方，为了平衡大框和小框的梯度。
2. **置信度损失**
    - 有目标与无目标的置信度分别加权。置信度理应等于IoU(预测框, 真框)，没有目标时应为0。
3. **分类损失**
    - 只对有目标的cell计算，分类采用softmax后的one-hot标签和网络输出做MSE。



# 四、YOLOv1各损失作用（总结）

- **loc loss** (位置损失): 保证预测框能覆盖目标
- **conf loss** (置信度损失): 保证分辨哪里是目标，哪里不是
- **class loss** (分类损失): 保证类别预测准确

