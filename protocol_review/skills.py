from __future__ import annotations

import re
from typing import Dict, List

from .state import ProtocolReviewState, ReviewItem


CAMEL_CASE_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def _build_review(compliant: bool, score: int, issues: List[str], suggestions: List[str]) -> ReviewItem:
    return {
        "compliant": compliant,
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
    }


def name_naming_skill(state: ProtocolReviewState) -> ProtocolReviewState:
    """Skill 1: 评审协议名称命名是否合规。"""
    name = state["protocol_name"].strip()
    issues: List[str] = []
    suggestions: List[str] = []
    score = 100

    if not name:
        issues.append("协议名称不能为空。")
        suggestions.append("请提供有业务语义的协议名称，例如 PaymentRequestProtocol。")
        score -= 60
    else:
        if not CAMEL_CASE_RE.match(name):
            issues.append("协议名称建议使用 PascalCase（首字母大写驼峰）。")
            suggestions.append("示例：PaymentRequestProtocol、AccountSyncMessage。")
            score -= 30

        if len(name) < 4:
            issues.append("协议名称过短，可读性不足。")
            suggestions.append("建议至少 4 个字符，并包含业务语义。")
            score -= 15

        if " " in name or "-" in name:
            issues.append("协议名称不应包含空格或连字符。")
            suggestions.append("请使用无分隔符驼峰命名。")
            score -= 15

    compliant = score >= 80 and not issues
    state["reviews"]["name_naming"] = _build_review(compliant, max(score, 0), issues, suggestions)
    return state


def identifier_naming_skill(state: ProtocolReviewState) -> ProtocolReviewState:
    """Skill 2: 评审标识符命名是否合规。"""
    identifiers = state["identifiers"]
    issues: List[str] = []
    suggestions: List[str] = []
    score = 100

    if not identifiers:
        issues.append("未提供任何标识符。")
        suggestions.append("请至少提供协议字段、常量或枚举标识符。")
        score -= 60

    seen = set()
    for identifier in identifiers:
        if identifier in seen:
            issues.append(f"标识符 `{identifier}` 重复定义。")
            suggestions.append("请确保标识符在同一协议范围内唯一。")
            score -= 10
        seen.add(identifier)

        if not SNAKE_CASE_RE.match(identifier):
            issues.append(f"标识符 `{identifier}` 未采用 snake_case。")
            suggestions.append(f"建议将 `{identifier}` 修改为小写下划线风格。")
            score -= 10

        if len(identifier) < 3:
            issues.append(f"标识符 `{identifier}` 长度过短，语义不清。")
            suggestions.append("建议标识符长度不小于 3 且可表达具体业务含义。")
            score -= 5

    compliant = score >= 80 and not issues
    state["reviews"]["identifier_naming"] = _build_review(compliant, max(score, 0), issues, suggestions)
    return state


def protocol_description_skill(state: ProtocolReviewState) -> ProtocolReviewState:
    """Skill 3: 评审协议描述是否合规。"""
    description = state["description"].strip()
    issues: List[str] = []
    suggestions: List[str] = []
    score = 100

    if not description:
        issues.append("协议描述不能为空。")
        suggestions.append("请补充协议目标、关键字段和约束条件。")
        score -= 70
    else:
        if len(description) < 40:
            issues.append("协议描述过短，信息不完整。")
            suggestions.append("建议补充场景、字段含义、边界条件与错误处理策略。")
            score -= 25

        required_keywords = ["字段", "约束", "错误"]
        missing_keywords = [kw for kw in required_keywords if kw not in description]
        if missing_keywords:
            issues.append(f"协议描述缺少关键要素：{', '.join(missing_keywords)}。")
            suggestions.append("建议明确字段定义、约束规则、错误码/异常处理。")
            score -= 25

    compliant = score >= 80 and not issues
    state["reviews"]["protocol_description"] = _build_review(compliant, max(score, 0), issues, suggestions)
    return state


def build_summary(state: ProtocolReviewState) -> ProtocolReviewState:
    reviews: Dict[str, ReviewItem] = state["reviews"]
    total = sum(item["score"] for item in reviews.values())
    count = max(len(reviews), 1)
    average = round(total / count, 2)
    failed = [name for name, item in reviews.items() if not item["compliant"]]

    state["summary"] = {
        "average_score": average,
        "passed": len(failed) == 0,
        "failed_items": failed,
        "action": "通过" if not failed else "需整改",
    }
    return state
