from typing import Any


def with_levels(ctx: dict[str, Any]) -> dict[str,Any]:
    levels: list[str] = []
    for i in range(1, 11):
        levels.append(str(i))
    ctx["levels"] = levels
    return ctx
