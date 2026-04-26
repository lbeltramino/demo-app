#!/usr/bin/env python3
"""Report builder server - generates HTML reports from listing data."""
import json
import os
import ssl
import time
from pathlib import Path
from statistics import median
from datetime import datetime, timezone

from flask import Flask, request, send_file, jsonify, render_template_string

app = Flask(__name__)

API_BASE = os.environ.get("API_URL", "https://api.sosiva451.com/Avisos")
OUTPUT_JSON = os.environ.get("OUTPUT_JSON", "/data/output.json")
OUTPUT_HTML = os.environ.get("OUTPUT_HTML", "/data/output.html")
TEMPLATE_FILE = Path(__file__).parent / "template.py"

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    FULL_TEMPLATE = f.read()

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
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file provided", 400
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e}", 400
        
        data = build_report(data)
        
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        html_content = generate_html(data)
        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        total = len(data.get("dormitorios_2", {}).get("avisos", [])) + len(data.get("dormitorios_3", {}).get("avisos", []))
        return f"Report generated: {total} listings"
    
    if Path(OUTPUT_HTML).exists():
        return send_file(OUTPUT_HTML)
    
    return render_template_string(UPLOAD_HTML)

@app.route("/api/report")
def get_report():
    if not Path(OUTPUT_JSON).exists():
        return jsonify({"error": "No report generated yet"}), 404
    return send_file(OUTPUT_JSON, mimetype="application/json")

UPLOAD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Upload Report Data</title>
  <style>
    :root { --bg: #0f1419; --paper: #f3ead8; --accent: #c45c3e; }
    body { margin: 0; font-family: system-ui, sans-serif; background: var(--bg); color: var(--paper); padding: 2rem; }
    h1 { font-size: 2rem; margin-bottom: 1rem; }
    .upload { margin-top: 2rem; padding: 2rem; background: #1a222d; border-radius: 14px; }
    input[type="file"] { margin: 1rem 0; }
    button { background: var(--accent); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-size: 1rem; }
    button:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <h1>Atlas - Upload Report Data</h1>
  <p>Upload a JSON file with Argenprop listings to generate a report.</p>
  <div class="upload">
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept=".json">
      <button type="submit">Generate Report</button>
    </form>
  </div>
</body>
</html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)