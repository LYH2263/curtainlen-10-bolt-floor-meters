from app.engines.helpers import ceil_units


def apply_min_order(meters: float, min_order_m: float) -> float:
    """整匹起订托底：订货米数 = max(基础米数, M)。M 非正为非法数据。"""
    m = float(min_order_m)
    if m <= 0:
        raise ValueError("min order meters must be positive")
    return round(max(float(meters), m), 2)


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
    min_order_m: float = None,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    finished_w = float(window_w) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    meters = panels * cut_h
    result = {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
    }
    if min_order_m is not None:
        result["min_order_m"] = float(min_order_m)
        result["order_meters"] = apply_min_order(result["meters"], min_order_m)
    return result
