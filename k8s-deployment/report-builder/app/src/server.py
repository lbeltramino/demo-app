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

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Atlas - Report</title>
  <style>
    :root { --bg: #0f1419; --paper: #f3ead8; --accent: #c45c3e; }
    body { margin: 0; font-family: system-ui, sans-serif; background: var(--bg); color: var(--paper); padding: 2rem; }
    h1 { font-size: 2rem; margin-bottom: 1rem; }
    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 2rem 0; }
    .stat { background: #1a222d; padding: 1rem; border-radius: 8px; }
    .stat .v { font-size: 1.5rem; font-weight: bold; }
    .stat .l { font-size: 0.75rem; text-transform: uppercase; opacity: 0.7; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
    .card { background: #1a222d; border-radius: 8px; overflow: hidden; }
    .card img { width: 100%; height: 200px; object-fit: cover; }
    .card .body { padding: 1rem; }
    .card .price { font-size: 1.2rem; font-weight: bold; }
    .card .meta { font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem; }
    .upload { margin-bottom: 2rem; padding: 1rem; background: #1a222d; border-radius: 8px; }
  </style>
</head>
<body>
  <h1>Atlas - Real Estate Report</h1>
  <div class="upload">
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept=".json">
      <button type="submit">Generate Report</button>
    </form>
  </div>
  {{ content | safe }}
</body>
</html>"""

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
        out.append({"full": m.get("Url"), "medium": m.get("Medium_U") or m.get("Medium")})
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
            item["titulo_api"] = payload.get("Title")
            item["barrio_api"] = payload.get("Barrio_t")
        except Exception as e:
            item["api_error"] = str(e)[:200]
        time.sleep(0.12)

def seg_stats(items):
    prices = [a.get("price_usd_numeric") for a in items if a.get("price_usd_numeric")]
    m2s = [a.get("superficie_cubierta_m2") for a in items if a.get("superficie_cubierta_m2")]
    return {"n": len(items), "precio_median": median(prices) if prices else None, "m2_median": median(m2s) if m2s else None}

def build_report(data):
    for key in ("dormitorios_2", "dormitorios_3"):
        if key in data:
            enrich_listings(data[key]["avisos"])
    data["meta"]["generated_at"] = datetime.now(timezone.utc).isoformat()
    a2 = data.get("dormitorios_2", {}).get("avisos", [])
    a3 = data.get("dormitorios_3", {}).get("avisos", [])
    data["analytics"] = {"dorm_2": seg_stats(a2), "dorm_3": seg_stats(a3), "global": seg_stats(a2 + a3)}
    return data

def generate_html(data):
    all_items = data.get("dormitorios_2", {}).get("avisos", []) + data.get("dormitorios_3", {}).get("avisos", [])
    g = data.get("analytics", {}).get("global", {})
    
    stats_html = f"""
    <div class="stats">
      <div class="stat"><div class="v">{g.get('n', len(all_items))}</div><div class="l">Total listings</div></div>
      <div class="stat"><div class="v">${int(g.get('precio_median') or 0):,}</div><div class="l">Median USD</div></div>
      <div class="stat"><div class="v">{int(g.get('m2_median') or 0):,} m²</div><div class="l">Median m²</div></div>
    </div>
    """
    
    grid_html = '<div class="grid">'
    for item in all_items[:50]:
        foto = (item.get("fotos") or [{}])[0].get("medium") or ""
        price = item.get("price_usd_numeric") or 0
        title = item.get("title_card") or "Sin título"
        m2 = item.get("superficie_cubierta_m2") or 0
        img_html = f'<img src="{foto}" alt="" loading="lazy"/>' if foto else '<div style="height:200px;display:flex;align-items:center;justify-content:center;">Sin foto</div>'
        grid_html += f'''
        <div class="card">
          {img_html}
          <div class="body">
            <div class="price">${price:,}</div>
            <div>{m2} m²</div>
            <div class="meta">{title}</div>
          </div>
        </div>'''
    grid_html += '</div>'
    
    return stats_html + grid_html

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
        
        with open(OUTPUT_JSON, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        html_content = generate_html(data)
        with open(OUTPUT_HTML, "w") as f:
            f.write(HTML_TEMPLATE.replace("{{ content | safe }}", html_content))
        
        return f"Report generated: {len(data.get('dormitorios_2',{}).get('avisos',[])) + len(data.get('dormitorios_3',{}).get('avisos',[]))} listings"
    
    if Path(OUTPUT_HTML).exists():
        return send_file(OUTPUT_HTML)
    
    return render_template_string(HTML_TEMPLATE.replace("{{ content | safe }}", "<p>Upload a JSON file to generate a report</p>"))

@app.route("/api/report")
def get_report():
    if not Path(OUTPUT_JSON).exists():
        return jsonify({"error": "No report generated yet"}), 404
    return send_file(OUTPUT_JSON, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)