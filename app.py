# bungakuquote - 日替わり文学引用ミュージアム
# 小説・随筆・古典・詩歌から、1日1つずつ名文を「展示」する単一ファイルFlaskアプリ。
# 引用文はすべて著作権保護期間を満了した作品（パブリックドメイン）から採り、
# 青空文庫等の原文で wording を照合した。
from datetime import datetime
from zoneinfo import ZoneInfo
import random

from flask import Flask, abort, jsonify, redirect, render_template_string, url_for

app = Flask(__name__)

JST = ZoneInfo("Asia/Tokyo")

QUOTES = [
    {"id": 1, "genre": "小説", "work": "吾輩は猫である", "author": "夏目漱石",
     "text": "吾輩は猫である。名前はまだ無い。",
     "note": "漱石のデビュー作。猫の目を通して明治の人間模様を描く。"},
    {"id": 2, "genre": "小説", "work": "坊っちゃん", "author": "夏目漱石",
     "text": "親譲りの無鉄砲で小供の時から損ばかりしている。",
     "note": "漱石の代表作。無鉄砲な教師「坊っちゃん」の赴任先での騒動。"},
    {"id": 3, "genre": "小説", "work": "草枕", "author": "夏目漱石",
     "text": "山路を登りながら、こう考えた。智に働けば角が立つ。情に棹させば流される。意地を通せば窮屈だ。とかくに人の世は住みにくい。",
     "note": "「非人情」の小説。画工の山旅の思索から始まる。"},
    {"id": 4, "genre": "小説", "work": "こころ", "author": "夏目漱石",
     "text": "私はその人を常に先生と呼んでいた。だからここでもただ先生と書くだけで本名は打ち明けない。",
     "note": "「先生」と「私」の物語。漱石後期の代表作。"},
    {"id": 5, "genre": "小説", "work": "夢十夜", "author": "夏目漱石",
     "text": "こんな夢を見た。腕組をして枕元に坐っていると、仰向きに寝た女が、静かな声でもう死にますと云う。",
     "note": "十の夢を綴る幻想的な短編連作。第一夜の書き出し。"},
    {"id": 6, "genre": "小説", "work": "羅生門", "author": "芥川龍之介",
     "text": "或日の暮方の事である。一人の下人が、羅生門の下で雨やみを待っていた。",
     "note": "芥川初期の短編。『今昔物語集』を題材にした。"},
    {"id": 7, "genre": "小説", "work": "鼻", "author": "芥川龍之介",
     "text": "禅智内供の鼻と云えば、池の尾で知らない者はない。長さは五六寸あって上唇の上から顋の下まで下っている。",
     "note": "漱石に激賞された芥川の出世作。"},
    {"id": 8, "genre": "小説", "work": "蜘蛛の糸", "author": "芥川龍之介",
     "text": "ある日の事でございます。御釈迦様は極楽の蓮池のふちを、独りでぶらぶら御歩きになっていらっしゃいました。",
     "note": "芥川の児童向け短編。地獄に垂らされた一本の糸。"},
    {"id": 9, "genre": "小説", "work": "走れメロス", "author": "太宰治",
     "text": "メロスは激怒した。必ず、かの邪智暴虐の王を除かなければならぬと決意した。",
     "note": "太宰の短編。友のために走るメロスの物語。"},
    {"id": 10, "genre": "小説", "work": "人間失格", "author": "太宰治",
     "text": "恥の多い生涯を送って来ました。",
     "note": "太宰の代表作。主人公・大庭葉蔵の手記の冒頭。"},
    {"id": 11, "genre": "小説", "work": "銀河鉄道の夜", "author": "宮沢賢治",
     "text": "なにがしあわせかわからないです。ほんとうにどんなつらいことでも、それがただしいみちを進む中でのできごとなら、峠の上りも下りもみんなほんとうの幸福に近づく一あしずつですから。",
     "note": "賢治の代表作。燈台守がジョバンニをなぐさめる場面の言葉。"},
    {"id": 12, "genre": "小説", "work": "注文の多い料理店", "author": "宮沢賢治",
     "text": "二人の若い紳士が、すっかりイギリスの兵隊のかたちをして、ぴかぴかする鉄砲をかついで、白熊のような犬を二疋つれて、だいぶ山奥の、木の葉のかさかさしたとこを、こんなことを云いながら、あるいておりました。",
     "note": "賢治の童話集の表題作。山猫軒の不思議な注文。"},
    {"id": 13, "genre": "小説", "work": "山月記", "author": "中島敦",
     "text": "隴西の李徴は博学才穎、天宝の末年、若くして名を虎榜に連ね、ついで江南尉に補せられたが、性、狷介、自ら恃むところ頗る厚く、賤吏に甘んずるを潔しとしなかった。",
     "note": "中島敦の短編。虎になってしまった男・李徴の物語。"},
    {"id": 14, "genre": "小説", "work": "舞姫", "author": "森鴎外",
     "text": "石炭をば早や積み果てつ。中等室の卓のほとりはいと静にて、熾熱燈の光の晴れがましきも徒なり。",
     "note": "鴎外初期の短編。ドイツ留学中の恋を描く。"},
    {"id": 15, "genre": "小説", "work": "檸檬", "author": "梶井基次郎",
     "text": "えたいの知れない不吉な塊が私の心を始終圧えつけていた。焦躁と言おうか、嫌悪と言おうか。",
     "note": "梶井基次郎の短編。一個の檸檬に心がほどける。"},
    {"id": 16, "genre": "小説", "work": "ごん狐", "author": "新美南吉",
     "text": "これは、私が小さいときに、村の茂平というおじいさんからきいたお話です。",
     "note": "新美南吉の童話。小学校の教科書でも親しまれる。"},
    {"id": 17, "genre": "随筆・評論", "work": "学問のすゝめ", "author": "福沢諭吉",
     "text": "天は人の上に人を造らず人の下に人を造らずと言えり。",
     "note": "福沢諭吉の代表作。有名な書き出し。"},
    {"id": 18, "genre": "随筆・評論", "work": "茶の本", "author": "岡倉天心",
     "text": "Tea began as a medicine and grew into a beverage.",
     "note": "岡倉天心が英語で著した茶の本『The Book of Tea』の冒頭。"},
    {"id": 19, "genre": "古典", "work": "源氏物語", "author": "紫式部",
     "text": "いづれの御時にか、女御、更衣あまたさぶらひたまひけるなかに、いとやむごとなき際にはあらぬが、すぐれて時めきたまふありけり。",
     "note": "平安時代の長編物語。「桐壺」の書き出し。"},
    {"id": 20, "genre": "古典", "work": "枕草子", "author": "清少納言",
     "text": "春はあけぼの。やうやう白くなりゆく山際、少し明かりて、紫だちたる雲の細くたなびきたる。",
     "note": "清少納言の随筆。冒頭の段。"},
    {"id": 21, "genre": "古典", "work": "方丈記", "author": "鴨長明",
     "text": "ゆく河の流れは絶えずして、しかももとの水にあらず。よどみに浮かぶうたかたは、かつ消えかつ結びて、久しくとどまりたるためしなし。",
     "note": "鴨長明の随筆。無常観を述べた書き出し。"},
    {"id": 22, "genre": "古典", "work": "徒然草", "author": "吉田兼好",
     "text": "つれづれなるままに、日暮らし、硯にむかひて、心にうつりゆくよしなしごとを、そこはかとなく書きつくれば、あやしうこそものぐるほしけれ。",
     "note": "吉田兼好の随筆。序段の書き出し。"},
    {"id": 23, "genre": "古典", "work": "平家物語", "author": "作者不詳",
     "text": "祇園精舎の鐘の声、諸行無常の響きあり。沙羅双樹の花の色、盛者必衰の理をあらはす。",
     "note": "軍記物語。栄華の盛衰を告げる冒頭。"},
    {"id": 24, "genre": "古典", "work": "奥の細道", "author": "松尾芭蕉",
     "text": "月日は百代の過客にして、行きかふ年もまた旅人なり。",
     "note": "松尾芭蕉の紀行文。旅の序文。"},
    {"id": 25, "genre": "詩歌", "work": "古今和歌集", "author": "小野小町",
     "text": "花の色は うつりにけりな いたづらに わが身世にふる ながめせしまに",
     "note": "『古今和歌集』の小野小町の歌。色あせる花と人の世を重ねる。"},
    {"id": 26, "genre": "詩歌", "work": "俳句", "author": "正岡子規",
     "text": "柿くへば 鐘が鳴るなり 法隆寺",
     "note": "正岡子規の俳句。法隆寺にちなむ作として知られる。"},
    {"id": 27, "genre": "詩歌", "work": "君死にたまふことなかれ", "author": "与謝野晶子",
     "text": "ああをとうとよ、君を泣く、君死にたまふこと勿れ。",
     "note": "日露戦争のさなか、弟を思って発表した詩の書き出し。"},
    {"id": 28, "genre": "詩歌", "work": "一握の砂", "author": "石川啄木",
     "text": "はたらけど はたらけど猶 わが生活 楽にならざり ぢっと手を見る",
     "note": "短歌集『一握の砂』から。働けど暮らしの楽にならない嘆き。"},
    {"id": 29, "genre": "詩歌", "work": "雨ニモマケズ", "author": "宮沢賢治",
     "text": "雨ニモマケズ 風ニモマケズ 雪ニモ夏ノ暑サニモマケヌ 丈夫ナカラダヲモチ",
     "note": "賢治の手帳に残された詩。冒頭の部分。"},
    {"id": 30, "genre": "世界文学", "work": "Hamlet", "author": "William Shakespeare",
     "text": "To be, or not to be, that is the question.",
     "note": "シェイクスピアの悲劇『ハムレット』。有名な独白の書き出し。"},
]

BY_ID = {q["id"]: q for q in QUOTES}
GENRES = []
for q in QUOTES:
    if q["genre"] not in GENRES:
        GENRES.append(q["genre"])


def today_jst():
    return datetime.now(JST).date()


def daily_quote(day=None):
    day = day or today_jst()
    return QUOTES[day.toordinal() % len(QUOTES)]


def citation(q):
    return "「" + q["text"] + "」――" + q["author"] + "『" + q["work"] + "』"


CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: #f5f1e8; color: #2b2620;
  font-family: "Hiragino Mincho ProN", "Yu Mincho", "YuMincho", Georgia, serif;
  line-height: 1.9;
}
header { text-align: center; padding: 2.2rem 1rem 0.4rem; }
header h1 { font-size: 1.55rem; letter-spacing: 0.22em; margin: 0; font-weight: 600; }
header p { color: #7a6f5c; font-size: 0.85rem; letter-spacing: 0.12em; margin: 0.3rem 0 0; }
main { max-width: 720px; margin: 0 auto; padding: 1.2rem 1rem 3rem; }
.exhibit {
  background: #fffdf8; border: 1px solid #cbbfa5; outline: 4px solid #fffdf8;
  box-shadow: 0 0 0 5px #cbbfa5, 0 10px 30px rgba(80, 64, 32, 0.12);
  padding: 2.4rem 2rem 1.8rem; margin-top: 1.4rem;
}
.exhibit .date { text-align: center; color: #8a7a5c; font-size: 0.85rem; letter-spacing: 0.2em; }
.exhibit blockquote {
  margin: 1.4rem 0 1.2rem; font-size: 1.28rem; line-height: 2.15; text-align: justify;
}
.plate { border-top: 1px solid #ddd2ba; padding-top: 1rem; text-align: center; }
.plate .work { font-size: 1.05rem; }
.plate .author { color: #5c5240; }
.badge {
  display: inline-block; border: 1px solid #a08c5f; color: #7a6438; border-radius: 999px;
  padding: 0.05rem 0.7rem; font-size: 0.78rem; letter-spacing: 0.15em; margin-bottom: 0.4rem;
}
.note { color: #6d6250; font-size: 0.92rem; text-align: center; margin-top: 0.7rem; }
.actions { text-align: center; margin-top: 1.3rem; }
button, .btn {
  font-family: inherit; background: #3d3427; color: #f7f2e7; border: none; cursor: pointer;
  padding: 0.55rem 1.3rem; font-size: 0.9rem; letter-spacing: 0.1em; text-decoration: none;
  display: inline-block; margin: 0 0.25rem;
}
button:hover, .btn:hover { background: #5a4c36; }
.btn.sub { background: transparent; color: #3d3427; border: 1px solid #3d3427; }
nav.links { text-align: center; margin-top: 1.6rem; }
nav.links a { color: #6b5a38; margin: 0 0.8rem; font-size: 0.92rem; }
h2.genre { font-size: 1.1rem; border-bottom: 2px solid #cbbfa5; padding-bottom: 0.3rem; margin-top: 2.2rem; letter-spacing: 0.15em; }
.card {
  background: #fffdf8; border: 1px solid #ddd2ba; padding: 1.1rem 1.3rem; margin: 0.9rem 0;
}
.card blockquote { margin: 0 0 0.5rem; font-size: 1.02rem; }
.card .meta { color: #6d6250; font-size: 0.88rem; }
.card .meta a { color: #6b5a38; }
footer { text-align: center; color: #9a8c70; font-size: 0.8rem; padding: 0 1rem 2rem; }
"""

SCRIPT = """
function copyQuote(id) {
  var el = document.getElementById('citation-' + id);
  var text = el.textContent;
  function done() {
    var btn = document.getElementById('copy-btn-' + id);
    var old = btn.textContent;
    btn.textContent = 'コピーしました';
    setTimeout(function () { btn.textContent = old; }, 1600);
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done, done);
  } else {
    var ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    done();
  }
}
"""

BASE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} | bungakuquote</title>
<style>{{ css|safe }}</style>
</head>
<body>
<header>
<h1>文学引用ミュージアム</h1>
<p>bungakuquote ― 日替わりで名文を展示します</p>
</header>
<main>
{{ body|safe }}
</main>
<footer>収録の引用はすべてパブリックドメインの作品から採り、原文と照合しています。</footer>
<script>{{ script|safe }}</script>
</body>
</html>
"""


def render_page(title, body):
    return render_template_string(BASE, title=title, body=body, css=CSS, script=SCRIPT)


def exhibit_html(q, day_label):
    body = f"""
<section class="exhibit">
  <div class="date">{day_label}</div>
  <blockquote>{q['text']}</blockquote>
  <div class="plate">
    <div><span class="badge">{q['genre']}</span></div>
    <div class="work">『{q['work']}』</div>
    <div class="author">{q['author']}</div>
    <p class="note">{q['note']}</p>
  </div>
  <div class="actions">
    <span id="citation-{q['id']}" hidden>{citation(q)}</span>
    <button id="copy-btn-{q['id']}" onclick="copyQuote({q['id']})">引用文をコピー</button>
    <a class="btn sub" href="/random">ランダムに1つ</a>
  </div>
</section>
<nav class="links">
  <a href="/all">展示一覧</a>
  <a href="/quote/{q['id']}">この展示のページ</a>
</nav>
"""
    return render_page("本日の展示", body)


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "quotes": len(QUOTES)})


@app.route("/")
def index():
    day = today_jst()
    q = daily_quote(day)
    label = f"{day.year}年{day.month}月{day.day}日 ― 本日の展示 No.{q['id']}"
    return exhibit_html(q, label)


@app.route("/quote/<int:qid>")
def quote_page(qid):
    q = BY_ID.get(qid)
    if q is None:
        abort(404)
    return exhibit_html(q, f"展示 No.{q['id']}")


@app.route("/random")
def random_quote():
    q = random.choice(QUOTES)
    return redirect(url_for("quote_page", qid=q["id"]))


@app.route("/all")
def all_quotes():
    parts = []
    for genre in GENRES:
        parts.append(f'<h2 class="genre">{genre}</h2>')
        for q in QUOTES:
            if q["genre"] != genre:
                continue
            parts.append(
                f'<div class="card"><blockquote>{q["text"]}</blockquote>'
                f'<div class="meta">『{q["work"]}』 {q["author"]} ― '
                f'<a href="/quote/{q["id"]}">展示 No.{q["id"]}</a></div></div>'
            )
    parts.append('<nav class="links"><a href="/">本日の展示へ</a></nav>')
    return render_page("展示一覧", "\n".join(parts))


@app.route("/api/today")
def api_today():
    day = today_jst()
    q = daily_quote(day)
    return jsonify({"date": day.isoformat(), **q, "citation": citation(q)})


@app.route("/api/random")
def api_random():
    q = random.choice(QUOTES)
    return jsonify({**q, "citation": citation(q)})


@app.route("/api/quote/<int:qid>")
def api_quote(qid):
    q = BY_ID.get(qid)
    if q is None:
        abort(404)
    return jsonify({**q, "citation": citation(q)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
