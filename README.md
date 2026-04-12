# Academic Skills (Chinese) / 中文文献调研、学术写作与绘图技能包

这是一组专为 AI Agent 设计的技能包，旨在提升 Agent 在**arXiv文献跟踪**，**中文学术写作**与**学术图表绘制**方面的专业性与规范性。

通过安装本技能包，您的 AI Agent 将掌握严格的学术排版规范、逻辑论证框架以及专业的学术词汇库，从而输出达到发表级标准的内容。

## 极简体验

复制技能的原文件到您常用的 AI 对话框中即可：

- [中文学术写作 academic-writing-zh/SKILL.md](./academic-writing-zh/SKILL.md)
- [中文科研绘图 academic-figure-zh/SKILL.md](./academic-figure-zh/SKILL.md)
- [arXiv 视觉冲刺 arxiv-visual-sprint/SKILL.md](./arxiv-visual-sprint/SKILL.md)
- [任务分解与编排 task-decomposition-zh/SKILL.md](./task-decomposition-zh/SKILL.md)

## 包含技能

本仓库包含以下三个独立技能：

### 1. `academic-writing-zh` - 中文学术写作助手

**核心能力**：帮助用户进行符合学术规范的中文写作、润色与框架搭建。

**主要特性**：
- **逻辑框架构建**：强制执行“立项背景 → 痛点分析 → 解决方案”的三段式论证逻辑，确保论述严谨。
- **学术词汇升级**：内置高级动词与名词库，自动将口语化表达转化为学术术语（如“干”→“攻克”，“想”→“构建”）。
- **句式模板引擎**：提供“现状转折”、“归因分析”、“方案对策”等万能学术句式模版。
- **名词化处理**：将动作过程转化为科学概念，提升文本的理论高度。

### 2. `academic-figure-zh` - 学术图表规范指南

**核心能力**：指导 Agent 生成符合学术出版规范的图表（包括数据图、框架图、原理图）。

**主要特性**：
- **尺寸即语义**：强制要求作图时设定最终物理尺寸（单栏 3.5" / 双栏 7.0"），杜绝后期缩放导致的字体模糊。
- **全局颜色字典**：定义了严格的颜色语义（如深蓝代表主方法，朱红代表基线），确保整篇论文视觉语言统一。
- **视觉层级压制**：通过线宽、颜色饱和度建立清晰的信息层级，引导读者视线。
- **跨平台规范**：包含 Matplotlib 参数设置、LaTeX 插入最佳实践以及灰度安全检查清单。

### 3. `arxiv-visual-sprint` - 近一周论文冲刺与可视化摘要

**核心能力**：围绕用户选题自动发散关键词，筛选最近 7 天 arXiv 论文，按类别组织结果，并生成可直接交付的 PNG Visual Abstract。

**主要特性**：
- **时效优先检索**：自动聚焦近 7 天新论文，避免历史噪声干扰。
- **分类化浏览**：将候选论文按技术子类聚合，降低“20 篇平铺”阅读负担。
- **SSE 生图链路**：默认走 `streamGenerateContent?alt=sse`，支持重试与超时配置。
- **代理与模型适配**：支持可选 `GEMINI_API_BASE`，可自动识别 cherryin 模型名。
- **交付路径友好**：生成脚本会输出图片文件绝对路径，方便直接定位文件。

### 4. `task-decomposition-zh` - 任务分解与编排

**核心能力**：根据用户任务描述，自动分解为多个子任务，每个子任务都有明确的依赖关系和执行顺序。

**主要特性**：
- **任务分解**：将复杂任务分解为多个子任务，每个子任务都有明确的依赖关系和执行顺序。
- **子任务输出**：每个子任务都有一个清晰的输出物，方便后续处理。
- **任务执行计划**：根据子任务的依赖关系，生成一个优化的执行计划，确保任务按顺序执行。

---

## 安装方法

若您已经安装了 [Node.js](https://nodejs.org/)，即可通过 [Skills CLI](https://skills.sh) 安装和管理 Skills。在终端运行以下命令：

```bash
npx skills add Dandelight/research-skills
```

这将同时安装 `academic-writing-zh`、`academic-figure-zh` 和 `arxiv-visual-sprint` 三个技能。

或者您可以只安装单个 Skill：

```bash
# 只安装「学术写作规范」技能
npx skills add Dandelight/research-skills --skill academic-writing-zh

# 只安装「学术图表规范」技能
npx skills add Dandelight/research-skills --skill academic-figure-zh

# 只安装「arXiv 视觉冲刺」技能
npx skills add Dandelight/research-skills --skill arxiv-visual-sprint

# 只安装「任务分解与编排」技能
npx skills add Dandelight/research-skills --skill task-decomposition-zh
```

如果您未安装 Node.js 或 Skills CLI，您可以直接从 GitHub 仓库下载技能文件，放到您的 AI Agent 配置目录下，一般为全局的 `~/.skills/` 或者项目的 `skills/` 目录。配置之后应该目录结构如下：

```
skills/
├── academic-writing-zh/
│   └── SKILL.md
├── academic-figure-zh/
│   └── SKILL.md
├── task-decomposition-zh/
│   └── SKILL.md
└── arxiv-visual-sprint/
    └── SKILL.md
```

## 使用示例

安装后，您可以直接向您的 AI Agent 提问，技能将根据语境自动激活。

### 场景一：学术写作（自动激活 `academic-writing-zh`）

**用户输入**：
> “帮我把这段话改写得更学术一点：我们要做一个算法，把传感器信号和图像结合起来。现在的算法直接把信号数值当成字处理，容易丢精度...”

**Agent 输出（应用技能后）**：
> “本课题提出面向‘图像-信号’跨模态语义对齐算法。然而，传统方法将高精度时序信号直接视为离散 token 处理，导致数值精度丢失严重，且难以在长时序上建立跨模态关联。针对上述挑战，本课题拟提出‘语义锚定’与‘原生编码’融合机制：一方面，通过图像特征引导信号进行语义切片，实现多模态粒度的精准对齐；另一方面，设计原生时序编码器，完整保留信号的高维数值特征。最终，赋予模型在复杂场景下的鲁棒语义理解能力。”

### 场景二：绘制图表（自动激活 `academic-figure-zh`）

**用户输入**：
> “请帮我生成一段 Python 代码，画一个展示我们方法（蓝色）和基线方法（红色）对比的折线图，要求符合学术规范，单栏宽度。”

**Agent 行为（应用技能后）**：
- 自动设定 `figsize=(3.5, 2.2)`。
- 调用全局颜色字典：主方法 `#1D4ED8`，基线 `#DC2626`。
- 设置字体为 Times New Roman，字号为 9pt。
- 隐藏图表的上边框和右边框，保留左边框和下边框。

### 场景三：快速文献冲刺（自动激活 `arxiv-visual-sprint`）

**用户输入**：
> “帮我筛选最近一周 multi-agent 的新论文，按类别整理一下，并给我生成一个 visual abstract。”

**Agent 行为（应用技能后）**：
- 自动发散 3-5 个检索关键词并聚合最近 7 天论文。
- 默认展示前 20 篇并按技术子类分组，主动引导用户选择类别或论文编号。
- 基于论文前 5 页内容生成 PNG Visual Abstract（默认 SSE 模式）。
- 输出生成文件的绝对路径，便于用户直接打开或分享。

### 场景四：任务分解与编排（自动激活 `task-decomposition-zh`）

**用户输入**：
> “请帮我分解‘复现一篇论文’的任务”

**Agent 输出（应用技能后）**：
- 任务分解为多个子任务，每个子任务都有明确的依赖关系和执行顺序。
- 每个子任务都有一个清晰的输出物，方便后续处理。
- 任务执行计划（如并行执行、顺序执行等）。

## 常见报错排查（arxiv-visual-sprint）

使用 `arxiv-visual-sprint` 前，至少需要设置 `GEMINI_API_KEY`。`GEMINI_API_BASE` 是可选项：直连官方时可不设置，走中转或第三方网关时建议设置。

我在用的中转服务商：[CherryIN](https://open.cherryin.ai/register?aff=Z26d)

### 1) 必备环境变量

```bash
GEMINI_API_KEY=你的密钥
GEMINI_API_BASE=你的网关地址（可选）
```

### 2) macOS / Linux 设置示例

```bash
export GEMINI_API_KEY="your_api_key"
export GEMINI_API_BASE="https://your-api-base.example.com"
```

### 3) Windows PowerShell 设置示例

```powershell
$env:GEMINI_API_KEY="your_api_key"
$env:GEMINI_API_BASE="https://your-api-base.example.com"
```

### 4) 常见错误与处理

- `GEMINI_API_KEY not found`：未设置 API Key，先设置后再运行。
- `Operation timed out`：优先检查 `GEMINI_API_BASE` 可达性，随后提高 `--timeout-seconds` 并配合 `--retries`。
- 返回 401/403：检查 Key 是否有效、额度是否充足、网关权限是否包含图像模型。
- cherryin 模式下模型名建议使用 `google/gemini-3.1-flash-image-preview`（也可通过 `GEMINI_MODEL` 显式覆盖）。

## 贡献与反馈

本技能包是一次建立学术写作与绘图基础规范的尝试，远非完美无缺，但一个尚不完善但明确统一的规范，远胜于毫无规范可循的状态。因此，我们诚挚地邀请您：

- 分享您在学术写作与绘图中的实践经验与心得
- 指出当前规范中不合理或难以落地的部分
- 提出您认为更优的处理方式或规则建议
- 补充您所在领域的特殊规范或惯例

无论是批评指正还是建设性意见，都欢迎通过 Issue 或 Pull Request 的方式告诉我们。让我们共同完善这套规范，使其真正成为学术写作的实用指南。

## 许可证

[MIT](LICENSE)
