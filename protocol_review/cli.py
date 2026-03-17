from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graph import review_protocol


def main() -> None:
    parser = argparse.ArgumentParser(description="LangGraph 协议评审工具")
    parser.add_argument("--input", required=True, help="输入 JSON 文件路径")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = review_protocol(
        protocol_name=payload.get("protocol_name", ""),
        identifiers=payload.get("identifiers", []),
        description=payload.get("description", ""),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
