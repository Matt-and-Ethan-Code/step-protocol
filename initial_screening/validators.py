from django.core.exceptions import ValidationError


def validate_sequential_order(orders: list[int], *, label: str = "item") -> None:
    """Raise ValidationError unless orders form 1..N with no repeats or gaps."""
    expected = list(range(1, len(orders) + 1))
    if sorted(orders) != expected:
        raise ValidationError(
            f"{label} order values must start at 1 and increase by 1 with no repeats or "
            f"gaps (got {sorted(orders)}, expected {expected})."
        )
