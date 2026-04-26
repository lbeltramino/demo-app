#!/usr/bin/env python3
"""Report builder server - generates HTML reports from listing data."""
import json
import os
import ssl
import time
from pathlib import Path
from statistics import median
from datetime import datetime, timezone
import uuid

from flask import Flask, request, send_file, jsonify, render_template_string

app = Flask(__name__)

API_BASE = os.environ.get("API_URL", "https://api.sosiva451.com/Avisos")
DATA_DIR = os.environ.get("DATA_DIR", "/data")
TEMPLATE_FILE = Path(__file__).parent / "template.py"

OUTPUT_JSON_DIR = Path(DATA_DIR) / "reports"
OUTPUT_HTML_DIR = Path(DATA_DIR) / "reports"

OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_HTML_DIR.mkdir(parents=True, exist_ok=True)

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    FULL_TEMPLATE = f.read()

def get_report_list():
    reports = []
    for html_file in sorted(OUTPUT_HTML_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True):
        report_id = html_file.stem
        json_file = OUTPUT_JSON_DIR / f"{report_id}.json"
        meta = {}
        if json_file.exists():
            try:
                with open(json_file) as f:
                    data = json.load(f)
                    meta = data.get("meta", {})
                    meta["analytics"] = data.get("analytics", {})
            except:
                pass
        reports.append({
            "id": report_id,
            "filename": html_file.name,
            "modified": html_file.stat().st_mtime,
            "meta": meta,
        })
    return reports

def fetch_aviso(aid):
    import urllib.request
    req = urllib.request.Request(f"{API_BASE}/{aid}", headers={"User-Agent": "Mozilla/5.0"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
        return json.loads(r.read().decode())

def extract_photos(api_payload):
    mm = api_payload.get("Multimedia_s") or []
    out = []
    for m in sorted(mm, key=lambda x: x.get("Orden") or 0):
        if m.get("IdTipoMultimedia") != 1:
            continue
        out.append({
            "full": m.get("Url"),
            "medium": m.get("Medium_U") or m.get("Medium"),
            "small": m.get("Small_U") or m.get("Small"),
        })
    return out

def enrich_listings(entries):
    for item in entries:
        aid = item.get("id_aviso_argenprop")
        item["fotos"] = []
        item["api_error"] = None
        if not aid:
            item["api_error"] = "missing_id"
            continue
        try:
            payload = fetch_aviso(aid)
            item["fotos"] = extract_photos(payload)
            item["precio_publicado_usd"] = payload.get("Precio_i")
            item["titulo_api"] = payload.get("Title") or payload.get("h1")
            item["direccion_calle"] = (payload.get("Direccion_NombreCalle_t") or "").strip() or None
            item["barrio_api"] = (payload.get("Barrio_t") or "").strip() or None
            item["localidad_api"] = (payload.get("Localidad_t") or "").strip() or None
        except Exception as e:
            item["api_error"] = str(e)[:200]
        time.sleep(0.12)

def seg_stats(items):
    prices = [a["price_usd_numeric"] for a in items if a.get("price_usd_numeric")]
    m2s = [a["superficie_cubierta_m2"] for a in items if a.get("superficie_cubierta_m2")]
    pm2 = []
    for a in items:
        p, m = a.get("price_usd_numeric"), a.get("superficie_cubierta_m2")
        if p and m and m > 0:
            pm2.append(p / m)
    exp = sum(1 for a in items if a.get("has_expensas_mention"))
    return {
        "n": len(items),
        "precio_median": median(prices) if prices else None,
        "precio_min": min(prices) if prices else None,
        "precio_max": max(prices) if prices else None,
        "m2_median": median(m2s) if m2s else None,
        "usd_m2_median": median(pm2) if pm2 else None,
        "usd_m2_min": min(pm2) if pm2 else None,
        "usd_m2_max": max(pm2) if pm2 else None,
        "con_expensas_en_texto": exp,
        "pct_expensas": round(100 * exp / len(items), 1) if items else 0,
    }

def analytics(data):
    return {
        "dorm_2": seg_stats(data.get("dormitorios_2", {}).get("avisos", [])),
        "dorm_3": seg_stats(data.get("dormitorios_3", {}).get("avisos", [])),
        "global": seg_stats(
            data.get("dormitorios_2", {}).get("avisos", []) + data.get("dormitorios_3", {}).get("avisos", [])
        ),
    }

def build_report(data):
    for key in ("dormitorios_2", "dormitorios_3"):
        if key in data:
            enrich_listings(data[key]["avisos"])
    data["meta"]["enriched_at_utc"] = datetime.now(timezone.utc).isoformat()
    data["meta"]["photo_source"] = "https://api.sosiva451.com/Avisos/{id} → Multimedia_s"
    data["analytics"] = analytics(data)
    return data

def generate_html(data):
    payload = json.dumps(data, ensure_ascii=False)
    html = FULL_TEMPLATE.replace("__DATA_JSON__", payload)
    return html

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET", "POST"])
def index():
    reports = get_report_list()
    current_report_id = request.args.get("report")
    
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file provided", 400
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e}", 400
        
        data = build_report(data)
        
        report_id = str(uuid.uuid4())[:8]
        output_json = OUTPUT_JSON_DIR / f"{report_id}.json"
        output_html = OUTPUT_HTML_DIR / f"{report_id}.html"
        
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        html_content = generate_html(data)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        total = len(data.get("dormitorios_2", {}).get("avisos", [])) + len(data.get("dormitorios_3", {}).get("avisos", []))
        reports_json = json.dumps(get_report_list())
        success = f'<div class="success"><h3>✓ Reporte generado: {total} listings</h3><p><a href="/?report={report_id}">Ver reporte</a></p></div>'
        return render_template_string(INDEX_HTML.replace("__REPORTS_JSON__", reports_json).replace("__SUCCESS__", success))
    
    if current_report_id:
        html_file = OUTPUT_HTML_DIR / f"{current_report_id}.html"
        if html_file.exists():
            return send_file(html_file)
    
    reports_json = json.dumps(get_report_list())
    return render_template_string(INDEX_HTML.replace("__REPORTS_JSON__", reports_json))

@app.route("/api/reports")
def list_reports():
    return jsonify(get_report_list())

@app.route("/api/report/<report_id>")
def get_report(report_id):
    json_file = OUTPUT_JSON_DIR / f"{report_id}.json"
    if not json_file.exists():
        return jsonify({"error": "Report not found"}), 404
    return send_file(json_file, mimetype="application/json")

@app.route("/api/report/<report_id>", methods=["DELETE"])
def delete_report(report_id):
    json_file = OUTPUT_JSON_DIR / f"{report_id}.json"
    html_file = OUTPUT_HTML_DIR / f"{report_id}.html"
    deleted = []
    if json_file.exists():
        json_file.unlink()
        deleted.append("json")
    if html_file.exists():
        html_file.unlink()
        deleted.append("html")
    if not deleted:
        return jsonify({"error": "Report not found"}), 404
    return jsonify({"status": "deleted", "files": deleted})

UPLOAD_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Atlas - Report Builder</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    :root { --bg0: #0f1419; --bg1: #1a222d; --paper: #f3ead8; --accent: #c45c3e; --accent2: #2d6a8f; }
    body { margin: 0; font-family: 'Outfit', system-ui, sans-serif; background: var(--bg0); color: var(--paper); min-height: 100vh; }
    .nav { position: fixed; top: 0; left: 0; right: 0; height: 60px; background: var(--bg1); border-bottom: 1px solid rgba(243,234,216,.08); display: flex; align-items: center; padding: 0 1.5rem; z-index: 100; }
    .nav h1 { font-family: 'Fraunces', serif; font-size: 1.25rem; margin: 0; background: linear-gradient(120deg, var(--paper) 0%, #d4c4a8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hamburger { margin-left: auto; cursor: pointer; padding: 0.5rem; display: flex; flex-direction: column; gap: 5px; }
    .hamburger span { width: 24px; height: 2px; background: var(--paper); transition: 0.3s; }
    .menu { display: none; position: fixed; top: 60px; right: 0; bottom: 0; width: 320px; background: var(--bg1); border-left: 1px solid rgba(243,234,216,.1); padding: 1rem; overflow-y: auto; }
    .menu.open { display: block; }
    .menu h2 { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(243,234,216,.5); margin: 0 0 1rem; }
    .report-item { padding: 0.75rem 1rem; background: var(--bg0); border-radius: 8px; margin-bottom: 0.5rem; cursor: pointer; transition: 0.2s; }
    .report-item:hover { background: rgba(196,92,62,.2); }
    .report-item.active { border: 1px solid var(--accent); }
    .report-item .title { font-weight: 600; font-size: 0.9rem; }
    .report-item .meta { font-size: 0.75rem; color: rgba(243,234,216,.6); margin-top: 0.25rem; }
    .main { padding: 80px 2rem 2rem; max-width: 600px; margin: 0 auto; }
    .upload { padding: 2rem; background: var(--bg1); border-radius: 14px; border: 1px solid rgba(243,234,216,.08); }
    .upload h2 { font-family: 'Fraunces', serif; font-size: 1.5rem; margin: 0 0 1rem; }
    .upload input[type="file"] { display: block; margin: 1rem 0; width: 100%; }
    .upload button { background: var(--accent); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-size: 1rem; width: 100%; }
    .upload button:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <nav class="nav">
    <h1>Atlas · Rosario</h1>
    <div class="hamburger" onclick="this.classList.toggle('open'); document.querySelector('.menu').classList.toggle('open')">
      <span></span><span></span><span></span>
    </div>
  </nav>
  <div class="menu">
    <h2>Reportes guardados</h2>
    <div id="reportList"></div>
  </div>
  <div class="main">
    <div class="upload">
      <h2>Subir nuevos datos</h2>
      <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".json">
        <button type="submit">Generar Reporte</button>
      </form>
    </div>
  </div>
  <script>
    const reports = __REPORTS_JSON__;
    const currentId = new URLSearchParams(window.location.search).get('report');
    document.getElementById('reportList').innerHTML = reports.map(r => {
      const meta = r.meta || {};
      const city = meta.ciudad || 'Rosario';
      const range = meta.precio_desde ? `USD ${meta.precio_desde}-${meta.precio_hasta}` : '';
      const date = new Date(r.modified * 1000).toLocaleDateString('es-AR');
      return `<div class="report-item${r.id === currentId ? ' active' : ''}" onclick="window.location.href='/?report=${r.id}'">
        <div class="title">${city}</div>
        <div class="meta">${range} · ${date}</div>
      </div>`;
    }).join('');
  </script>
</body>
</html>"""

UPLOAD_SUCCESS_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Atlas - Report Generated</title>
  <style>
    :root { --bg0: #0f1419; --bg1: #1a222d; --paper: #f3ead8; --accent: #c45c3e; }
    body { margin: 0; font-family: system-ui, sans-serif; background: var(--bg0); color: var(--paper); padding: 2rem; text-align: center; }
    a { color: var(--accent); }
  </style>
</head>
<body>
  <h1>✓ Reporte generado: {{ total }} listings</h1>
  <p><a href="/?report={{ report_id }}">Ver reporte</a></p>
  <p><a href="/">Subir otro</a></p>
</body>
</html>"""

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Atlas - Report Builder</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    :root { --bg0: #0f1419; --bg1: #1a222d; --paper: #f3ead8; --accent: #c45c3e; --accent2: #2d6a8f; }
    body { margin: 0; font-family: 'Outfit', system-ui, sans-serif; background: var(--bg0); color: var(--paper); min-height: 100vh; }
    .nav { position: fixed; top: 0; left: 0; right: 0; height: 60px; background: var(--bg1); border-bottom: 1px solid rgba(243,234,216,.08); display: flex; align-items: center; padding: 0 1.5rem; z-index: 100; }
    .nav h1 { font-family: 'Fraunces', serif; font-size: 1.25rem; margin: 0; background: linear-gradient(120deg, var(--paper) 0%, #d4c4a8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hamburger { margin-left: auto; cursor: pointer; padding: 0.5rem; display: flex; flex-direction: column; gap: 5px; }
    .hamburger span { width: 24px; height: 2px; background: var(--paper); transition: 0.3s; }
    .hamburger:hover span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
    .hamburger:hover span:nth-child(2) { opacity: 0; }
    .hamburger:hover span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
    .menu { display: none; position: fixed; top: 60px; right: 0; bottom: 0; width: 320px; background: var(--bg1); border-left: 1px solid rgba(243,234,216,.1); padding: 1rem; overflow-y: auto; z-index: 99; }
    .menu.open { display: block; }
    .menu h2 { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(243,234,216,.5); margin: 0 0 1rem; }
    .report-item { padding: 0.75rem 1rem; background: var(--bg0); border-radius: 8px; margin-bottom: 0.5rem; cursor: pointer; transition: 0.2s; }
    .report-item:hover { background: rgba(196,92,62,.2); }
    .report-item.active { border: 1px solid var(--accent); }
    .report-item .title { font-weight: 600; font-size: 0.9rem; }
    .report-item .meta { font-size: 0.75rem; color: rgba(243,234,216,.6); margin-top: 0.25rem; }
    .main { padding: 80px 2rem 2rem; max-width: 600px; margin: 0 auto; }
    .upload { padding: 2rem; background: var(--bg1); border-radius: 14px; border: 1px solid rgba(243,234,216,.08); }
    .upload h2 { font-family: 'Fraunces', serif; font-size: 1.5rem; margin: 0 0 1rem; }
    .upload input[type="file"] { display: block; margin: 1rem 0; width: 100%; }
    .upload button { background: var(--accent); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-size: 1rem; width: 100%; }
    .upload button:hover { opacity: 0.9; }
    .success { padding: 1.5rem; background: rgba(45,106,143,.2); border: 1px solid var(--accent2); border-radius: 8px; margin-bottom: 1.5rem; }
    .success a { color: #7eb8d8; }
  </style>
</head>
<body>
  <nav class="nav">
    <h1>Atlas · Rosario</h1>
    <div class="hamburger" onclick="document.querySelector('.menu').classList.toggle('open')">
      <span></span><span></span><span></span>
    </div>
  </nav>
  <div class="menu">
    <h2>Reportes guardados</h2>
    <div id="reportList"></div>
  </div>
  <div class="main">
    __SUCCESS__
    <div class="upload">
      <h2>Subir nuevos datos</h2>
      <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".json">
        <button type="submit">Generar Reporte</button>
      </form>
    </div>
  </div>
  <script>
    const reports = __REPORTS_JSON__;
    const currentId = new URLSearchParams(window.location.search).get('report');
    document.getElementById('reportList').innerHTML = reports.map(r => {
      const meta = r.meta || {};
      const city = meta.ciudad || 'Rosario';
      const analytics = meta.analytics || {};
      const g = analytics.global || {};
      const total = g.n || '—';
      const date = new Date(r.modified * 1000).toLocaleDateString('es-AR', {day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'});
      return `<div class="report-item${r.id === currentId ? ' active' : ''}" onclick="window.location.href='/?report=${r.id}'">
        <div class="title">${city}</div>
        <div class="meta">${total} avisos · ${date}</div>
      </div>`;
    }).join('') || '<p style="color:rgba(243,234,216,.5)">No hay reportes</p>';
  </script>
</body>
</html>"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

