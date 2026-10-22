
from itertools import permutations

from .models import ShippingBox
def orientations(dimensions):
    """Return unique 90-degree rotations of a rectangular item."""
    return set(permutations(tuple(float(x) for x in dimensions)))


def overlaps(a, b):
    """Check whether two placed cuboids overlap."""
    ax, ay, az, al, aw, ah = a
    bx, by, bz, bl, bw, bh = b

    return (
        ax < bx + bl and ax + al > bx
        and ay < by + bw and ay + aw > by
        and az < bz + bh and az + ah > bz
    )


def can_pack(items, box_dimensions):
    """
    items: list of (length, width, height) tuples.
    box_dimensions: (length, width, height).

    Greedy placement; False means this heuristic could
    not find an arrangement, not necessarily that none exists.
    """
    L, W, H = map(float, box_dimensions)

    # Try the largest products first.
    items = sorted(
        items,
        key=lambda d: d[0] * d[1] * d[2],
        reverse=True,
    )

    placed = []

    for dimensions in items:
        candidates = [(0.0, 0.0, 0.0)]

        # Candidate positions at existing item boundaries.
        for x, y, z, l, w, h in placed:
            candidates.extend([
                (x + l, y, z),
                (x, y + w, z),
                (x, y, z + h),
            ])

        found = False

        for length, width, height in orientations(dimensions):
            if length > L or width > W or height > H:
                continue

            for x, y, z in candidates:
                if (
                    x + length > L
                    or y + width > W
                    or z + height > H
                ):
                    continue

                item = (
                    x, y, z, length, width, height
                )

                if any(overlaps(item, other) for other in placed):
                    continue

                placed.append(item)
                found = True
                break

            if found:
                break

        if not found:
            return False

    return True


def recommend_box(order):
    """Return the lowest-cost box found for an order."""
    items = []

    for order_item in order.items.select_related("product"):
        product = order_item.product

        items.extend(
            [
                (product.length, product.width, product.height)
            ] * order_item.quantity
        )

    if not items:
        return {
            "success": False,
            "message": "The order has no items.",
        }

    total_weight = sum(
        (
            item.product.weight * item.quantity
            for item in order.items.select_related("product")
        ),
        start=0,
    )

    candidates = ShippingBox.objects.filter(
        is_active=True,
        max_weight__gte=total_weight,
    ).order_by("cost")

    for box in candidates:
        fits = can_pack(
            items,
            (box.length, box.width, box.height),
        )

        if fits:
            return {
                "success": True,
                "box": box,
                "total_weight": total_weight,
                "box_cost": box.cost,
                "message": "Suitable box found.",
            }

    return {
        "success": False,
        "message": (
            "No available box could be recommended. "
            "Check box dimensions, weight capacity, "
            "or use a more advanced packing solver."
        ),
    }
