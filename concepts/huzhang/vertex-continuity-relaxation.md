---
title: "Hu–Zhang 应力顶点连续性与角点松弛"
type: concept
aliases:
  - 角点松弛
  - 应力顶点连续性松弛
  - Vertex Continuity Relaxation
tags:
  - finite-element
  - mixed-finite-element
  - hdiv
  - boundary-condition
status: in-progress
source: "[[../../literature/fem/sources/Hu2021-vertex-continuity-relaxation.pdf]]"
date_added: 2026-10-15
date_update: 2026-10-15
---

# Hu–Zhang 应力顶点连续性与角点松弛

角点松弛把原来共享的角点应力自由度部分拆开，使两侧可以满足各自的牵引条件，同时保持内部界面力平衡。

## 1. 先区分应力、牵引和两类法向

应力是矩阵，牵引是作用在某个面上的力密度向量：

$$
\sigma=\begin{pmatrix}\sigma_{xx}&\sigma_{xy}\\\sigma_{xy}&\sigma_{yy}\end{pmatrix},
\qquad g=\sigma n.
$$

设右上角为 $x_c$，靠右边、靠上边的单元分别为 R、T。

$$
S_R=\sigma_h|_R(x_c),\qquad S_T=\sigma_h|_T(x_c)
$$

表示两个单元在**同一个角点处的应力矩阵**，不表示整个单元应力恒定。下文外边界法向为 $n_{\mathrm{right}}=(1,0)^T$、$n_{\mathrm{top}}=(0,1)^T$；内部公共边的共同法向记为 $n$。

## 2. 连续问题与离散空间要求的连续性不同

对分片多项式应力，$H(\operatorname{div})$ 协调性要求内部公共边上的法向迹连续。使用同一个法向时，就是两侧的 $\sigma_h n$ 相等；不要求整个应力矩阵相同。

原 Hu–Zhang 元采用“连续 Lagrange 应力＋单元 $H(\operatorname{div})$ bubble”的构造。bubble 在顶点为零，因此顶点值由连续部分给出，带来 $S_R=S_T$ 的额外约束。这种构造方便定义和拼接自由度，bubble 则补充稳定性所需的能力。

松弛去掉部分额外约束，**确实扩大了有限元空间**。在同一网格上比较，有

$$
\Sigma_h\subset\widetilde\Sigma_h\subset H(\operatorname{div},\Omega;\mathbb S).
$$

它允许两侧应力不同，并非要求它们必须不同。

## 3. 牵引–牵引角点为什么可能冲突

右边向上拉，上边自由：

$$
g_{\mathrm{right}}=(0,1)^T,\qquad g_{\mathrm{top}}=(0,0)^T.
$$

**自由边也是牵引边**，只是给定牵引为零，所以右上角是牵引–牵引角点。

松弛前，角点共享一个对称应力矩阵 $S=\begin{pmatrix}p&q\\q&r\end{pmatrix}$。两边分别要求

$$
Sn_{\mathrm{right}}=\begin{pmatrix}p\\q\end{pmatrix}
=\begin{pmatrix}0\\1\end{pmatrix},
\qquad
Sn_{\mathrm{top}}=\begin{pmatrix}q\\r\end{pmatrix}
=\begin{pmatrix}0\\0\end{pmatrix}.
$$

乘 $(1,0)^T$ 就是取第一列，乘 $(0,1)^T$ 就是取第二列。右边要求剪应力 $q=1$，上边要求 $q=0$，因此找不到共同的 $S$。

一般地，两条不平行牵引边的单侧角点数据必须满足

$$
\boxed{n_2^Tg_1=n_1^Tg_2,}
$$

因为对称矩阵满足 $n_2^TSn_1=n_1^TSn_2$。所以**不是所有牵引–牵引角点都需要松弛**；例如两侧零牵引就相容。这个条件也不是要求两个牵引向量相等。

角点虽然是一个点，但边上的多项式若精确满足给定牵引，其端点值也随之确定，不能靠忽略该点消除离散冲突。这是原空间的表示障碍，不等于连续弹性问题无解。

## 4. 拆开的是什么，保留的又是什么

从角点向内部引出公共边 $e$，形成 R、T 两个三角形。取这条边的切向和法向

$$
t=\frac1{\sqrt2}(1,1)^T,\qquad n=\frac1{\sqrt2}(1,-1)^T.
$$

在这个局部标架下，公共边牵引为

$$
Sn=\sigma_{nn}n+\sigma_{nt}t.
$$

它不含纯切向分量 $\sigma_{tt}$，因此可以把这个分量拆开：

| 角点分量（相对于内部边 $e$） | 松弛前 | 松弛后 |
|---|---|---|
| $\sigma_{nn},\sigma_{nt}$ | 两单元共享 | 两单元共享 |
| $\sigma_{tt}$ | 两单元共享 | 两侧分别存储 |
| 独立自由度数 | 3 | 4 |

也就是从 $S_R=S_T$ 放宽为 $S_Rn=S_Tn$，允许的差异为 $S_R-S_T=\alpha tt^T$。这里的切向是**内部公共边的切向**，不是外边界的切向。

实际构造把角点基函数 $\phi_{x_c}tt^T$ 拆成两侧各自的基函数。由于 $tt^Tn=0$，拆分项不改变公共边牵引；整条边的法向迹连续仍保留，两个矩阵也仍各自对称。

## 5. 逐步解出松弛后的角点应力

### 5.1 先分别满足两条外边界

右边牵引规定 $S_R$ 的第一列为 $(0,1)^T$，对称性同时确定左下角；右下角尚未确定，记为 $a$：

$$
S_R=\begin{pmatrix}0&1\\1&a\end{pmatrix}.
$$

上边自由规定 $S_T$ 的第二列为零，对称性同时确定左下角；左上角尚未确定，记为 $b$：

$$
S_T=\begin{pmatrix}b&0\\0&0\end{pmatrix}.
$$

**自由边不要求整个应力矩阵为零。**此时外边界条件已经满足，剩下 $a,b$ 用来匹配内部牵引。

### 5.2 共同法向与各自外法向

![[huzhang-corner-interface.svg]]

图 1：左图为共同法向，右图为各自外法向与界面牵引方向。两侧箭头错开以便辨认，牵引方向由下节的局部矩阵算得，不表示沿边幅值恒定。

取 $n$ 从 T 指向 R，朝右下方。因此 T 的界面外法向是 $n$，R 的界面外法向是 $-n$。两部分受到的界面牵引等大反向：

$$
\underbrace{S_Tn}_{\text{R 对 T 的牵引}}
+\underbrace{S_R(-n)}_{\text{T 对 R 的牵引}}=0
\quad\Longleftrightarrow\quad
\boxed{S_Rn=S_Tn.}
$$

“共同”表示两边计算时使用同一方向。也可以选从 R 指向 T 的 $-n$，两边同时变号，结论不变。**共同法向下结果相等，各自外法向下实际牵引相反。**

### 5.3 用内部牵引匹配确定剩余分量

代入上述矩阵：

$$
S_Rn=\frac1{\sqrt2}\begin{pmatrix}-1\\1-a\end{pmatrix},
\qquad S_Tn=\frac1{\sqrt2}\begin{pmatrix}b\\0\end{pmatrix}.
$$

两者相等给出 $a=1,b=-1$，于是

$$
\boxed{S_R=\begin{pmatrix}0&1\\1&1\end{pmatrix},\qquad
S_T=\begin{pmatrix}-1&0\\0&0\end{pmatrix}.}
$$

它们分别满足右边向上拉、上边自由；内部两侧的实际牵引为

$$
S_R(-n)=\frac1{\sqrt2}(1,0)^T,\qquad
S_Tn=\frac1{\sqrt2}(-1,0)^T,
$$

即 R 侧向右、T 侧向左，等大反向。法向斜向、牵引水平，二者不必平行。

两个矩阵的差恰好是允许拆开的纯切向分量：

$$
S_R-S_T=\begin{pmatrix}1&1\\1&1\end{pmatrix}=2tt^T.
$$

因此，松弛后两条外边界条件与内部牵引连续可以同时满足。这个例子证明的是**局部约束不再矛盾**，不是给出了整个区域的应力解。

## 6. 换成位移–牵引角点会怎样

把上边改成固定 $u=0$，右边仍向上拉，就可以保留共同应力值

$$
S_R=S_T=\begin{pmatrix}0&1\\1&a\end{pmatrix}.
$$

上边固定不要求牵引为零，而是允许产生由解确定的反力，其局部牵引为 $(1,a)^T$。因此，上边不再要求剪应力为零，原来的矛盾消失。

所以，位移–牵引角点**不必为了消除上述牵引不相容而松弛**。
