# LangGraph 协议评审项目

这是一个基于 **LangGraph** 的完整协议评审工程，包含 3 个独立评审技能（skills）：

1. **名称命名评审（Skill 1）**：检查协议名称是否符合 PascalCase、长度与可读性要求。
2. **标识符命名评审（Skill 2）**：检查字段标识符是否符合 snake_case、唯一性与语义长度要求。
3. **协议描述评审（Skill 3）**：检查协议描述是否完整，是否包含字段、约束、错误处理等关键要素。

## 项目结构

```text
.
├── protocol_review/
│   ├── __init__.py
│   ├── cli.py
│   ├── graph.py
│   ├── skills.py
│   └── state.py
├── examples/
│   └── sample_protocol.json
├── tests/
│   └── test_graph.py
├── requirements.txt
└── README.md
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 使用

1. 准备输入 JSON（可参考 `examples/sample_protocol.json`）
2. 执行命令：

```bash
python -m protocol_review.cli --input examples/sample_protocol.json
```

## 输出说明

输出包含：

- `reviews.name_naming`：名称命名评审结果
- `reviews.identifier_naming`：标识符命名评审结果
- `reviews.protocol_description`：协议描述评审结果
- `summary`：总分、是否通过、未通过项、整改建议状态

## 测试

```bash
pytest -q
```
