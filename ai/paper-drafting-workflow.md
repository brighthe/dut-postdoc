---
name: paper-drafting
description: >-
  《任意次胡张混合有限元拓扑优化》CICP 投稿论文专项提炼与撰写工作流。
  在讨论 papers/arbitrary-order-huzhang-topopt-draft-zh.md 时，经提议同意或显式指示后加载。
---

# 胡张混合元拓扑优化论文撰写指南 · paper-drafting

本技能专用于推进与撰写 **《任意次胡张混合有限元拓扑优化》**（投稿目标：*Communications in Computational Physics, CICP*）。

---

## 1. 触发与授权协议

1. **AI 提议模式**：当识别到涉及 `papers/arbitrary-order-huzhang-topopt-draft-zh.md` 的重构、推导或撰写时，先询问：
   > 💡 *检测到胡张元论文撰写任务，建议调用 `paper-drafting` 技能（严格对照博士论文第五章与 CICP 投稿标准），请问是否同意加载？*
2. **用户显式模式**：用户显式指示“调用 paper-drafting”时，AI 声明 `[已激活技能：paper-drafting]` 并直接执行。

---

## 2. 三大核心事实源（写实锚定）

1. **正文推演底稿**：
   * `papers/arbitrary-order-huzhang-topopt-draft-zh.md`
2. **投稿决策与门禁**：
   * `papers/arbitrary-order-huzhang-topopt-outline.md`（锁定 CICP 风格、4 项核心贡献与证据边界）
3. **原始数学与算例事实源**：
   * 源码：`C:\workspace\xtu-phd-thesis\thesis\body\chapter05\chapter05.tex`
   * 渲染：`C:\workspace\xtu-phd-thesis\thesis\brightPhD.pdf`（第五章，第 117–153 页）

---

## 3. 核心写作与架构准则

1. **知识库 (Wiki) 与投稿论文 (Draft) 的双轨分工原则**：
   * **概念知识库 (`concepts/huzhang/huzhang-mixed-fem.md`)**：作为全量、永久的底层知识资产库（SSOT），完整保留所有推导细节、全阶次自由度解析计数表、带循环逻辑的伪代码与数据结构映射；
   * **投稿论文 (`papers/arbitrary-order-huzhang-topopt-draft-zh.md`)**：严格遵循顶刊学术体裁，去除“手册感”的低阶算术表格与伪代码，改用任意阶次 $k$ 的通用解析维数通项公式与严密数学定义，保持精炼的 6 章节经典学术架构（不单独设立割裂的 Implementation 章节）。
2. **CICP 投稿与排版硬性规范**：
   * **插图多模态资产维护**：插图必须在 `papers/figures/` 中同步维护 `.eps`（CiCP 终稿生产出版标准）、`.pdf`（标准矢量编译）与 `.png`（Markdown 实时图文预览）；
   * **公式渲染通用兼容性**：跳量算子一律使用跨平台通用的 `[\![ \dots ]\!]`（避免在 Markdown 中依赖非标宏包命令 `\llbracket` 导致渲染报错）；
   * **定义严谨性**：有限元空间与角点松弛采用严格的泛函空间集合论定义，公式内部杜绝中文字符与口语化描述。
3. **内容严格对照博士论文第五章**：
   * 变分推导、矩阵分块形式与数值算例严格溯源 `chapter05.tex`，不编造未经检验的结论。
