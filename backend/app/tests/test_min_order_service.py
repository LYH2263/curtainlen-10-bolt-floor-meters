import os, tempfile
os.environ["DATA_DIR"] = tempfile.mkdtemp()
import pytest
from fastapi import HTTPException
from app import seed
from app.repositories import fabrics, history
from app.services import estimate_service

seed.init_db()

def test_order_equals_base_when_m_smaller():
    r = estimate_service.run_estimate(1, 1, save=False, note="")
    assert r["meters"] == 14.25
    assert r["min_order_m"] == 1.0
    assert r["order_meters"] == 14.25

def test_order_floored_when_m_larger():
    fabrics.update_min_order(1, 20.0)
    r = estimate_service.run_estimate(1, 1, save=False, note="")
    assert r["meters"] == 14.25
    assert r["order_meters"] == 20.0
    fabrics.update_min_order(1, 1.0)

def test_save_snapshot_immune_to_later_m_change():
    r = estimate_service.run_estimate(1, 1, save=True, note="")
    run = history.get_run(r["run_id"])
    assert run["result"]["meters"] == 14.25
    assert run["result"]["min_order_m"] == 1.0
    assert run["result"]["order_meters"] == 14.25
    fabrics.update_min_order(1, 50.0)
    again = history.get_run(r["run_id"])
    assert again["result"]["order_meters"] == 14.25
    assert again["result"]["min_order_m"] == 1.0
    fabrics.update_min_order(1, 1.0)

def test_non_positive_m_fails_and_writes_nothing():
    fabrics.update_min_order(1, 0.0)
    before = len(history.list_runs(1000))
    with pytest.raises(HTTPException) as e:
        estimate_service.run_estimate(1, 1, save=True, note="")
    assert e.value.status_code == 422
    assert len(history.list_runs(1000)) == before
    fabrics.update_min_order(1, 1.0)
