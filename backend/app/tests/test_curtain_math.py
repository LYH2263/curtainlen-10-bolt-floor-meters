import pytest
from app.engines.curtain_math import fabric_meters

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_min_order_below_base_keeps_meters():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, min_order_m=1.0)
    assert r["min_order_m"] == 1.0
    assert r["order_meters"] == r["meters"] == 14.25

def test_min_order_above_base_floors_order():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8, min_order_m=5.0)
    assert r["meters"] == 2.0
    assert r["order_meters"] == 5.0

def test_min_order_non_positive_rejected():
    with pytest.raises(ValueError):
        fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8, min_order_m=0)
    with pytest.raises(ValueError):
        fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8, min_order_m=-3)
