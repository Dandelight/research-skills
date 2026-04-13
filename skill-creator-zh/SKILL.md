---
name: skill-creator-zh
description: 包含了高质量 Skill 开发的约束。当被要求创建 Skill 时，必须读取这个文件。
---

# 高质量 Claude Skill 开发指南

> **导读**：一个优秀的 Claude Skill 绝不仅仅是一段散漫的“提示词（Prompt）”，它更像是一个带有类型校验、流程控制和错误处理的**“Agent 自动化脚本”**。本指南基于 Anthropic 官方的 [Skills](https://github.com/anthropics/skills) 和 [Agent Skills 规范](https://agentskills.io/)提炼，教你如何编写具有极高工程严谨性的 Skill。

## 零、基本结构与硬性约束

每个 Skill 都是一个独立的文件夹。在开始编写前，你必须遵守以下约束，否则会导致 Skill 难以被识别或调用：

1. **文件与目录命名**：
   - 必须有一个专属的父文件夹，名称使用 **kebab-case**（烤肉串命名法：全小写字母，单词之间用短横线 `-` 连接，不能包含空格或其他特殊字符，例如 `my-awesome-skill`）。
   - 文件夹内必须包含一个名为 `SKILL.md`（全大写）的主文件。
2. **YAML 头部元信息 (Frontmatter)**：
   `SKILL.md` 的开头必须是 YAML frontmatter，且 `name` 字段**必须与父文件夹名称完全一致**。

```yaml
---
name: my-awesome-skill
description: "这里写描述。描述必须具有侵略性（Pushy），不仅要写能做什么，更要规定在什么用户输入下必须触发。最大 1024 字符，不能包含尖括号 < 或 >。"
license: Apache-2.0 # 可选
---
```

---

## 核心方法论：设计好 Skill 的 5 大支柱

### 1. 明确的触发条件 (Clear Triggers)

大模型在面对海量工具时，常会出现“该用不用”的情况。因此，`description` 字段必须极其“强势（Pushy）”，要穷举正向触发和反向拉黑的场景。

- **正向穷举**：明确规定哪怕用户只是随口一提，也必须触发。
- **反向拉黑**：明确界定技能的边界，防止模型滥用。

> 🔗 **官方示例参考**：
>
> - **[xlsx 技能](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)**：在描述中，明确规定了：即使交付物涉及表格数据，但如果最终要求输出的是 Word 文档或 HTML 报告，**绝对不要触发 (Do NOT trigger)** 本技能。
> - **[frontend-design 技能](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)**：列举了极度具体的触发场景：“当用户要求构建 Web 组件、页面、落地页、仪表板或美化任何 Web UI 时触发。”
> - **[pdf 技能](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)**：用命令式语气收尾：“如果用户提到了 .pdf 文件或者要求生成一个，**使用这个技能** (use this skill)。”

### 2. 渐进式分层 (Layering & Progressive Disclosure)

大语言模型的上下文窗口是宝贵的资源，严禁将所有逻辑塞进一个巨大的 Markdown 文件中，这会导致模型“注意力失焦”。

- **主文件限长**：`SKILL.md` 主文件应尽量保持在 **500 行以内**。
- **作为路由器**：如果信息过多，主文件应作为“路由中心”，指导模型去读取对应的子文件（如放入 `references/` 文件夹的文档）。
- **黑盒化复杂逻辑**：对于需要反复执行的代码（如环境配置、启动服务器、复杂 API 调用），不要让 Agent 现场写代码，而是提前写好 Python/Bash 脚本放入 `scripts/` 目录，让 Agent 直接传参调用。

> 🔗 **官方示例参考**：
>
> - **[mcp-builder 技能](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md)**：主文件中只保留了 4 个宏观开发阶段，而将庞大的 TypeScript 和 Python 实现细节拆分到了 `reference/` 目录下的独立 Markdown 文件中，按需加载。
> - **[claude-api 技能](https://github.com/anthropics/skills/blob/main/skills/claude-api/SKILL.md)**：主文件作为一个“路由中心”。它先教模型如何检测用户的编程语言，然后根据语言指导模型去读取对应的子文档（如 `python/claude-api/README.md`）。
> - **[python-evaluator 技能](https://github.com/anthropics/skills/blob/main/skills/python-evaluator/SKILL.md)**：将复杂的执行环境配置、超时控制和输出捕获全部封装在 `scripts/evaluate.py` 中，模型只需以黑盒方式调用该脚本。

### 3. 设立门禁与必做动作 (Mandatory Actions & Gates)

好的 Skill 充满了红线约束（`CRITICAL` / `NEVER` / `ALWAYS`），绝不让 Agent 靠“猜”来执行任务。

- **操作门禁 (Gates)**：规定在执行高风险或复杂动作前，必须先完成的前置动作。
- **强制确认 (Asking)**：规定在信息不足时，必须向用户提问，而不是擅自编造或假设。
- **解释原因 (Explain the Why)**：不要只给生硬的规则，告诉大模型“为什么要这样做”，这能激发其推理能力，在处理边缘情况时表现更好。

> 🔗 **官方示例参考**：
>
> - **[webapp-testing 技能](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md)**：明确规定门禁：Agent 在使用 `with_server.py` 辅助脚本前，**必须先运行带 `--help` 参数的命令查看用法**，绝对不允许直接去阅读复杂的黑盒脚本源码。
> - **[docx 技能](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md)**：使用绝对禁令：“❌ 错误示范：永远不要手动插入 Unicode 圆点作为列表符”，并配以“✅ 正确示范：使用配置好的 LevelFormat.BULLET”。
> - **[skill-creator 技能](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)**：设定了强制确认关口：在编写测试用例前，必须先问清楚边缘情况、输入输出格式，**拿到用户确认后，才能进入下一步**。

### 4. 分步骤检查清单 (Checklists)

人会犯错，大模型也会。在工作流的尾声，必须提供带有 `[ ]` 框的校验单，强迫 Agent 在交付结果前检查自己的作业。

- 设计具体的排错清单，针对该领域最常犯的错误进行精准拦截。
- 要求 Agent 在回复用户前，在内部思维过程中逐一核对这些清单。

> 🔗 **官方示例参考**：
>
> - **[xlsx 技能](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)**：提供了一份详尽的 `Formula Verification Checklist`（公式验证清单），要求 Agent 检查是否处理了 NaN 值、是否存在除以零（#DIV/0!）的风险等。
> - **[pptx 技能](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md)**：在 QA 环节不仅提供了清单，还进行了心理建设：“假设肯定有 Bug，你的任务是找到它们。如果你第一遍没找到，说明你找得不够仔细。”
> - **[mcp-builder 技能](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md)**：包含构建和测试的质量清单，强制检查无重复代码 (DRY)、一致的错误处理和清晰的工具描述。

### 5. 提供具体示例 (Examples & Templates)

抽象的指令不如具体的 `Input / Output` 示例。提供标准参考能极大提升模型输出的稳定性和准确率。

- **给指令模板**：列出常见任务对应的标准代码块、命令段或输出的 Markdown 格式。
- **给出错处理示例**：不仅教它怎么做对，还要教它出错时怎么看日志，该去读哪个字段。

> 🔗 **官方示例参考**：
>
> - **[pdf 技能](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)**：在文档末尾提供了一个清晰的 `Quick Reference` 表格，直接告诉 Agent：如果是合并 PDF，用 `pypdf` 库，代码写 `writer.add_page(page)`；如果是提取表格，用 `pdfplumber` 库。不给模型留任何自己瞎琢磨的空间。
> - **[xlsx 技能](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)**：不仅给了正确的公式代码，还展示了脚本报错时的 JSON 结构长什么样，教 Agent 如何读取 `error_summary` 字段来定位 `#REF!` 错误。
> - **[skill-creator 技能](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)**：专门定义了 `Examples pattern`，规定了如何为新技能编写输入/输出示例（Input / Output 对）。

---

## 示例

来自官方的 `xlsx` Skill：

---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
license: Proprietary. LICENSE.txt has complete terms
---

# Requirements for Outputs

## All Excel files

### Professional Font
- Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

# XLSX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

## Important Requirements

**LibreOffice Required for Formula Recalculation**: You can assume LibreOffice is installed for recalculating formula values using the `scripts/recalc.py` script. The script automatically configures LibreOffice on first run, including in sandboxed environments where Unix sockets are restricted (handled by `scripts/office/soffice.py`)

## Reading and analyzing data

### Data analysis with pandas
For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel File Workflows

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

### ❌ WRONG - Hardcoding Calculated Values
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ CORRECT - Using Excel Formulas
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

## Common Workflow
1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the scripts/recalc.py script
   ```bash
   python scripts/recalc.py output.xlsx
   ```
6. **Verify and fix any errors**:
   - The script returns JSON with error details
   - If `status` is `errors_found`, check `error_summary` for specific error types and locations
   - Fix the identified errors and recalculate again
   - Common errors to fix:
     - `#REF!`: Invalid cell references
     - `#DIV/0!`: Division by zero
     - `#VALUE!`: Wrong data type in formula
     - `#NAME?`: Unrecognized formula name

### Creating new Excel files

```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editing existing Excel files

```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## Recalculating formulas

Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `scripts/recalc.py` script to recalculate formulas:

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

Example:
```bash
python scripts/recalc.py output.xlsx 30
```

The script:
- Automatically sets up LibreOffice macro on first run
- Recalculates all formulas in all sheets
- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)
- Returns JSON with detailed error locations and counts
- Works on both Linux and macOS

## Formula Verification Checklist

Quick checks to ensure formulas work correctly:

### Essential Verification
- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)

### Common Pitfalls
- [ ] **NaN handling**: Check for null values with `pd.notna()`
- [ ] **Far-right columns**: FY data often in columns 50+
- [ ] **Multiple matches**: Search all occurrences, not just first
- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)
- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)
- [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets

### Formula Testing Strategy
- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly
- [ ] **Verify dependencies**: Check all cells referenced in formulas exist
- [ ] **Test edge cases**: Include zero, negative, and very large values

### Interpreting scripts/recalc.py Output
The script returns JSON with error details:
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## Best Practices

### Library Selection
- **pandas**: Best for data analysis, bulk operations, and simple data export
- **openpyxl**: Best for complex formatting, formulas, and Excel-specific features

### Working with openpyxl
- Cell indices are 1-based (row=1, column=1 refers to cell A1)
- Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`
- **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost
- For large files: Use `read_only=True` for reading or `write_only=True` for writing
- Formulas are preserved but not evaluated - use scripts/recalc.py to update values

### Working with pandas
- Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`
- For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Code Style Guidelines
**IMPORTANT**: When generating Python code for Excel operations:
- Write minimal, concise Python code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

**For Excel files themselves**:
- Add comments to cells with complex formulas or important assumptions
- Document data sources for hardcoded values
- Include notes for key calculations and model sections

---

## 结语

当你准备编写下一个 Skill 时，请将自己定位为一位**自动化流水线的设计师**。通过精心的触发器设计、上下文分层、红线门禁以及 QA 检查表，你将把 Claude 从一个“聊天助手”转化为一个高度可靠的“专业领域数字员工”。
