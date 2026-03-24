---
name: "arxiv-visual-sprint"
description: "45-min arXiv Visual Sprint: Auto-expands topics, filters last 7 days & generates PNG abstracts. MANDATORY for quick literature reviews, topic scouting, or visual abstract requests."
---

# arXiv Visual Sprint

## 描述
**45分钟论文视觉化冲刺：科研情报的“闪电战”工具**。该 Skill 专门设计用于将宽泛的科研选题快速转化为近一周最前沿的结构化 Visual Abstract。

**当用户提及以下场景时，必须立即触发此 Skill：**
- **最新动态追踪**：用户问“最近一周 [选题] 有什么新论文？”或“帮我查查 [选题] 的最新进展”。
- **选题方向调研**：用户在构思新方向，需要快速发散关键词并检索相关领域论文。
- **视觉化产出**：用户要求“做个文献可视化”、“生成论文总结图”或“做个 Visual Abstract”。
- **精益读论文**：用户表示“不想看全文，只想快速过一下最近的几篇好文章”或“帮我快速 review”。

**核心价值**：AI 完成选题发散、检索、萃取与可视化，人工仅需在关键节点进行 3 次审查（共 10 分钟）。

## 交互规范 (Communication Guidelines)
- **热情且专业**：使用积极的语气（如“太棒了”、“我为您找到了...”），体现作为科研助手的价值。
- **细节导向**：不仅列出标题，还要通过“核心亮点”展示论文的独特价值，引发用户兴趣。
- **主动引导**：在展示检索结果后，**必须**主动询问用户是否需要生成 Visual Abstract，并清晰说明后续步骤。
- **进度可视化**：告知用户当前处于 Sprint 的哪个阶段（如“已完成 Phase 1 检索，正在等待您的选择”）。

## 依赖检查
- [ ] MCP Server `arxiv` 已配置
- [ ] `GEMINI_API_KEY` 环境变量已设置，具备 `gemini-3.1-flash-image-preview` 权限
- [ ] `GEMINI_API_BASE` 可选（未设置时走官方默认地址；使用代理时请设置）
- [ ] 若使用 cherryin 提供商，模型名需使用 `google/gemini-3.1-flash-image-preview`（脚本会自动识别，也可通过 `GEMINI_MODEL` 显式指定）
- [ ] [uv](https://github.com/astral-sh/uv) 已安装

### 故障排除与新手引导 (Troubleshooting)
- **环境变量缺失**：如果脚本报错“GEMINI_API_KEY not found”，**必须**告知用户先设置 API Key；若使用代理且报连接问题，再引导设置 `GEMINI_API_BASE`。
- **新手引导**：如果用户不了解“环境变量”概念，**必须**引导其参考 [REFERENCE.md#环境变量设置指南](./REFERENCE.md#环境变量设置指南)，并根据其操作系统（Windows/macOS/Linux）提供可直接复制的命令。
- **超时排查**：如果出现 `Operation timed out`，**必须**先检查 `GEMINI_API_BASE` 是否可达，再提高 `--timeout-seconds` 并使用 `--retries` 重试，同时保留脚本日志定位卡点。
- [ ] 工作目录 `./workspace/sprints/` 可写

## 执行检查清单

### Phase 0: 环境准备
- [ ] **必须**在 `arxiv-visual-sprint/` 目录下执行 `uv sync` 以安装依赖。
- [ ] **必须**执行 `uv run scripts/setup_workspace.py` 以初始化工作空间。

### Phase 1: 选题发散与智能检索（10分钟）
- [ ] **必须**根据用户提供的选题，调用 Gemini 发散出 3-5 个精准的 arXiv 搜索关键词。
- [ ] **必须**对每个关键词执行 `search_papers`，参数建议设为：`max_results=30, sort_by="submittedDate"`（确保覆盖量）。
- [ ] **必须**筛选出**提交日期在过去 7 天内**的论文（前 20 篇）。
- [ ] **必须**调用 Gemini 对这 20 篇论文进行**智能分类**（划分为 3-5 个技术子类）。
- [ ] **必须**按类别向用户展示论文列表（标题+亮点），并**主动询问**用户想要针对哪个类别或哪几篇生成 Visual Abstract。
- [ ] **checkpoint**: 如果筛选后符合要求的论文不足 10 篇，**必须**建议用户放宽关键词或选题范围。

### Phase 2: 深度解析（15分钟）
- [ ] **必须**执行 `download_pdf(paper_id)` 仅提取前 5 页内容（Introduction + Method + Fig 1 Caption）。
- [ ] **必须**使用 Gemini Flash 提取结构化信息：
  ```json
  {"contributions": ["...", "...", "..."], "problem_statement": "...", "method_keyword": "...", "claim_validation": "supported/unsupported/unclear"}
  ```
- [ ] **checkpoint**: 如果 `claim_validation` 为 "unsupported"，**必须**标红警告用户该论文声称的 SOTA 可能存在水分。

### Phase 3: Visual Abstract 生成（15分钟）
- [ ] **必须**调用 `uv run scripts/generate_visual_abstract.py` 脚本生成 PNG 图片。
- [ ] **必须**优先使用 PDF 直连模式：`--pdf <path> --pdf-pages 5`，直接提取前 5 页文本送入 Gemini。
- [ ] **必须**符合官方规范：`aspectRatio: "3:2"`, `imageSize: "1K"`。
- [ ] **必须**保存到 `./workspace/sprints/{date}-{keyword}/visuals/{paper_id}_abstract.png`。
- [ ] **checkpoint**: 使用 `uv run scripts/validate_image.py` 自动验证图像合规性；如失败需保留完整日志并提示用户如何设置环境变量。

### Phase 4: 交付与汇总（5分钟）
- [ ] **必须**生成 `index.html` 汇总页，包含 3 个 Visual Abstract 卡片。
- [ ] **必须**输出最终路径：`./workspace/sprints/{date}-{keyword}/index.html`

## 禁止事项（ANTI-PATTERNS）
- **禁止**搜索全量历史论文（必须限定为近一周，确保“冲刺”的时效性）。
- **禁止**跳过选题发散步骤（直接搜选题往往噪音太大）。
- **禁止**下载 PDF 全文（仅前 5 页）。

## 任务示例
**输入**: "帮我看看最近一周关于大模型长文本处理 (Long Context) 的论文，做个可视化摘要"

**执行流**:
1. Gemini 发散关键词: "Long Context Window", "Needle In A Haystack", "Transformer Context Extension"...
2. 检索近 7 天论文 -> 得到 8 篇 -> 用户选择 3 篇。
3. 提取前 5 页 -> 生成 JSON -> 生成 3 张 PNG。
4. 生成 `index.html`。

## 参考文档
- 详细策略与代码实现: [REFERENCE.md](./REFERENCE.md)
- 初始化脚本: [scripts/setup_workspace.py](./scripts/setup_workspace.py)
- 生成脚本: [scripts/generate_visual_abstract.py](./scripts/generate_visual_abstract.py)
- 验证脚本: [scripts/validate_image.py](./scripts/validate_image.py)
