from typing import Any


def with_levels(ctx: dict[str, Any]) -> dict[str,Any]:
    """
    Add a `levels: [0, 1, 2, ..., 10]` list to the ctx
    """
    levels: list[str] = []
    for i in range(0, 11):
        levels.append(str(i))
    ctx["levels"] = levels
    return ctx
