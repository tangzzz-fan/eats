# Transformer与注意力机制：写给高中生的入门指南

Transformer 是现在几乎所有 AI 大模型（ChatGPT、Claude、DeepSeek……）的心脏。它干的事情一句话就能说完：**让电脑读懂一段话里每个词和其他词的关系，然后一个词一个词地生成通顺的文字**。而它成功的关键，是一个叫"注意力机制（Attention）"的发明。

整篇教程我们会用一个贯穿始终的比喻：**你去图书馆查资料写论文**。你会看到，Transformer 理解句子的方式，和一个聪明的学生查资料的方式，惊人地相似。

---

## 先建立直觉

想象你在学校的食堂里吃饭，周围几百人同时说话，吵成一锅粥。但神奇的是，你依然能听清对面朋友讲的话——你的大脑自动把朋友的说话声"调高音量"，把其他噪音"调低音量"。

这就是"注意力"：人脑不可能同时处理所有信息，所以它学会了一件事——**有选择地聚焦**。

电脑读句子也面临同样的问题。看这句话：

> "小明把书借给了小红，因为**他**已经看完了。"

这里的"他"指谁？你一眼就知道是小明。但电脑怎么知道？它必须让"他"这个词去"关注"前面的"小明"，而不是"小红"或"书"。**注意力机制，就是教电脑给每个词分配"该看谁、看多重"的一套数学方法。**

那为什么不用更老的 RNN（循环神经网络，一种按顺序逐词读文本的老模型）呢？因为 RNN 像"传话游戏"：一句话从左到右一个词一个词往后传，传到第 50 个词时，第 1 个词的信息早就模糊不清了。而且传话必须排队，没法让几千台机器同时干活。Transformer 用注意力机制让每个词**直接和其他所有词对话**，不用排队传话——记得牢，还能并行计算，于是 RNN 就被淘汰了。

---

## 知识地图

| 核心知识点 | 一句话概括 |
| :--- | :--- |
| 词嵌入（Embedding） | 把每个词变成一串数字（向量），让意思相近的词数字也相近 |
| Q / K / V | 每个词扮三个角色：提问的 Query、贴标签的 Key、装内容的 Value |
| 缩放点积 + Softmax | 用点积算"匹配度"，缩放防数值爆炸，Softmax 把得分变成比例 |
| 加权汇总 | 按关注比例混合所有词的内容，每个词"吸收"了上下文 |
| 多头注意力 | 让好几组"眼睛"同时从不同角度读同一句话 |
| 自回归生成 | 每次只预测下一个词，再把它拼回去继续猜，像接龙 |
| 为什么取代 RNN | 不排队传话、记得住远距离的词、可以大规模并行训练 |

---

## 重点逐个讲

### 一、词嵌入：把词翻译成数字

**生活比喻**：图书馆给每本书一个索书号。索书号不是乱编的——同类书号码相近，小说区挨着小说区。这样管理员一看号码就知道两本书"是不是一家"。

**直觉解释**：电脑只认识数字，不认识"苹果"两个字。所以第一步是把每个词变成一串数字，这串数字叫**词向量（word vector）**，这个转换过程叫**词嵌入（Embedding）**。关键在于：这些数字不是随便编的，而是通过训练学出来的，学完之后意思相近的词，数字串也相近——"国王"和"女王"的数字很像，"苹果"和"香蕉"的数字很像，但"苹果"和"汽车"就差得很远。

**最小例子**：用一个字典模拟这个"查表"过程（真实的嵌入表有几万行、每行几百个数字，但原理完全一样）：

```python
# 一张微型的"嵌入表"：每个词对应 2 个数字（真实模型里是几百个）
embedding = {"国王": [0.9, 0.8], "女王": [0.85, 0.75], "香蕉": [0.1, 0.2]}

def 距离(a, b):  # 两串数字差得越小，意思越相近
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

print(round(距离(embedding["国王"], embedding["女王"]), 2))  # 0.1 → 很像
print(round(距离(embedding["国王"], embedding["香蕉"]), 2))  # 1.4 → 差很远
```

**一句话总结**：词嵌入就是把每个词变成一个"数字坐标"，让电脑能用数学方式比较词与词的意思。

---

### 二、Q / K / V：每个词的三种身份

**生活比喻**：回到图书馆。你想写论文《机器人的运动路径》，你会：

- 在检索框里输入**查询词**——这是 **Query（Q，查询）**；
- 系统把你的查询词和每本书的**书名/标签**比对——这是 **Key（K，键/标签）**；
- 比对成功后，你真正借走阅读的是书的**正文内容**——这是 **Value（V，值/内容）**。

**直觉解释**：Transformer 里，句子中每个词都会同时生成 Q、K、V 三份"分身"。当模型要理解"他"这个词时：

1. "他"拿出自己的 Q 去问："谁跟我有关？"
2. 句子里每个词（包括"小明""小红""书"）都亮出自己的 K："我是主语""我是人名"……
3. Q 和每个 K 算一个匹配度，谁匹配就多看谁的 V（正文内容）。

最容易搞混的一点是：**权重由 Q 和 K 决定，但最后搬走的货物是 V**。就像你按书名搜书（Q 配 K），但你带回家读的是书的内容（V）。

**最小例子**：手算一次匹配。假设"他"的 Q 是 `[1, 0]`，"小明"的 K 是 `[0.9, 0.1]`，"小红"的 K 是 `[0.1, 0.9]`。匹配度用点积（对应位置相乘再相加）计算：

```text
"他" vs "小明"：1×0.9 + 0×0.1 = 0.9   ← 很匹配！
"他" vs "小红"：1×0.1 + 0×0.9 = 0.1   ← 不太匹配
```

**一句话总结**：Q 负责提问、K 负责被检索、V 才是真正被汇总的内容——三种身份，各司其职。

---

### 三、缩放点积与 Softmax：把匹配度变成"关注比例"

**生活比喻**：你查到了 3 本书，初步打分是 2 分、1 分、0.1 分。但你一天的阅读时间是固定的 100%，怎么分配？直觉是把分数换算成百分比：分数高的多分时间，分数低的少分，加起来正好 100%。

**直觉解释**：这正是 Softmax（一种把任意分数变成"总和为 1 的比例"的函数）干的事。它先把每个分数取 e 的指数（让差异拉开、负数变正），再除以总和。上一步 Q·K 算出的点积得分，经过 Softmax 就变成了漂亮的关注比例。

那"缩放"是怎么回事？注意一个隐患：如果每个词用 64 个数字表示，点积是 64 个乘积相加，数值很容易变得巨大。而 Softmax 遇到特别大的输入会"极端化"——最大的那个直接变成 99.99%，其他全变成 0，模型就没法微调、学不动了。所以 Transformer 规定：**先把得分除以 √d（d 是每个词的数字个数，√ 是开平方），把数值按回正常范围**。64 维就除以 8，仅此而已，但没这一步模型就训练不动。

**最小例子**：亲手把三个分数变成比例，代码可以直接运行：

```python
import math

scores = [2.0, 1.0, 0.1]               # 三本书（三个词）的原始得分
exps = [math.exp(s) for s in scores]   # 第一步：每个分数取 e 的指数
total = sum(exps)                      # 第二步：算出指数的总和
probs = [e / total for e in exps]      # 第三步：每个指数除以总和
print([round(p, 3) for p in probs])    # [0.659, 0.242, 0.099]，加起来正好是 1
```

**一句话总结**：点积量出"有多匹配"，除以 √d 防止数值爆炸，Softmax 把分数换算成加起来为 1 的关注比例。

---

### 四、加权汇总：得到"听懂了上下文"的新词向量

**生活比喻**：你按 65%、25%、10% 的时间比例精读三本书，最后写出来的论文综述，就是三本书内容的"加权混合体"——哪本看得多，综述里谁的影子就重。

**直觉解释**：拿到关注比例后，最后一步很简单：把每个词的 V（内容向量）按比例加权相加。比如"他"对"我""爱""吃"的关注比例是 0.1、0.8、0.1，那"他"的新表示就是 `0.1×V_我 + 0.8×V_爱 + 0.1×V_吃`。这个新向量不再只是孤零零的"他"，而是**揉进了上下文信息的"他"**——这就是"理解"在数学上的样子。

**最小例子**：

```python
# 假设"我""爱""吃"的 V（内容向量）各是 2 个数字
V = {"我": [1, 0], "爱": [0, 1], "吃": [1, 1]}
w = {"我": 0.1, "爱": 0.8, "吃": 0.1}   # Softmax 算出的关注比例

# 按比例加权混合：新向量 = 0.1×V我 + 0.8×V爱 + 0.1×V吃
out = [sum(w[word] * V[word][i] for word in V) for i in range(2)]
print(out)  # [0.2, 0.9] → "爱"占主导，这很合理
```

**一句话总结**：注意力 = 用关注比例对所有词的内容做加权混合，每个词因此"吸收"了上下文。

---

### 五、多头注意力：多请几位读者一起读

**生活比喻**：写论文时，你只找一个同学讨论，他可能只懂历史角度。聪明的做法是请一个小组：有人看语法、有人查事实、有人品情感，最后大家把笔记拼在一起，理解就全面了。

**直觉解释**：上面讲的整套注意力流程，叫一个"头（head）"。一个头只能捕捉一种关系——比如只发现"动词旁边有名词"。**多头注意力（Multi-Head Attention）就是把词的向量切成好几份，每个头独立跑一遍注意力**：头 1 可能关注"主语是谁"，头 2 可能关注"'他'指代谁"，头 3 可能关注"情感是褒是贬"。最后把各头的结果拼接起来，就是对句子的全面理解。注意是"切分"而不是"复制放大"：512 个数字切成 8 份，每头 64 个，算完再拼回 512，总开销几乎不变。

**最小例子**：

```text
原向量（8 个数字）:  [a1 a2 a3 a4 | b1 b2 b3 b4]
切 2 个头          →  头1 看 a1~a4，头2 看 b1~b4
各自独立算注意力   →  头1 发现"语法关系"，头2 发现"指代关系"
拼回去             →  [头1结论 | 头2结论]，又变回 8 个数字
```

**一句话总结**：多头就是"一组眼睛各看一个角度，结论拼起来"，让理解既全面又不增加多少成本。

---

### 六、自回归生成：AI 是这样"写字"的

**生活比喻**：成语接龙。你说"一马当先"，我接"先发制人"，你再接"人山人海"……每一步都只看前面已经接出来的词，猜下一个最合理的词。

**直觉解释**：GPT 这类模型生成文字的方式叫**自回归生成（Autoregressive Generation）**：模型先看你给的文字，算出下一个词的概率分布，选（或抽）一个词；然后把这个词**拼回原文**，再整体看一遍，猜下下个词……如此循环。这就是为什么你看 AI 回答问题是"一个字一个字往外蹦"——它真的就是一次只生成一个词，而且每生成一个词都要把整段话重新读一遍，所以生成没法并行。

还有个细节：模型每次给出的是一堆候选词的概率。如果每次都死板地选概率最高的（贪婪策略），文章会很无聊还容易陷入重复；如果完全随机抽，又容易胡说八道。实际做法是 **Top-K 采样**：只在概率最高的前 K 个候选里抽，兼顾质量和花样。

**最小例子**：用一个字典假装是训练好的模型，演示"预测 → 拼回去 → 再预测"的循环：

```python
# 假装这个字典是模型：给它一段文字，它告诉你下一个词
next_word = {"今天": "天气", "今天 天气": "真好", "今天 天气 真好": "！"}

text = "今天"
for _ in range(3):            # 重复 3 轮"接龙"
    word = next_word[text]    # 模型看着已有全文，猜下一个词
    text = f"{text} {word}"   # 把新词拼回去，作为下一轮的输入
print(text)                   # 今天 天气 真好 ！
```

**一句话总结**：生成 = 反复做"看全文、猜下一个词、拼回去"的循环，一次只蹦一个词。

---

## 难点与易踩的坑

### 坑 1：Q、K、V 傻傻分不清

**为什么难**：三个字母同时出现，还都来自同一个词，很容易以为它们是一回事。

**正确理解**：死死记住图书馆比喻——Q 是你输的查询词，K 是书脊上的标签，V 是书里的正文。**权重由 Q 和 K 的匹配决定，但最终被加权汇总的是 V**。面试和考试里问"注意力权重乘的是谁"，答案永远是 V。

### 坑 2：以为 Softmax 只是"除法归一化"

**为什么难**：直接把分数除以总分不也能得到比例吗？为什么要先用 `e^x` 折腾一圈？

**正确理解**：`e^x` 有两个不可替代的作用：一是把负数得分变正（不然比例会出现负数，没意义）；二是**放大差距**——2 分和 1 分只差 1，但 e² 和 e¹ 差了 4.7 倍，让"重点关注谁"更鲜明。指数化 + 归一化，两步缺一不可。

### 坑 3：忘了缩放（除以 √d）

**为什么难**：这个步骤在直觉上最不显眼，感觉"除以一个常数能有多大影响"。

**正确理解**：维度 d 越大，点积是 d 个数相加，数值天然越大。Softmax 遇到巨大输入会极端化（一个约等于 1，其余约等于 0），比例失去弹性，模型就学不动了。除以 √d 就是把得分按回"正常体温"，这是让 Transformer 能训练起来的关键小细节。

### 坑 4：以为多头是把模型变大 8 倍

**为什么难**："8 个头"听起来像 8 倍的参数和计算量。

**正确理解**：多头是**切分**原有维度，不是复制。512 维切成 8 个 64 维分别算，再拼回 512。总参数量和单个"大头"基本一样，换来的是多角度的理解能力——划算买卖，不是奢侈开销。

### 坑 5：以为 AI 生成文章是"一次想一整句"

**为什么难**：AI 的回答流畅自然，很容易以为它先在"脑子"里构思好整段话再输出。

**正确理解**：它真的只是反复猜"下一个词"，没有任何全局草稿。这解释了 AI 的两个经典毛病：说着说着跑题（每一步只看局部最优），以及速度上限（必须一个词一个词串行生成，无法跳过）。

---

## 补充知识：位置编码与 Mask

原教程省略了两个变压器里的关键部件，这里补上。它们不难，但必须知道。

### 位置编码（Positional Encoding）：告诉模型词的先后顺序

**问题**：注意力让每个词和所有词交互，但这样句子就变成了"一袋词"——"我爱你"和"你爱我"在注意力眼里一模一样，因为只是三个词的不同排列，但它们的注意力连接结构完全对称。模型需要知道词的**位置**。

**解法**：给每个位置生成一串固定的波浪状数字（正弦/余弦），加到词向量上。同一位置的编码是固定的（不需要训练），不同位置的编码天然不同——位置 1 和位置 2 的数字模式相近，位置 1 和位置 100 则完全不同。这样就给了模型"先后顺序"的感知。

```python
import numpy as np

def positional_encoding(seq_len, d_model):
    """生成位置编码矩阵，形状 (seq_len, d_model)"""
    pe = np.zeros((seq_len, d_model))
    for pos in range(seq_len):
        for i in range(0, d_model, 2):
            # 偶数维用 sin，奇数维用 cos
            # 波长随维度增大而增大，类似不同频率的波浪
            wavelength = 10000 ** (2 * i / d_model)
            pe[pos, i] = np.sin(pos / wavelength)
            pe[pos, i + 1] = np.cos(pos / wavelength)
    return pe

# 直观感受：相邻位置的编码很像，远距离位置的编码差异大
pe = positional_encoding(seq_len=10, d_model=4)
print("位置 0:", pe[0])   # [0.  1.  0.  1.]
print("位置 1:", pe[1])   # [0.84 0.54 0.01 0.99] — 第 1 个数字从 0 变到 0.84
print("位置 9:", pe[9])   # 和位置 0 差异显著
```

**一句话总结**：位置编码就是给每个词贴上"第几个"的数学标签，让模型知道词的先后顺序。

### 注意力 Mask：挡住不该看的东西

注意力机制默认让每个词看到所有其他词，但有两种情况需要"遮住"：

**1. Padding Mask（填充遮罩）**：句子长短不一，短句子后面补了 `<pad>` 占位符。`<pad>` 没有实际含义，不应该被关注。做法是：把 `<pad>` 位置的注意力得分设为负无穷（-∞），经过 Softmax 后这些位置的关注比例就变成了 0。

**2. Causal Mask（因果遮罩 / 上三角遮罩）**：训练语言模型时，让第 i 个词**只能看到它前面的词**（包括自己），不能偷看后面的词。否则模型作弊——直接把正确答案抄过来就行，根本不用学"预测"。

```python
import numpy as np

def causal_mask(seq_len):
    """生成因果遮罩：允许看到自己及左边，禁止看右边"""
    # 全 0 矩阵（0 = 允许关注）
    mask = np.zeros((seq_len, seq_len))
    # 把右上角（未来位置）设为 -∞
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            mask[i, j] = -np.inf
    return mask

# 可视化为：第 i 行第 j 列表示"第 i 个词能不能看第 j 个词"
mask = causal_mask(4)
print("因果遮罩（■=允许看，□=不许看）：")
for i in range(4):
    row = "".join("■ " if mask[i, j] == 0 else "□ " for j in range(4))
    print(f"词{i}: {row}")
# 输出：
# 词0: ■ □ □ □    ← 词0 只能看自己
# 词1: ■ ■ □ □    ← 词1 能看词0和自己
# 词2: ■ ■ ■ □    ← 词2 能看词0、词1和自己
# 词3: ■ ■ ■ ■    ← 词3 能看所有前面的词
```

**一句话总结**：Mask 就是"不许看"的标记——Pad Mask 不让看无意义的填充，Causal Mask 不让看未来的词。

---

## 注意力权重可视化：理解模型在"看"什么

这是调试 Transformer 最直观的手段。对于一个训练好的模型，提取某一层的注意力权重矩阵（形状为 `(seq_len, seq_len)`），画成热力图，你就能看到每个词在关注谁。

```python
# 概念演示：假设这是某个头的注意力权重矩阵
# 横轴 = 被关注的词，纵轴 = 提问的词
# 深色格子 = 关注度高

# "小明把书借给了小红，因为他已经看完了"
#          小  把  书  借  给  了  小   ，  因  为  他  已  经  看  完  了
#         [明] [ ] [ ] [ ] [ ] [ ] [红]             [ ]
# 小[明]   ■                       □
# 把[ ]       ■
# 书[ ]           ■
# 借[ ]               ■
# 给[ ]                   ■
# 了[ ]                       ■
# 小[红]                          ■
# ，[ ]                               ■
# 因[ ]                                   ■
# 为[ ]                                       ■
# 他[ ]   ■                                   □       ■        ← "他" 关注 "小明"！
# 已[ ]                                               ■
# 经[ ]                                                   ■
# 看[ ]                                                       ■
# 完[ ]                                                           ■
# 了[ ]                                                               ■
#                     ↑ 对角线 = 每个词关注自己
#                     ↑ "他" 那行，"小明"列的格子很亮 = 注意力在"小明"上
```

这种可视化是理解模型"在想什么"的最直接窗口。实际调试时，你可能会发现有些头在做奇怪的事——比如一个头只关注逗号和句号（标点头），另一个头全关注第一个词（"哑"头）。这些都是正常的，也说明多头机制确实带来了冗余和鲁棒性。

---

## 实战练习：手写迷你 Attention

### 练习一：纯 NumPy 手写单头注意力（20 分钟）

**任务**：不用 PyTorch 的 `nn.MultiheadAttention`，只用 NumPy 写出完整的一头注意力——从输入到输出，包括 Q、K、V 的线性变换、缩放点积、Softmax、加权汇总。

这是检验你**彻底理解**注意力机制的终极方式。

```python
import numpy as np

def softmax(x, axis=-1):
    """稳定的 Softmax 实现：先减最大值防溢出"""
    x_max = x.max(axis=axis, keepdims=True)
    e_x = np.exp(x - x_max)
    return e_x / e_x.sum(axis=axis, keepdims=True)


def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: 形状都是 (batch, seq_len, d_k)
    mask: (batch, 1, seq_len, seq_len) 或 None
    返回: (batch, seq_len, d_k)
    """
    d_k = Q.shape[-1]

    # TODO 1: 计算注意力得分
    # score = Q @ K^T / sqrt(d_k)
    # 提示: K 需要转置最后两维——怎么在 NumPy 里做？
    # K 形状 (batch, seq_len, d_k)，K^T 应该是 (batch, d_k, seq_len)

    # TODO 2: 应用 mask（如果有的话）
    # 把 mask 中为 True 的位置设为 -1e9（即负无穷的近似值）

    # TODO 3: Softmax

    # TODO 4: 用注意力权重加权汇总 V

    pass


# 测试：3 个词，每个词 4 维
np.random.seed(42)
Q = np.random.randn(1, 3, 4)  # batch=1, 3个词, 4维
K = np.random.randn(1, 3, 4)
V = np.random.randn(1, 3, 4)

output = scaled_dot_product_attention(Q, K, V)
print("输出形状:", output.shape)  # 应该是 (1, 3, 4)

# 验证：每一行（每个词）的注意力权重之和应该≈1
# 你可以加个返回权重的版本自己验证
```

<details>
<summary>点击查看答案</summary>

```python
import numpy as np

def softmax(x, axis=-1):
    x_max = x.max(axis=axis, keepdims=True)
    e_x = np.exp(x - x_max)
    return e_x / e_x.sum(axis=axis, keepdims=True)


def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]

    # 1. 计算得分: (batch, seq, d_k) × (batch, d_k, seq) → (batch, seq, seq)
    # K 转置最后两维用 transpose(0, 2, 1) 或用 swapaxes(-1, -2)
    scores = Q @ K.swapaxes(-1, -2) / np.sqrt(d_k)

    # 2. 应用 mask
    if mask is not None:
        scores = np.where(mask, -1e9, scores)

    # 3. Softmax 沿最后维（每行归一化）
    attn_weights = softmax(scores, axis=-1)

    # 4. 加权汇总 V: (batch, seq, seq) × (batch, seq, d_k) → (batch, seq, d_k)
    output = attn_weights @ V

    return output


# 测试
np.random.seed(42)
Q = np.random.randn(1, 3, 4)
K = np.random.randn(1, 3, 4)
V = np.random.randn(1, 3, 4)

output = scaled_dot_product_attention(Q, K, V)
print("输出形状:", output.shape)  # (1, 3, 4)

# 验证注意力权重每行和为 1
d_k = Q.shape[-1]
scores = Q @ K.swapaxes(-1, -2) / np.sqrt(d_k)
weights = softmax(scores, axis=-1)
print("每行权重和:", weights.sum(axis=-1))  # 应该全是 1.0

# 测试因果 mask
seq_len = 3
causal_mask = np.triu(np.ones((1, 1, seq_len, seq_len)), k=1).astype(bool)
print("\n因果 mask 形状:", causal_mask.shape)
output_masked = scaled_dot_product_attention(Q, K, V, mask=causal_mask)
print("mask 后输出形状:", output_masked.shape)  # (1, 3, 4)
```
</details>

---

### 练习二：多头注意力（15 分钟）

**任务**：在练习一的基础上，实现多头注意力。流程是：

1. 把输入的 `d_model` 维切成 `num_heads` 份（每份 `d_k = d_model / num_heads`）
2. 每个头独立做一次注意力
3. 把所有头的结果拼回去

```python
def multi_head_attention(X, W_q, W_k, W_v, W_o, num_heads=2):
    """
    X: (batch, seq_len, d_model)  输入
    W_q, W_k, W_v: (d_model, d_model)  Q/K/V 的投影矩阵
    W_o: (d_model, d_model)  输出的投影矩阵
    num_heads: 头数

    返回: (batch, seq_len, d_model)
    """
    batch, seq_len, d_model = X.shape
    d_k = d_model // num_heads

    # 1. 投影得到 Q、K、V: (batch, seq_len, d_model)
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v

    # TODO 2: 把 d_model 维拆成 (num_heads, d_k)
    # 形状变换: (batch, seq_len, d_model) → (batch, num_heads, seq_len, d_k)
    # 提示: 先 reshape 成 (batch, seq_len, num_heads, d_k)，再 transpose

    # TODO 3: 每个头独立做缩放点积注意力
    # 因为头维度在前两维，可以一次矩阵乘法完成

    # TODO 4: 合并头: (batch, num_heads, seq_len, d_k) → (batch, seq_len, d_model)
    # 提示: 先 transpose 再 reshape

    # 5. 最后的线性投影
    # output = merged @ W_o

    pass


# 测试
np.random.seed(42)
d_model, num_heads = 8, 2
X = np.random.randn(1, 4, d_model)  # 1 个句子，4 个词，每个词 8 维
W_q = np.random.randn(d_model, d_model) * 0.1
W_k = np.random.randn(d_model, d_model) * 0.1
W_v = np.random.randn(d_model, d_model) * 0.1
W_o = np.random.randn(d_model, d_model) * 0.1

output = multi_head_attention(X, W_q, W_k, W_v, W_o, num_heads=num_heads)
print("多头注意力输出形状:", output.shape)  # 应该是 (1, 4, 8)
```

<details>
<summary>点击查看答案</summary>

```python
def multi_head_attention(X, W_q, W_k, W_v, W_o, num_heads=2):
    batch, seq_len, d_model = X.shape
    d_k = d_model // num_heads

    # 1. 投影
    Q = X @ W_q  # (batch, seq_len, d_model)
    K = X @ W_k
    V = X @ W_v

    # 2. 拆成多头: (batch, seq_len, d_model) → (batch, num_heads, seq_len, d_k)
    Q = Q.reshape(batch, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)
    K = K.reshape(batch, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)
    V = V.reshape(batch, seq_len, num_heads, d_k).transpose(0, 2, 1, 3)

    # 3. 注意力: 现在 Q, K, V 是 (batch, num_heads, seq_len, d_k)
    scores = Q @ K.swapaxes(-1, -2) / np.sqrt(d_k)
    attn_weights = softmax(scores, axis=-1)
    attn_output = attn_weights @ V  # (batch, num_heads, seq_len, d_k)

    # 4. 合并头: (batch, num_heads, seq_len, d_k) → (batch, seq_len, d_model)
    attn_output = attn_output.transpose(0, 2, 1, 3)  # (batch, seq_len, num_heads, d_k)
    merged = attn_output.reshape(batch, seq_len, d_model)

    # 5. 输出投影
    output = merged @ W_o
    return output


np.random.seed(42)
d_model, num_heads = 8, 2
X = np.random.randn(1, 4, d_model)
W_q = np.random.randn(d_model, d_model) * 0.1
W_k = np.random.randn(d_model, d_model) * 0.1
W_v = np.random.randn(d_model, d_model) * 0.1
W_o = np.random.randn(d_model, d_model) * 0.1

output = multi_head_attention(X, W_q, W_k, W_v, W_o, num_heads=num_heads)
print("多头注意力输出形状:", output.shape)  # (1, 4, 8)
```
</details>

---

### 练习三：迷你自回归生成器（20 分钟）

**任务**：用练习二的注意力模块，搭一个只有一层注意力的极简语言模型。数据用你自己造的 5 句话，模型要能背下来并续写。

**脚手架**：

```python
# 极简训练数据：5 句中文（帮你直观感受整个过程）
corpus = [
    "我 爱 吃 苹果",
    "我 爱 吃 香蕉",
    "你 爱 喝 牛奶",
    "他 爱 看 电影",
    "我 喜欢 打 篮球",
]

# TODO 1: 建词表——把所有出现过的词编上号
# 需要三个特殊 token: <pad>（填充）, <sos>（句首）, <eos>（句尾）

# TODO 2: 把语料转成数字序列

# TODO 3: 搭一个 Embedding + 注意力层 + 输出层的极简模型

# TODO 4: 训练几轮（用交叉熵损失，和 MNIST 练习一样的套路）

# TODO 5: 给"我"让它续写——应该能看到"爱 吃"之类的结果
```

<details>
<summary>点击查看完整答案</summary>

```python
import numpy as np

# ---- 1. 词表 ----
corpus = [
    "我 爱 吃 苹果",
    "我 爱 吃 香蕉",
    "你 爱 喝 牛奶",
    "他 爱 看 电影",
    "我 喜欢 打 篮球",
]

words = set()
for sent in corpus:
    for w in sent.split():
        words.add(w)
words = ["<pad>", "<sos>", "<eos>"] + sorted(words)
w2i = {w: i for i, w in enumerate(words)}
i2w = {i: w for w, i in w2i.items()}
vocab_size = len(words)
print(f"词表大小: {vocab_size}")

# ---- 2. 准备训练数据 ----
# 对每句话，输入是 "<sos> + 前 n-1 词"，目标是 "原句 + <eos>"
# 例如 "我爱吃苹果" → 输入 ["<sos>","我","爱","吃","苹果"]，目标 ["我","爱","吃","苹果","<eos>"]
seqs = []
for sent in corpus:
    tokens = ["<sos>"] + sent.split() + ["<eos>"]
    ids = [w2i[t] for t in tokens]
    seqs.append(ids)

# 手动 pad 到相同长度（实际工程用 DataLoader 的 collate_fn）
max_len = max(len(s) for s in seqs)
padded = np.array([s + [w2i["<pad>"]] * (max_len - len(s)) for s in seqs])

# 输入 = 去掉最后一列，目标 = 去掉第一列
X = padded[:, :-1]
Y = padded[:, 1:]

print(f"输入形状: {X.shape}, 目标形状: {Y.shape}")
print(f"第一句输入: {[i2w[i] for i in X[0]]}")
print(f"第一句目标: {[i2w[i] for i in Y[0]]}")

# ---- 3. 极简模型：Embedding → Attention → 输出 ----
d_model = 16
num_heads = 2

# 参数初始化（小随机数）
np.random.seed(42)
E = np.random.randn(vocab_size, d_model) * 0.1     # 词嵌入表
W_q = np.random.randn(d_model, d_model) * 0.1
W_k = np.random.randn(d_model, d_model) * 0.1
W_v = np.random.randn(d_model, d_model) * 0.1
W_o = np.random.randn(d_model, d_model) * 0.1
W_out = np.random.randn(d_model, vocab_size) * 0.1  # 输出投影

# 因果 mask（让词只能看到前面的）
causal_mask = np.triu(np.ones((1, 1, max_len - 1, max_len - 1)), k=1).astype(bool)

def forward(x_ids):
    """x_ids: (batch, seq_len) → logits: (batch, seq_len, vocab_size)"""
    x = E[x_ids]  # (batch, seq_len, d_model)
    x = multi_head_attention(x, W_q, W_k, W_v, W_o, num_heads)
    logits = x @ W_out  # (batch, seq_len, vocab_size)
    return logits

# ---- 4. 训练 ----
lr = 0.05
for epoch in range(500):
    # 前向
    logits = forward(X)  # (5, seq_len, vocab_size)

    # 交叉熵损失（从 logits 手算）
    logits_max = logits.max(axis=-1, keepdims=True)
    exp_logits = np.exp(logits - logits_max)
    probs = exp_logits / exp_logits.sum(axis=-1, keepdims=True)

    # 只算非 pad 位置的损失
    mask = (Y != w2i["<pad>"])
    n_valid = mask.sum()
    # 取每个位置对正确 token 的概率，求负对数
    batch_indices = np.repeat(np.arange(X.shape[0])[:, None], X.shape[1], axis=1)
    seq_indices = np.repeat(np.arange(X.shape[1])[None, :], X.shape[0], axis=0)
    correct_probs = probs[batch_indices, seq_indices, Y]
    loss = -np.sum(np.log(correct_probs + 1e-8) * mask) / n_valid

    # 反向传播（手动计算梯度——只为了演示，真正训练请用 PyTorch！）
    # 这里简化：直接对 E 和 W_out 做梯度下降
    # dL/d(logits) = probs - one_hot(Y)
    grad_logits = probs.copy()
    grad_logits[batch_indices, seq_indices, Y] -= 1
    grad_logits *= mask[:, :, None] / n_valid

    # 更新参数
    grad_W_out = x.reshape(-1, d_model).T @ grad_logits.reshape(-1, vocab_size)
    W_out -= lr * grad_W_out

    grad_x = grad_logits @ W_out.T  # 反向传到注意力层的输入
    E[X.reshape(-1)] -= lr * grad_x.reshape(-1, d_model) * 0.1  # 简化

    if epoch % 100 == 0:
        print(f"Epoch {epoch:3d}: loss = {loss:.4f}")

# ---- 5. 续写 ----
def generate(prompt, max_new=5):
    tokens = ["<sos>"] + prompt.split()
    ids = [w2i.get(t, w2i["<pad>"]) for t in tokens]
    for _ in range(max_new):
        x = np.array([ids])
        logits = forward(x)
        next_id = logits[0, -1].argmax()  # 贪心选最大
        if next_id == w2i["<eos>"]:
            break
        ids.append(next_id)
    return " ".join(i2w[i] for i in ids if i not in [w2i["<sos>"], w2i["<pad>"]])

print("\n续写结果:")
print(f"  输入 '我' → '{generate('我')}'")
print(f"  输入 '你' → '{generate('你')}'")
print(f"  输入 '他' → '{generate('他')}'")
```
</details>

---

## 学完能做什么 & 下一步

**这个方向的实际应用**：

- **聊天机器人**（ChatGPT、文心一言等）：核心就是"注意力理解 + 自回归生成"，你学到的每个概念都在里面真实运转。
- **机器翻译**：注意力让模型翻译"他"这个词时能回头看原文里的"小明"，译文才能前后一致。
- **AI 绘画与语音**：注意力机制早已走出文字领域——Stable Diffusion 用它把文字描述和图像区域对应起来。

**继续深入的建议路径**：

1. 先补一点**向量基础**：不用系统学线性代数，只要搞懂"一串数字可以相加、可以按位置相乘再相加（点积）"就够看懂本文的所有计算。
2. 读经典论文 *Attention Is All You Need*（2017，Transformer 的出生证明），只看第 3 章的图，配合本文对照着看。
3. 用 PyTorch 手写一个 50 行的迷你注意力模块——亲手把 Q、K、V 从输入里算出来，是检验真懂了的最好方式。
4. 最后再去看位置编码（Positional Encoding，告诉模型词的先后顺序）和完整的编码器-解码器结构，那时你已经有了足够的地基。

读到这里，下次有人问你"ChatGPT 是怎么工作的"，你可以告诉他：它先把词变成数字，再让每个词拿着查询词去和所有词的标签匹配，算出关注比例，按比例混合出"听懂上下文"的新理解，最后像成语接龙一样一个词一个词地往外写。——你已经比 99% 的用户更懂它了。
