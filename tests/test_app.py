import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as m


client = m.app.test_client()


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"
    assert r.get_json()["quotes"] == 30


def test_quotes_data_integrity():
    assert len(m.QUOTES) == 30
    assert [q["id"] for q in m.QUOTES] == list(range(1, 31))
    for q in m.QUOTES:
        assert q["text"] and q["work"] and q["author"] and q["genre"] and q["note"]
    genres = {q["genre"] for q in m.QUOTES}
    assert genres == {"小説", "随筆・評論", "古典", "詩歌", "世界文学"}


def test_index_shows_daily_quote():
    r = client.get("/")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    q = m.daily_quote()
    assert q["text"] in html
    assert q["work"] in html
    assert "本日の展示" in html


def test_daily_quote_is_deterministic():
    d = date(2026, 11, 27)
    assert m.daily_quote(d) is m.daily_quote(d)
    # 30日周期で全件を一巡する
    seen = {m.daily_quote(date.fromordinal(d.toordinal() + i))["id"] for i in range(30)}
    assert seen == set(range(1, 31))


def test_quote_page_and_404():
    r = client.get("/quote/1")
    assert r.status_code == 200
    assert "吾輩は猫である" in r.get_data(as_text=True)
    assert client.get("/quote/999").status_code == 404


def test_all_lists_every_work():
    html = client.get("/all").get_data(as_text=True)
    for q in m.QUOTES:
        assert q["work"] in html


def test_random_redirects_to_a_quote():
    r = client.get("/random")
    assert r.status_code == 302
    assert "/quote/" in r.headers["Location"]


def test_api_today_and_quote():
    r = client.get("/api/today")
    assert r.status_code == 200
    data = r.get_json()
    assert data["id"] == m.daily_quote()["id"]
    assert data["citation"].endswith("『" + data["work"] + "』")
    r2 = client.get("/api/quote/30")
    assert r2.get_json()["author"] == "William Shakespeare"
    assert client.get("/api/quote/999").status_code == 404


def test_script_not_escaped():
    # render_template_string で JS が HTML エスケープされるとコピー機能が死ぬ（過去の事故）。
    html = client.get("/").get_data(as_text=True)
    assert "&#39;" not in html
    assert "navigator.clipboard.writeText(text).then(done, done)" in html
