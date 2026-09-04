---
title: "梅跃老师首次面谈：申请书七条修改意见"
advisor: "梅跃（大连理工大学教授，大连工业软件创新发展研究院常务副院长）"
report_period: "2026-08"
meeting_date: "2026-08-31"
meeting_mode: "线下（研究院办公室，约 14:30）"
status: "follow-up-done" # preparing | reported | follow-up-done
date_start: 2026-08-31
date_update: 2026-08-31
tags:
  - 工作汇报
  - PIML
  - matrix-free
  - GPU
topics:
  - "请梅跃老师看已提交的第 80 批申请书，得七条修改意见；另问出计算力学大会的经费口径与 Matrix-Free 上的合作线索"
related:
  - "./mei-yue"
  - "../../research/funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft"
  - "../../research/funding/grant-writing-review-notes.md"
  - "../../research/piml-matrix-free-gpu/project-plan"
---

# 梅跃老师首次面谈：申请书七条修改意见

> 与梅跃老师的**第一次线下讨论**，带纸质打印件当面翻。背景与其研究方向见 [[mei-yue|梅跃实体页]]，逐字微信记录与约见过程见 [[wechat-log|微信沟通档案]]。

原打算问四件事：申请书写法、研究方向定位、计算力学大会、向几何/材料非线性推广。**实际只有第一件充分展开**，得七条意见；大会问出了经费口径；研究方向与非线性推广他未表态。非线性一题需另约——本人倾向**几何非线性先行**：共旋格式把刚体转动分离到局部之外，子结构内部仍是小应变线弹性，离线随机采样的前提保得住，而路径相关本构（弹塑性、损伤）会让这个前提直接失效；此判断尚未经他核，技术背景见 [[../../concepts/nonlinear-fem|非线性有限元页]]。

## 七条修改意见

按他给出的顺序记录，未加本人解读。材料 08-30 已提交、不再修改，**这七条没有一条改进了本批**，价值全在后续材料——跨批次口径已入 [[../../research/funding/grant-writing-review-notes|本子写作意见汇编]]（与刘畅 08-27 的初稿审阅意见合编），成果著录口径入 [[../../research/funding/publications-ledger|代表性成果台账]]。

**署名与用词**

1. **标题里不要出现「问题无关机器学习」**。PIML 尚未形成学界统一认识，不像 PINN 那样是共识术语，评审看到会不知道指什么；建议换成「AI 泛化」一类更通用的描述。
2. **关键词限 5 个但不必写满，3 个也可以**；投力学口的话，「Krylov 迭代」「GPU 协同加速」这类词尽量都不要写。

**图**

3. **图 2 图题与图不符**：图题写了「约 33.2 亿单元」，但单看图体现不出这个量级。
4. **图还是有一点 AI 感。**
5. **图不精致**；**力学中一般不用黑白图**，图还是要自己画，尽量改得更美观。

**研究基础（第 6 部分）**

6. **好论文要写清楚发在什么期刊、本人是第几作者**。力学口的人普遍文章多，数学背景在篇数上很吃亏，能标注质量的地方必须标注。
7. **「已具备的科研条件」应当写上 CAE 全国重点实验室**，这是一个很重要的基础。

## 两条会后结论

- **Matrix-Free 上有一条可对话的技术线**。他对 Matrix-Free 有一点兴趣；他们做过一种 **cut 单元**的做法，也是**把共性的部分抽离出来、不需要每一次迭代都计算**——与 Matrix-Free 复用几何量与局部算子的动机同构（此同构判断由本人所作，尚未与他核对）。见 [[../../concepts/matrix-free/_index|Matrix-Free 主题入口]]。
- **计算力学大会卡在经费不在报名**。本人目前没有可报销的项目，梅跃因此指向去问郭旭老师。届次、时间地点、摘要与报名截止本库仍无记录。

## 会后待填

- [ ] **问郭旭报名的事**——中国计算力学大会的报名与经费。
- [ ] **发 Matrix-Free 结果给梅跃**，顺带问清是哪一类 cut 方法、抽离的是哪部分量、有无对应论文。

## 关联页面

- [[mei-yue|梅跃实体页]] — 静态画像、研究方向与结合点评估。
- [[../../research/funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft|第 80 批申请书正文]] — 本次要过的材料本体。
- [[../../research/funding/grant-writing-review-notes|本子写作意见汇编]] — 七条的跨批次沉淀去处。
- [[../liu-chang/liu-chang|刘畅]]、[[../guo-xu/guo-xu|郭旭]] — PIML 主线合作者与合作导师。
