from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    try:
        calc = fabric_meters(
            w["width"], w["height"], fullness,
            f["hem_top"], f["hem_bottom"], f["fabric_width"],
            min_order_m=f.get("min_order_m"),
        )
    except ValueError as e:
        # 起订米数非正等非法数据：校验失败，不写历史
        raise HTTPException(422, str(e))
    run_id = history.insert_run(window_id, fabric_id, calc, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **calc}
