# arXiv Visual Sprint - 详细参考

## 1. 意图驱动设计原理

### 为什么需要选题发散？
用户输入的选题往往过于笼统（如 "Transformer"），直接检索会产生大量无关结果。通过 AI 发散出 3-5 个技术细分关键词（如 "Efficient Attention", "Linear Transformer"），可以显著提高检索的召回精度。

### 为什么只搜近一周？
"Sprint" 的核心是时效性。限定近 7 天确保用户获取的是领域内最前沿的动态，同时也减少了信息过载。

### 官方尺寸与分辨率
- **aspectRatio: "3:2"**: 经典学术图表比例。
- **imageSize: "1K"**: 兼顾细节表现力与生成速度。

## 2. 核心 Prompt 模板

### Phase 1: 选题发散 Prompt
```text
你是学术检索专家。用户现在的选题是: {topic}
请发散出 3-5 个用于 arXiv 检索的精准关键词。
要求:
1. 关键词必须是具体的学术术语。
2. 能够覆盖该选题下的最新研究热点。
3. 仅输出关键词列表，每行一个。
```

### Phase 1b: 论文智能分类 Prompt
```text
你是学术情报专家。以下是最近一周关于 {topic} 的 20 篇论文标题。
请将它们划分为 3-5 个逻辑清晰的子类别（Sub-themes），并为每个类别起一个专业的名称。
输出格式要求:
### [类别名称1]
- [论文索引编号] 标题
...
### [类别名称2]
...
```

### Phase 2: 深度解析 Prompt
```python
prompt = f"""
基于以下论文前 5 页文本，提取结构化信息：
{text[:8000]}

提取要求:
{{
  "problem": "研究缺口或痛点（1句话）",
  "contributions": ["贡献1", "贡献2", "贡献3"],
  "method_keyword": "核心技术关键词",
  "claim_validation": "supported/unsupported/unclear"
}}
"""
```

### Phase 3: Visual Abstract 生成 (Python SDK)

该阶段现在由 `scripts/generate_visual_abstract.py` 脚本统一处理。

**Python 调用方式 (通过 uv run)**:
```bash
uv run scripts/generate_visual_abstract.py \
    --pdf "/Users/dandelight/workspace/github.com/Dandelight/research-skills/workspace/{datetime}-{topic}/raw/paper.pdf" \
    --pdf-pages 5 \
    --retries 3 \
    --timeout-seconds 180 \
    --output "/Users/dandelight/workspace/github.com/Dandelight/research-skills/workspace/{datetime}-{topic}/visuals/output.png"
```

也支持结构化字段模式（不传 PDF）：
```bash
uv run scripts/generate_visual_abstract.py \
    --title "[论文标题]" \
    --problem "[问题陈述]" \
    --contributions "[贡献点1, 2, 3]" \
    --method "[方法关键词]" \
    --output "/Users/dandelight/workspace/github.com/Dandelight/research-skills/workspace/{datetime}-{topic}/visuals/output.png"
```

**内部逻辑 (google-genai SDK)**:
```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options={"base_url": os.environ.get("GEMINI_API_BASE"), "timeout": 180}
)

model_name = os.environ.get("GEMINI_MODEL")
if not model_name:
    model_name = (
        "google/gemini-3.1-flash-image-preview"
        if "cherryin" in os.environ.get("GEMINI_API_BASE", "").lower()
        else "gemini-3.1-flash-image-preview"
    )

response = client.models.generate_content(
    model=model_name,
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="3:2", image_size="1K")
    )
)
```

## 3. 验收检查表

- [ ] **时效性**: 所有论文提交日期均在 T-7 天内。
- [ ] **一致性**: Visual Abstract 中的标题与原始论文一致。
- [ ] **比例**: 图像宽高比为 1.5 (3:2)。

## 4. 常见陷阱

- **陷阱: 检索结果为空**
  - **解决**: 如果近一周无相关论文，提示用户扩大时间范围至近一月，或更换发散关键词。
- **陷阱: PDF 解析乱码**
  - **解决**: 降级为使用 arXiv 原始摘要进行生成，并在 `summary.md` 中注明“基于摘要生成”。
- **陷阱: 缺失所需功能时试图自行编写脚本**
  - **解决**: 严禁通过临时新增 Python 脚本或使用 `python -c` 执行复杂逻辑来弥补功能缺失。必须直接告知用户该 Skill 当前不支持该功能或缺少相关脚本，以维持工具的封装性和结果的可控性。

## 5. 环境变量设置指南

当前环境要求同时设置 `GEMINI_API_KEY` 与 `GEMINI_API_BASE`。如果脚本报错，请根据操作系统执行以下命令：

### macOS / Linux (Zsh or Bash)
在终端运行以下命令（仅对当前会话有效）：
```bash
export GEMINI_API_KEY="您的密钥"
export GEMINI_API_BASE="您的代理地址"
```
若要永久生效，请将上述命令添加到 `~/.zshrc` 或 `~/.bashrc` 文件中。

### Windows (PowerShell)
在 PowerShell 中运行：
```powershell
$env:GEMINI_API_KEY = "您的密钥"
$env:GEMINI_API_BASE = "您的代理地址"
```

### Windows (Command Prompt)
在 CMD 中运行：
```cmd
set GEMINI_API_KEY=您的密钥
set GEMINI_API_BASE=您的代理地址
```

如果您不知道什么是“环境变量”，可以把它理解成“给脚本提供配置参数的系统级键值对”。按上面的命令执行一次后，脚本就能读到对应配置。

如果您使用的是 cherryin 提供商，模型名通常需要前缀形式：
```bash
export GEMINI_MODEL="google/gemini-3.1-flash-image-preview"
```
不设置也可以，脚本会在检测到 `GEMINI_API_BASE` 包含 `cherryin` 时自动切换模型名。

## 6. Timeout 排查指南

- 先确认代理地址可达：`GEMINI_API_BASE` 指向的网关是否可访问。
- 降低并发：不要用一条超长 `&&` 串行命令一次跑多篇，建议单篇运行或分批运行。
- 拉长超时：使用 `--timeout-seconds 180` 或更高。
- 启用重试：使用 `--retries 3`，脚本会自动打印每次尝试耗时和失败原因。
- 保留日志：脚本已输出阶段日志（初始化、PDF解析、API调用、响应解析），可直接定位卡点。

## 7. 交互话术示例 (Response Templates)

### 展示检索结果 (Phase 1)
> 🚀 **太棒了！我已经为您在 arXiv 上完成了近一周的“情报扫描”。**
>
> 针对您的选题 **{topic}**，我发散了关键词 *{keywords}*，并为您精选了 **20 篇**最新的代表性论文。为了方便您快速锁定兴趣，我将它们分为了以下几个子领域：
>
> ### 📂 {Category_Name_1}
> 1. **{Title}** ({arXiv_ID})
>    - 💡 **核心亮点**: {One_sentence_summary}
> 2. ...
>
> ### 📂 {Category_Name_2}
> ...
>
> **这份清单涵盖了本周该领域的最前沿进展。您想针对哪个类别（或者选定哪 3 篇）生成深度解析的 Visual Abstract 吗？告诉我编号即可开始！** 期待为您揭开这些论文的技术细节。

### 任务交付 (Phase 4)
> ✅ **恭喜！您的 45 分钟科研情报冲刺已圆满完成！**
>
> 我已经为您生成了 3 份结构化的 Visual Abstract，并汇总到了以下路径：
> 📂 `/Users/dandelight/workspace/github.com/Dandelight/research-skills/workspace/{datetime}-{topic}/summary.md`
>
> **您可以直接在编辑器或支持 Markdown 的软件中打开此文件查看所有可视化卡片及结构化信息。** 这些摘要基于论文的核心方法论和 Figure 1 进行了深度萃取，希望能为您节省数小时的阅读时间！
>
> 您对这次的 Sprint 结果满意吗？如果有需要调整的地方，请随时告诉我。
