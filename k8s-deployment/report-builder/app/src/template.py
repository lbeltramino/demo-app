TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Atlas Rosario — Informe Argenprop</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;1,9..144,400&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg0: #0f1419;
      --bg1: #1a222d;
      --paper: #f3ead8;
      --accent: #c45c3e;
      --accent2: #2d6a8f;
    }
    html, body { margin: 0; font-family: 'Outfit', system-ui, sans-serif; background: var(--bg0); color: var(--paper); }
    .nav { position: fixed; top: 0; left: 0; right: 0; height: 60px; background: var(--bg1); border-bottom: 1px solid rgba(243,234,216,.08); display: flex; align-items: center; padding: 0 1.5rem; z-index: 100; }
    .nav h1 { font-family: 'Fraunces', serif; font-size: 1.25rem; margin: 0; }
    .nav a { color: var(--paper); text-decoration: none; }
    .hamburger { margin-left: auto; cursor: pointer; padding: 0.5rem; display: flex; flex-direction: column; gap: 5px; }
    .hamburger span { width: 24px; height: 2px; background: var(--paper); }
    .menu { display: none; position: fixed; top: 60px; right: 0; bottom: 0; width: 300px; background: var(--bg1); border-left: 1px solid rgba(243,234,216,.1); padding: 1rem; overflow-y: auto; z-index: 99; }
    .menu.open { display: block; }
    .menu h2 { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(243,234,216,.5); margin: 0 0 0.75rem; }
    .report-item { padding: 0.5rem 0.75rem; background: var(--bg0); border-radius: 6px; margin-bottom: 0.4rem; cursor: pointer; font-size: 0.85rem; }
    .report-item:hover { background: rgba(196,92,62,.2); }
    .report-item.active { border: 1px solid var(--accent); }
    .main { padding: 80px 1.5rem 2rem; }

header.hero {
  padding: 2.5rem 0 2rem;
  border-bottom: 1px solid rgba(243,234,216,.08);
}
.hero h1 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 3.2rem);
  font-weight: 700;
  margin: 0 0 .5rem;
  letter-spacing: -0.02em;
  background: linear-gradient(120deg, var(--paper) 0%, #d4c4a8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero .lede {
  font-size: 1.1rem;
  color: rgba(243,234,216,.72);
  max-width: 62ch;
  font-weight: 300;
}
.hero .badge {
  display: inline-block;
  margin-top: 1rem;
  padding: .35rem .85rem;
  border-radius: 999px;
  background: rgba(196,92,62,.15);
  color: #e8a090;
  font-size: .8rem;
  font-weight: 600;
  letter-spacing: .04em;
  text-transform: uppercase;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.stat {
  background: var(--bg1);
  border: 1px solid rgba(243,234,216,.06);
  border-radius: var(--radius);
  padding: 1rem 1.15rem;
  animation: rise .6s ease backwards;
}
.stat:nth-child(1){ animation-delay: .05s; }
.stat:nth-child(2){ animation-delay: .1s; }
.stat:nth-child(3){ animation-delay: .15s; }
.stat:nth-child(4){ animation-delay: .2s; }
.stat:nth-child(5){ animation-delay: .25s; }
.stat:nth-child(6){ animation-delay: .3s; }
@keyframes rise {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: none; }
}
.stat .v { font-size: 1.45rem; font-weight: 700; color: var(--paper); font-variant-numeric: tabular-nums; }
.stat .l { font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: rgba(243,234,216,.45); margin-top: .25rem; }

.panel {
  background: var(--bg1);
  border-radius: var(--radius);
  border: 1px solid rgba(243,234,216,.07);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
}
.panel h2 {
  font-family: var(--font-display);
  font-size: 1.35rem;
  margin: 0 0 1rem;
  color: var(--paper);
}

.filters {
  display: flex; flex-wrap: wrap; gap: .75rem 1rem;
  align-items: flex-end;
}
.filters label { font-size: .75rem; color: rgba(243,234,216,.5); display: block; margin-bottom: .25rem; }
.filters input[type="text"], .filters input[type="number"], .filters select {
  background: var(--bg0);
  border: 1px solid rgba(243,234,216,.12);
  color: var(--paper);
  padding: .5rem .75rem;
  border-radius: 10px;
  font-family: inherit;
  min-width: 120px;
}
.filters input:focus, .filters select:focus {
  outline: none; border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--glow);
}
.chip-row { display: flex; flex-wrap: wrap; gap: .5rem; }
.chip {
  border: 1px solid rgba(243,234,216,.15);
  background: transparent;
  color: var(--paper);
  padding: .4rem .9rem;
  border-radius: 999px;
  cursor: pointer;
  font-size: .85rem;
  transition: background .2s, border-color .2s;
}
.chip:hover { background: rgba(243,234,216,.06); }
.chip.on { background: rgba(196,92,62,.25); border-color: var(--accent); color: #fff; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}
.card {
  background: linear-gradient(165deg, var(--bg1) 0%, #141c24 100%);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid rgba(243,234,216,.06);
  transition: transform .2s, box-shadow .2s;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(0,0,0,.35);
}
.card .ph {
  position: relative;
  aspect-ratio: 4/3;
  background: #0a0e12;
  cursor: pointer;
}
.card .ph-badges {
  position: absolute;
  top: .5rem;
  right: .5rem;
  left: .5rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: .35rem;
  z-index: 2;
  pointer-events: none;
}
.card .badge-warn {
  font-size: .65rem;
  font-weight: 700;
  letter-spacing: .03em;
  text-transform: uppercase;
  padding: .28rem .5rem;
  border-radius: 6px;
  max-width: 100%;
  line-height: 1.2;
}
.card .badge-warn.piso {
  background: rgba(180, 120, 30, .92);
  color: #1a1208;
  border: 1px solid rgba(255, 220, 140, .45);
}
.card .badge-warn.cochera {
  background: rgba(95, 70, 140, .92);
  color: #f0e8ff;
  border: 1px solid rgba(200, 170, 255, .35);
}
.card .ph img {
  width: 100%; height: 100%; object-fit: cover;
  display: block;
}
.card .ph .nfo {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: .5rem .75rem;
  background: linear-gradient(transparent, rgba(0,0,0,.75));
  font-size: .75rem;
  display: flex; justify-content: space-between;
}
.card .body { padding: 1rem 1.1rem 1.15rem; }
.card .title { font-weight: 600; font-size: .95rem; margin: 0 0 .5rem; line-height: 1.35; color: var(--paper); }
.card .meta { font-size: .8rem; color: rgba(243,234,216,.55); font-variant-numeric: tabular-nums; }
.card .meta strong { color: #e8dcc8; }
.card .barrio { font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: var(--accent); margin-bottom: .35rem; }
.card .direccion {
  font-size: .92rem;
  font-weight: 600;
  color: #e8dcc8;
  line-height: 1.35;
  margin: 0 0 .5rem;
}
.card .loc {
  font-size: .78rem;
  color: rgba(243,234,216,.5);
  margin: -.25rem 0 .5rem;
}
.card a.ext {
  display: inline-block; margin-top: .65rem;
  font-size: .78rem; color: var(--accent2);
  text-decoration: none;
  font-weight: 600;
}
.card a.ext:hover { text-decoration: underline; }

.charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin: 2rem 0; }
.chart-box {
  background: var(--bg1);
  border-radius: var(--radius);
  border: 1px solid rgba(243,234,216,.06);
  padding: 1rem;
  height: 280px;
  position: relative;
}
.chart-box .chart-caption {
  font-size: .72rem;
  color: rgba(243,234,216,.42);
  margin: .35rem 0 0;
  line-height: 1.35;
}

.insight {
  font-size: .95rem;
  color: rgba(243,234,216,.78);
  line-height: 1.65;
}
.insight strong { color: var(--paper); }
.insight ul { margin: .5rem 0; padding-left: 1.2rem; }
.insight li { margin: .35rem 0; }

/* Modal */
.modal-overlay {
  display: none; position: fixed; inset: 0;
  background: rgba(10,12,15,.88);
  z-index: 100;
  padding: 1rem;
  overflow: auto;
  backdrop-filter: blur(6px);
}
.modal-overlay.open { display: flex; align-items: flex-start; justify-content: center; }
.modal {
  background: var(--bg1);
  border-radius: var(--radius);
  max-width: 960px; width: 100%;
  margin: 2rem auto;
  border: 1px solid rgba(243,234,216,.1);
  max-height: 92vh; overflow: auto;
}
.modal header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(243,234,216,.08);
  display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;
}
.modal header h3 { margin: 0; font-family: var(--font-display); font-size: 1.2rem; }
.modal .modal-head-text { flex: 1; min-width: 0; }
.modal .modal-ficha {
  display: inline-block;
  margin-top: .65rem;
  padding: .45rem .95rem;
  border-radius: 10px;
  background: rgba(45, 106, 143, .35);
  border: 1px solid rgba(126, 184, 216, .45);
  color: #b8dff5;
  font-size: .85rem;
  font-weight: 600;
  text-decoration: none;
  font-family: var(--font-body);
}
.modal .modal-ficha:hover {
  background: rgba(45, 106, 143, .55);
  color: #fff;
}
.modal .close {
  background: rgba(243,234,216,.08);
  border: none; color: var(--paper);
  width: 36px; height: 36px; border-radius: 10px;
  cursor: pointer; font-size: 1.2rem; line-height: 1;
}
.modal .close:hover { background: rgba(196,92,62,.3); }
.modal .gallery { padding: 0 1rem 1rem; }
.modal .empty { padding: 2rem; text-align: center; color: rgba(243,234,216,.45); }

.photo-viewer { user-select: none; -webkit-user-select: none; }
.photo-stage {
  display: flex;
  align-items: stretch;
  gap: 0;
  min-height: min(72vh, 640px);
  position: relative;
  touch-action: manipulation;
}
.photo-frame {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #070a0d;
  border-radius: 10px;
  overflow: hidden;
}
.photo-main-img {
  max-width: 100%;
  max-height: min(72vh, 640px);
  width: auto;
  height: auto;
  object-fit: contain;
  display: block;
}
.photo-btn {
  flex: 0 0 auto;
  width: 3rem;
  min-width: 44px;
  border: none;
  background: rgba(243,234,216,.08);
  color: var(--paper);
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  border-radius: 10px;
  align-self: stretch;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background .2s;
}
.photo-btn:hover { background: rgba(196,92,62,.35); }
.photo-btn:disabled { opacity: .25; cursor: default; }
.photo-counter {
  text-align: center;
  font-size: .85rem;
  color: rgba(243,234,216,.55);
  margin: .65rem 0 .35rem;
  font-variant-numeric: tabular-nums;
}
.photo-toolbar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .65rem;
  margin-bottom: .45rem;
  flex-wrap: wrap;
}
.photo-fs-btn {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  padding: .45rem .95rem;
  border-radius: 999px;
  border: 1px solid rgba(126, 184, 216, .45);
  background: rgba(45, 106, 143, .28);
  color: #c5e8ff;
  font-size: .82rem;
  font-weight: 600;
  cursor: pointer;
  font-family: var(--font-body);
}
.photo-fs-btn:hover { background: rgba(45, 106, 143, .5); color: #fff; }
.photo-fs-ico { font-size: 1.1rem; line-height: 1; opacity: .95; }
.photo-toolbar-hint {
  font-size: .72rem;
  color: rgba(243,234,216,.38);
  max-width: 14rem;
  text-align: center;
  line-height: 1.35;
}
.photo-strip {
  display: flex;
  gap: .4rem;
  overflow-x: auto;
  overflow-y: hidden;
  padding: .25rem 0 .5rem;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x proximity;
}
.photo-thumb {
  flex: 0 0 auto;
  width: 72px;
  height: 54px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: #0a0e12;
  scroll-snap-align: start;
}
.photo-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.photo-thumb.on {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px rgba(196,92,62,.5);
}
@media (max-width: 600px) {
  .photo-stage { min-height: min(68vh, 560px); }
  .photo-main-img { max-height: min(68vh, 560px); }
  .photo-btn { width: 2.5rem; font-size: 1.75rem; }
}

/* Vista ampliada (fullscreen / zoom) — encima del modal */
.photo-immersive {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: #030506;
  display: flex;
  flex-direction: column;
  touch-action: none;
}
.photo-immersive[hidden] { display: none !important; }
.photo-immersive-bar {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: .6rem 1rem;
  padding-top: max(.6rem, env(safe-area-inset-top));
  background: linear-gradient(180deg, rgba(0,0,0,.75), transparent);
  color: rgba(243,234,216,.85);
  font-size: .9rem;
  font-variant-numeric: tabular-nums;
}
.photo-immersive-exit {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 12px;
  background: rgba(243,234,216,.12);
  color: var(--paper);
  font-size: 1.35rem;
  line-height: 1;
  cursor: pointer;
}
.photo-immersive-exit:hover { background: rgba(196,92,62,.4); }
.photo-immersive-body {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: stretch;
  gap: 0;
}
.photo-immersive-viewport {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  touch-action: none;
}
.photo-zoom-inner {
  transform-origin: center center;
  will-change: transform;
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 100%;
  max-height: 100%;
}
.photo-immersive-viewport .photo-zoom-inner img {
  max-width: 100vw;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  display: block;
  -webkit-user-drag: none;
}
.photo-immersive-nav {
  flex: 0 0 3rem;
  min-width: 44px;
  border: none;
  background: rgba(243,234,216,.06);
  color: var(--paper);
  font-size: 2rem;
  cursor: pointer;
  align-self: stretch;
}
.photo-immersive-nav:hover { background: rgba(196,92,62,.25); }
.photo-immersive-nav:disabled { opacity: .2; cursor: default; }
.photo-immersive-foot {
  flex: 0 0 auto;
  text-align: center;
  font-size: .72rem;
  color: rgba(243,234,216,.4);
  padding: .4rem 1rem max(.6rem, env(safe-area-inset-bottom));
  margin: 0;
}
@media (min-width: 601px) {
  .photo-toolbar-hint { display: none; }
}

footer {
  margin-top: 3rem; padding-top: 1.5rem;
  border-top: 1px solid rgba(243,234,216,.08);
  font-size: .78rem; color: rgba(243,234,216,.4);
  text-align: center;
}

@media (max-width: 600px) {
  .filters { flex-direction: column; align-items: stretch; }
}
  </style>
</head>
<body>
  <nav class="nav">
    <h1><a href="/">Atlas · Rosario</a></h1>
    <div class="hamburger" onclick="document.querySelector('.menu').classList.toggle('open')">
      <span></span><span></span><span></span>
    </div>
  </nav>
  <div class="menu" id="reportMenu">
    <h2>Reportes</h2>
    <div id="reportList"></div>
    <p style="margin-top:1rem"><a href="/" style="color:var(--accent2)">← Subir nuevo reporte</a></p>
  </div>
  <div class="wrap">
    <header class="hero">
      <h1>Atlas inmobiliario · Rosario</h1>
      <p class="lede">
        Un tablero viviente sobre tu búsqueda filtrada en Argenprop: departamentos con perfil de crédito,
        dos o tres dormitorios, cochera, baños en cantidad, balcón y frente — ahora con <em>galerías en vivo</em> desde el CDN del portal (sin espejar archivos).
      </p>
      <span class="badge" id="metaBadge">Cargando…</span>
    </header>

    <section class="stats" id="statsRow"></section>

    <section class="panel">
      <h2>Filtros</h2>
      <div class="filters">
        <div>
          <label>Dormitorios</label>
          <div class="chip-row" id="dormChips">
            <button type="button" class="chip on" data-dorm="all">Todos</button>
            <button type="button" class="chip" data-dorm="2">2 dorm</button>
            <button type="button" class="chip" data-dorm="3">3 dorm</button>
          </div>
        </div>
        <div>
          <label>Precio USD mín</label>
          <input type="number" id="pMin" placeholder="90000" />
        </div>
        <div>
          <label>Precio USD máx</label>
          <input type="number" id="pMax" placeholder="200000" />
        </div>
        <div>
          <label>m² cub. mín</label>
          <input type="number" id="mMin" placeholder="66" />
        </div>
        <div>
          <label>Buscar texto</label>
          <input type="text" id="q" placeholder="calle, barrio, título…" style="min-width:200px" />
        </div>
        <div>
          <label>&nbsp;</label>
          <label style="display:flex;align-items:center;gap:.4rem;cursor:pointer">
            <input type="checkbox" id="onlyExp" /> Solo con mención expensas
          </label>
        </div>
      </div>
      <p style="margin:1rem 0 0;font-size:.85rem;color:rgba(243,234,216,.45)" id="countLabel"></p>
    </section>

    <section class="charts">
      <div class="chart-box">
        <canvas id="chartPm2"></canvas>
        <p class="chart-caption">Clic en una barra para filtrar avisos en ese rango USD/m². Clic de nuevo en la misma barra quita el filtro.</p>
      </div>
      <div class="chart-box">
        <canvas id="chartScatter"></canvas>
        <p class="chart-caption">Clic en un punto para ver solo esa propiedad. Clic otra vez en el mismo punto quita el filtro.</p>
      </div>
    </section>

    <section class="panel">
      <h2>Lectura rápida</h2>
      <div class="insight" id="insights"></div>
    </section>

    <section class="grid" id="cardGrid"></section>

    <footer>
      Datos de listado + fotos vía API pública Argenprop. Imágenes hotlinked para uso personal; derechos de autor de las fotos pertenecen a anunciantes/Argenprop.
      <br />Generado localmente — abrí este HTML desde disco; todo corre en el navegador.
    </footer>
  </div>

  <div class="modal-overlay" id="modal" role="dialog" aria-modal="true">
    <div class="modal">
      <header>
        <div class="modal-head-text">
          <h3 id="modalTitle">—</h3>
          <a class="modal-ficha" id="modalFicha" href="#" target="_blank" rel="noopener">Abrir ficha en Argenprop →</a>
        </div>
        <button type="button" class="close" id="modalClose" aria-label="Cerrar">×</button>
      </header>
      <div class="gallery" id="modalGallery"></div>
    </div>
    <div class="photo-immersive" id="photoImmersive" hidden>
      <div class="photo-immersive-bar">
        <span id="photoImmersiveCount">—</span>
        <button type="button" class="photo-immersive-exit" id="photoImmersiveExit" aria-label="Cerrar vista ampliada">×</button>
      </div>
      <div class="photo-immersive-body">
        <button type="button" class="photo-immersive-nav prev" id="photoImmPrev" aria-label="Foto anterior">‹</button>
        <div class="photo-immersive-viewport" id="photoImmersiveViewport">
          <div class="photo-zoom-inner" id="photoZoomInner">
            <img id="photoImmersiveImg" alt="" draggable="false" referrerpolicy="no-referrer-when-downgrade" decoding="async" />
          </div>
        </div>
        <button type="button" class="photo-immersive-nav next" id="photoImmNext" aria-label="Foto siguiente">›</button>
      </div>
      <p class="photo-immersive-foot">Pellizco para zoom · doble toque (o doble clic) para ampliar · flechas para otras fotos</p>
    </div>
  </div>

  <script>
const RAW = __DATA_JSON__;
</script>
<script>
fetch('/api/reports').then(r=>r.json()).then(reports=>{
  const list = document.getElementById('reportList');
  if(list) list.innerHTML = reports.map(r=>{
    const m=r.meta||{}, a=m.analytics||{}, g=a.global||{};
    return '<div class="report-item'+(r.id===window.__CURRENT_REPORT__?' active':'')+'" onclick="window.location.href=\'/?report='+r.id+'\'">'+(m.ciudad||'Reporte')+' · '+(g.n||'—')+' avisos</div>';
  }).join('')||'<p style="color:rgba(243,234,216,.5);font-size:0.8rem">No hay reportes</p>';
});
</script>
  <script>
const RAW = __DATA_JSON__;
const REPORT_ID = window.location.search.match(/report=([a-f0-9]+)/);
window.__CURRENT_REPORT__ = REPORT_ID ? REPORT_ID[1] : null;
  </script>
  <script>
(function () {
  const data = RAW;
  const meta = data.meta || {};
  const a2 = data.dormitorios_2.avisos.map((a) => ({ ...a, segment: "2", segmentLabel: "2 dorm" }));
  const a3 = data.dormitorios_3.avisos.map((a) => ({ ...a, segment: "3", segmentLabel: "3 dorm" }));
  const all = [...a2, ...a3];

  document.getElementById("metaBadge").textContent =
    meta.ciudad + " · USD " + meta.precio_desde?.toLocaleString() + "–" + meta.precio_hasta?.toLocaleString() + " · " + all.length + " avisos";

  const an = data.analytics || {};
  const g = an.global || {};
  const statsRow = document.getElementById("statsRow");
  const fmtUsd = (n) => (n == null ? "—" : "USD " + Math.round(n).toLocaleString());
  const fmtNum = (n) => (n == null ? "—" : n.toLocaleString(undefined, { maximumFractionDigits: 0 }));
  statsRow.innerHTML = [
    ["Avisos total", String(g.n ?? all.length)],
    ["Mediana USD", fmtUsd(g.precio_median)],
    ["Mediana USD/m²", g.usd_m2_median == null ? "—" : fmtUsd(g.usd_m2_median) + "/m²"],
    ["Rango USD/m²", g.usd_m2_min != null ? fmtUsd(g.usd_m2_min) + " – " + fmtUsd(g.usd_m2_max) + "/m²" : "—"],
    ["Mediana m² cub.", fmtNum(g.m2_median) + " m²"],
    ["Mencionan expensas", (g.pct_expensas ?? 0) + "%"],
  ]
    .map(
      ([l, v]) =>
        `<div class="stat"><div class="v">${v}</div><div class="l">${l}</div></div>`
    )
    .join("");

  // Charts (bins + scatter meta shared with filters)
  const bins = 12;
  const priced = all.filter((a) => a.price_usd_numeric && a.superficie_cubierta_m2);
  const pm2Vals = priced.map((a) => a.price_usd_numeric / a.superficie_cubierta_m2);
  const minP = pm2Vals.length ? Math.min(...pm2Vals) : 0;
  const maxP = pm2Vals.length ? Math.max(...pm2Vals) : 1;
  const w = (maxP - minP) / bins || 1;
  const binLists = Array.from({ length: bins }, () => []);
  priced.forEach((a) => {
    const v = a.price_usd_numeric / a.superficie_cubierta_m2;
    let i = Math.floor((v - minP) / w);
    if (i >= bins) i = bins - 1;
    if (i < 0) i = 0;
    binLists[i].push(a);
  });
  const hist = binLists.map((list) => list.length);
  const labels = hist.map((_, i) => {
    const a = minP + i * w;
    const b = minP + (i + 1) * w;
    return Math.round(a) + "-" + Math.round(b);
  });

  let chartSelection = null;
  let chartPm2Instance;
  let chartScatterInstance;

  const sc = all.filter((a) => a.price_usd_numeric && a.superficie_cubierta_m2);
  const sc2 = sc.filter((a) => a.segment === "2");
  const sc3 = sc.filter((a) => a.segment === "3");
  const scatterIds = [sc2.map((a) => a.id_aviso_argenprop), sc3.map((a) => a.id_aviso_argenprop)];

  function barBackgrounds() {
    return hist.map((_, i) =>
      chartSelection && chartSelection.kind === "pm2bin" && chartSelection.binIndex === i
        ? "rgba(255,180,140,.95)"
        : "rgba(196,92,62,.65)"
    );
  }

  const ctx1 = document.getElementById("chartPm2");
  chartPm2Instance = new Chart(ctx1, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Cantidad",
          data: hist,
          backgroundColor: barBackgrounds(),
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      onHover: (e, el) => {
        e.native.target.style.cursor = el.length ? "pointer" : "default";
      },
      onClick: (e, elements) => {
        if (!elements.length) return;
        const idx = elements[0].index;
        if (chartSelection && chartSelection.kind === "pm2bin" && chartSelection.binIndex === idx) {
          chartSelection = null;
        } else {
          chartSelection = { kind: "pm2bin", binIndex: idx };
        }
        render();
        syncChartHighlight();
      },
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Distribución USD/m² (cub.)", color: "#e8dcc8" },
        tooltip: {
          callbacks: {
            afterLabel: (ctx) => {
              const n = binLists[ctx.dataIndex]?.length ?? 0;
              return n ? n + " aviso(s) — clic para filtrar" : "Clic para filtrar";
            },
          },
        },
      },
      scales: {
        x: { ticks: { color: "#8a8075", maxRotation: 45, minRotation: 45, font: { size: 9 } }, grid: { color: "rgba(243,234,216,.06)" } },
        y: { ticks: { color: "#8a8075" }, grid: { color: "rgba(243,234,216,.06)" } },
      },
    },
  });

  const ctx2 = document.getElementById("chartScatter");
  chartScatterInstance = new Chart(ctx2, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "2 dorm",
          data: sc2.map((a) => ({ x: a.superficie_cubierta_m2, y: a.price_usd_numeric })),
          backgroundColor: "rgba(45,106,143,.7)",
        },
        {
          label: "3 dorm",
          data: sc3.map((a) => ({ x: a.superficie_cubierta_m2, y: a.price_usd_numeric })),
          backgroundColor: "rgba(196,92,62,.75)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      onHover: (e, el) => {
        e.native.target.style.cursor = el.length ? "pointer" : "default";
      },
      onClick: (e, elements) => {
        if (!elements.length) return;
        const el = elements[0];
        const id = scatterIds[el.datasetIndex][el.index];
        if (chartSelection && chartSelection.kind === "scatter" && chartSelection.id === id) {
          chartSelection = null;
        } else {
          chartSelection = { kind: "scatter", id };
        }
        render();
        syncChartHighlight();
      },
      plugins: {
        title: { display: true, text: "Precio vs m² cubiertos", color: "#e8dcc8" },
        legend: { labels: { color: "#c4b8a8" } },
        tooltip: {
          callbacks: {
            afterLabel: (ctx) => {
              const id = scatterIds[ctx.datasetIndex][ctx.dataIndex];
              return "ID " + id + " — clic para filtrar";
            },
          },
        },
      },
      scales: {
        x: { title: { display: true, text: "m² cub.", color: "#8a8075" }, ticks: { color: "#8a8075" }, grid: { color: "rgba(243,234,216,.06)" } },
        y: { title: { display: true, text: "USD", color: "#8a8075" }, ticks: { color: "#8a8075" }, grid: { color: "rgba(243,234,216,.06)" } },
      },
      elements: {
        point: {
          radius: (ctx) => {
            const id = scatterIds[ctx.datasetIndex][ctx.dataIndex];
            const on = chartSelection && chartSelection.kind === "scatter" && chartSelection.id === id;
            return on ? 11 : 5;
          },
          hoverRadius: 8,
        },
      },
    },
  });

  function syncChartHighlight() {
    if (chartPm2Instance) {
      chartPm2Instance.data.datasets[0].backgroundColor = barBackgrounds();
      chartPm2Instance.update("none");
    }
    if (chartScatterInstance) chartScatterInstance.update("none");
  }

  // Insights
  const byPm2 = [...all]
    .map((a) => ({
      a,
      r: a.price_usd_numeric && a.superficie_cubierta_m2 ? a.price_usd_numeric / a.superficie_cubierta_m2 : Infinity,
    }))
    .filter((x) => isFinite(x.r))
    .sort((x, y) => x.r - y.r);
  const best = byPm2.slice(0, 3);
  const worst = byPm2.slice(-3).reverse();
  document.getElementById("insights").innerHTML = `
    <p><strong>Contexto mercado (esta muestra):</strong> la mediana global ronda <strong>${fmtUsd(g.usd_m2_median)}/m²</strong> —
    útil para comparar contra el <em>resto del mercado rosarino</em> solo como orden de magnitud: acá ya entraron filtros duros (crédito, cochera, 2+ baños, balcón, frente), así que <strong>no</strong> es el índice Zonaprop crudo.</p>
    <ul>
      <li><strong>Mejor relación USD/m²</strong> (top 3 de esta lista): ${best.map((x) => `<a href="${x.a.url}" target="_blank" rel="noopener" style="color:#7eb8d8">${x.a.title_card?.slice(0,42) || "aviso"}…</a> (${fmtUsd(x.r)}/m²)`).join(" · ")}</li>
      <li><strong>Precio por m² más alto</strong> en el lote: ${worst.map((x) => `<span style="color:#e8a090">${x.a.title_card?.slice(0,36)}…</span> (${fmtUsd(x.r)}/m²)`).join(" · ")} — suele ser vista río, amenities o m² escasos.</li>
      <li><strong>Recomendación:</strong> cruzá siempre <em>expensas</em> y <em>tasación banco</em>; el filtro “apto crédito” del portal no reemplaza la aprobación hipotecaria.</li>
    </ul>
  `;

  let dormFilter = "all";
  const pMinEl = document.getElementById("pMin");
  const pMaxEl = document.getElementById("pMax");
  const mMinEl = document.getElementById("mMin");
  const qEl = document.getElementById("q");
  const onlyExp = document.getElementById("onlyExp");

  pMinEl.placeholder = String(meta.precio_desde || "");
  pMaxEl.placeholder = String(meta.precio_hasta || "");
  mMinEl.placeholder = String(meta.filtros?.superficie_cubierta_desde_m2 || "");

  document.querySelectorAll("#dormChips .chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#dormChips .chip").forEach((b) => b.classList.remove("on"));
      btn.classList.add("on");
      dormFilter = btn.dataset.dorm;
      if (dormFilter === "all") chartSelection = null;
      render();
      syncChartHighlight();
    });
  });

  [pMinEl, pMaxEl, mMinEl, qEl, onlyExp].forEach((el) => el.addEventListener("input", render));
  onlyExp.addEventListener("change", render);

  function matches(a) {
    if (chartSelection) {
      if (chartSelection.kind === "pm2bin") {
        if (!a.price_usd_numeric || !a.superficie_cubierta_m2) return false;
        const v = a.price_usd_numeric / a.superficie_cubierta_m2;
        let i = Math.floor((v - minP) / w);
        if (i >= bins) i = bins - 1;
        if (i < 0) i = 0;
        if (i !== chartSelection.binIndex) return false;
      } else if (chartSelection.kind === "scatter") {
        if (a.id_aviso_argenprop !== chartSelection.id) return false;
      }
    }
    if (dormFilter !== "all" && a.segment !== dormFilter) return false;
    const pmin = parseFloat(pMinEl.value);
    const pmax = parseFloat(pMaxEl.value);
    const mmin = parseFloat(mMinEl.value);
    if (!isNaN(pmin) && a.price_usd_numeric < pmin) return false;
    if (!isNaN(pmax) && a.price_usd_numeric > pmax) return false;
    if (!isNaN(mmin) && (a.superficie_cubierta_m2 || 0) < mmin) return false;
    if (onlyExp.checked && !a.has_expensas_mention) return false;
    const q = qEl.value.trim().toLowerCase();
    if (q) {
      const blob = (
        (a.title_card || "") +
        (a.raw_card_text || "") +
        (a.barrio_slug || "") +
        (a.direccion_calle || "") +
        (a.barrio_api || "") +
        (a.localidad_api || "")
      ).toLowerCase();
      if (!blob.includes(q)) return false;
    }
    return true;
  }

  function calleDisplay(a) {
    const d = (a.direccion_calle || "").trim();
    if (d) return d;
    const g = (a.address_guess || "").trim();
    if (g && g.length > 5 && !/ver más/i.test(g)) return g;
    return "";
  }

  function normTxt(s) {
    return String(s || "").toLowerCase();
  }

  function detectFloorEdge(a) {
    const raw = [a.raw_card_text, a.title_card, a.titulo_api].filter(Boolean).join(" ");
    const t = normTxt(raw);
    const ultimo =
      /último piso|ultimo piso/.test(t) ||
      /piso último|piso ultimo/.test(t) ||
      /ult\.?\s*piso/.test(t) ||
      /en el último piso|en el ultimo piso/.test(t);
    let pb = false;
    if (/(departamento|depto|unidad|vivienda|semi-?piso)[^.\n]{0,130}planta baja/i.test(raw)) pb = true;
    else if (/en planta baja[,.\s]+(con )?(living|dormitor|amplio|excelente|ventilacion|balcon)/i.test(raw))
      pb = true;
    else if (
      /planta baja[^.\n]{0,70}(living|dormitor|ventilacion|balcon|frente|contrafrente|ambient|mono|depto|departamento)/i.test(
        raw
      )
    )
      pb = true;
    else if (/en planta baja/i.test(raw) && !/cochera[^.\n]{0,45}en planta baja/i.test(raw)) pb = true;
    return { pb, ultimo };
  }

  function floorEdgeBadgeText(o) {
    if (o.pb && o.ultimo) return "Planta baja · último piso (revisar)";
    if (o.pb) return "Planta baja";
    if (o.ultimo) return "Último piso";
    return "";
  }

  function detectCocheraOpcional(a) {
    const raw = [a.raw_card_text, a.title_card, a.titulo_api].filter(Boolean).join(" ");
    const t = normTxt(raw);
    return (
      /cochera opcional/.test(t) ||
      /cocheras opcionales/.test(t) ||
      /estacionamiento opcional/.test(t) ||
      /opcional[^.]{0,55}cochera/.test(t) ||
      /cochera[^.]{0,40}opcional/.test(t) ||
      /\+\s*cochera opcional/.test(t) ||
      /box(es)? opcionales/i.test(raw)
    );
  }

  function render() {
    const list = all.filter(matches);
    let extra = "";
    if (chartSelection) {
      if (chartSelection.kind === "pm2bin") {
        const i = chartSelection.binIndex;
        const lo = Math.round(minP + i * w);
        const hi = Math.round(minP + (i + 1) * w);
        extra = " · Gráfico: USD/m² " + lo + "–" + hi + " (" + (binLists[i]?.length ?? 0) + " en barra)";
      } else if (chartSelection.kind === "scatter") {
        extra = " · Gráfico: 1 propiedad seleccionada";
      }
    }
    document.getElementById("countLabel").textContent =
      "Mostrando " + list.length + " de " + all.length + " avisos" + extra;
    const grid = document.getElementById("cardGrid");
    grid.innerHTML = list
      .map((a) => {
        const pm =
          a.price_usd_numeric && a.superficie_cubierta_m2
            ? Math.round(a.price_usd_numeric / a.superficie_cubierta_m2)
            : null;
        const thumb = (a.fotos && a.fotos[0] && (a.fotos[0].medium || a.fotos[0].full)) || "";
        const nf = (a.fotos && a.fotos.length) || 0;
        const calle = calleDisplay(a);
        const zone =
          [a.barrio_api, a.localidad_api].filter(Boolean).join(" · ") ||
          (a.barrio_slug || "rosario").replace(/-/g, " ");
        const imgTag = thumb
          ? `<img src="${thumb}" alt="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" />`
          : `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#555;font-size:.85rem">Sin foto en API</div>`;
        const fe = detectFloorEdge(a);
        const cochOp = detectCocheraOpcional(a);
        const floorLabel = floorEdgeBadgeText(fe);
        const badgeParts = [];
        if (floorLabel)
          badgeParts.push(
            `<span class="badge-warn piso" title="Detectado en el texto del aviso (revisá la ficha).">${floorLabel}</span>`
          );
        if (cochOp)
          badgeParts.push(
            `<span class="badge-warn cochera" title="Mención a cochera opcional / no incluida.">Cochera opcional</span>`
          );
        const badgeRow = badgeParts.length ? `<div class="ph-badges">${badgeParts.join("")}</div>` : "";
        return `
      <article class="card" data-id="${a.id_aviso_argenprop}">
        <div class="ph" data-open="${a.id_aviso_argenprop}">
          ${badgeRow}
          ${imgTag}
          <div class="nfo"><span>${nf} foto(s)</span><span>${a.segmentLabel}</span></div>
        </div>
        <div class="body">
          <div class="direccion">${calle ? escapeHtml(calle) : '<span style="color:rgba(243,234,216,.38)">Dirección no disponible</span>'}</div>
          <div class="barrio">${escapeHtml(zone)}</div>
          <h3 class="title">${escapeHtml(a.title_card || "Sin título")}</h3>
          <div class="meta">
            <strong>${a.price_usd_numeric != null ? "USD " + a.price_usd_numeric.toLocaleString() : "—"}</strong>
            · ${a.superficie_cubierta_m2 != null ? a.superficie_cubierta_m2 + " m² cub." : "—"}
            ${pm != null ? " · <strong>" + pm.toLocaleString() + " USD/m²</strong>" : ""}
            ${a.has_expensas_mention ? " · expensas (texto)" : ""}
          </div>
          <a class="ext" href="${a.url}" target="_blank" rel="noopener">Ver en Argenprop →</a>
        </div>
      </article>`;
      })
      .join("");

    grid.querySelectorAll(".ph").forEach((el) => {
      el.addEventListener("click", () => openModal(parseInt(el.dataset.open, 10)));
    });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  const byId = Object.fromEntries(all.map((a) => [a.id_aviso_argenprop, a]));

  function escAttr(s) {
    return String(s || "").replace(/&/g, "&amp;").replace(/"/g, "&quot;");
  }

  let photoViewerNav = null;

  function closePhotoImmersive() {
    const imm = document.getElementById("photoImmersive");
    if (!imm || imm.hidden) return;
    imm.hidden = true;
    imm.setAttribute("aria-hidden", "true");
    if (window.__photoZoomReset) window.__photoZoomReset();
    if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
  }

  function openPhotoImmersive() {
    const imm = document.getElementById("photoImmersive");
    const img = document.getElementById("photoImmersiveImg");
    const main = document.getElementById("photoMain");
    const ctr = document.getElementById("photoCounter");
    if (!imm || !img || !main) return;
    img.src = main.currentSrc || main.src;
    const c = document.getElementById("photoImmersiveCount");
    if (c && ctr) c.textContent = ctr.textContent;
    if (window.__photoZoomReset) window.__photoZoomReset();
    const parts = (ctr && ctr.textContent && ctr.textContent.split("/")) || [];
    const total = parts.length > 1 ? parseInt(parts[1].trim(), 10) : 1;
    const many = total > 1;
    const ip = document.getElementById("photoImmPrev"),
      inx = document.getElementById("photoImmNext");
    if (ip) ip.hidden = !many;
    if (inx) inx.hidden = !many;
    imm.hidden = false;
    imm.setAttribute("aria-hidden", "false");
    const req = imm.requestFullscreen || imm.webkitRequestFullscreen;
    if (req) req.call(imm).catch(function () {});
  }

  function setupImmersiveZoom() {
    const viewport = document.getElementById("photoImmersiveViewport");
    const inner = document.getElementById("photoZoomInner");
    if (!viewport || !inner) return;
    let scale = 1,
      tx = 0,
      ty = 0;
    let pinchDist0 = null,
      pinchScale0 = 1;
    let pan0 = null;
    function apply() {
      inner.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + scale + ")";
    }
    function reset() {
      scale = 1;
      tx = 0;
      ty = 0;
      apply();
    }
    window.__photoZoomReset = reset;

    function dist(a, b) {
      const dx = a.clientX - b.clientX,
        dy = a.clientY - b.clientY;
      return Math.sqrt(dx * dx + dy * dy);
    }

    viewport.addEventListener(
      "touchstart",
      function (e) {
        if (e.touches.length === 2) {
          pinchDist0 = dist(e.touches[0], e.touches[1]);
          pinchScale0 = scale;
        } else if (e.touches.length === 1 && scale > 1) {
          pan0 = { x: e.touches[0].clientX - tx, y: e.touches[0].clientY - ty };
        }
      },
      { passive: false }
    );

    viewport.addEventListener(
      "touchmove",
      function (e) {
        if (e.touches.length === 2 && pinchDist0) {
          e.preventDefault();
          let ns = pinchScale0 * (dist(e.touches[0], e.touches[1]) / pinchDist0);
          if (ns < 1) ns = 1;
          if (ns > 5) ns = 5;
          scale = ns;
          apply();
        } else if (e.touches.length === 1 && scale > 1 && pan0) {
          e.preventDefault();
          tx = e.touches[0].clientX - pan0.x;
          ty = e.touches[0].clientY - pan0.y;
          apply();
        }
      },
      { passive: false }
    );

    viewport.addEventListener("touchend", function (e) {
      if (e.touches.length < 2) pinchDist0 = null;
      if (e.touches.length === 0) pan0 = null;
    });

    let lastTap = 0,
      lastTapX = 0,
      lastTapY = 0;
    viewport.addEventListener(
      "touchend",
      function (e) {
        if (e.changedTouches.length !== 1) return;
        const now = Date.now(),
          x = e.changedTouches[0].clientX,
          y = e.changedTouches[0].clientY;
        if (now - lastTap < 300 && Math.abs(x - lastTapX) < 35 && Math.abs(y - lastTapY) < 35) {
          if (scale > 1) reset();
          else {
            scale = 2.5;
            tx = 0;
            ty = 0;
            apply();
          }
        }
        lastTap = now;
        lastTapX = x;
        lastTapY = y;
      },
      { passive: true }
    );

    viewport.addEventListener("dblclick", function (e) {
      e.preventDefault();
      if (scale > 1) reset();
      else {
        scale = 2.5;
        tx = 0;
        ty = 0;
        apply();
      }
    });
  }

  function closeModal() {
    closePhotoImmersive();
    document.getElementById("modal").classList.remove("open");
    document.body.style.overflow = "";
    photoViewerNav = null;
  }

  function initPhotoViewer(root, fotosList) {
    const imgEl = root.querySelector("#photoMain");
    const counter = root.querySelector("#photoCounter");
    const prevBtn = root.querySelector(".photo-prev");
    const nextBtn = root.querySelector(".photo-next");
    const stage = root.querySelector("#photoStage");
    const strip = root.querySelector("#photoStrip");
    let idx = 0;
    function syncImmersiveIfOpen() {
      const imm = document.getElementById("photoImmersive");
      if (!imm || imm.hidden) return;
      const f = fotosList[idx];
      const im = document.getElementById("photoImmersiveImg");
      if (im && f) im.src = f.full || f.medium || "";
      const ic = document.getElementById("photoImmersiveCount");
      if (ic) ic.textContent = idx + 1 + " / " + fotosList.length;
      const ip = document.getElementById("photoImmPrev"),
        inx = document.getElementById("photoImmNext");
      const many = fotosList.length > 1;
      if (ip) ip.hidden = !many;
      if (inx) inx.hidden = !many;
      if (window.__photoZoomReset) window.__photoZoomReset();
    }
    function renderAt(i) {
      idx = ((i % fotosList.length) + fotosList.length) % fotosList.length;
      const f = fotosList[idx];
      imgEl.src = f.full || f.medium || "";
      counter.textContent = idx + 1 + " / " + fotosList.length;
      const many = fotosList.length > 1;
      prevBtn.hidden = !many;
      nextBtn.hidden = !many;
      strip.querySelectorAll(".photo-thumb").forEach((btn, j) => btn.classList.toggle("on", j === idx));
      const active = strip.querySelector(".photo-thumb.on");
      if (active && active.scrollIntoView) active.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
      syncImmersiveIfOpen();
    }
    function next() {
      renderAt(idx + 1);
    }
    function prev() {
      renderAt(idx - 1);
    }
    prevBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      prev();
    });
    nextBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      next();
    });
    strip.addEventListener("click", (e) => {
      const b = e.target.closest(".photo-thumb");
      if (!b) return;
      e.stopPropagation();
      renderAt(parseInt(b.dataset.i, 10));
    });
    let tx0 = null;
    stage.addEventListener(
      "touchstart",
      (e) => {
        if (e.changedTouches.length === 1) tx0 = e.changedTouches[0].clientX;
      },
      { passive: true }
    );
    stage.addEventListener(
      "touchend",
      (e) => {
        if (tx0 == null || !e.changedTouches.length) return;
        const dx = e.changedTouches[0].clientX - tx0;
        tx0 = null;
        if (fotosList.length < 2 || Math.abs(dx) < 50) return;
        if (dx > 0) prev();
        else next();
      },
      { passive: true }
    );
    imgEl.addEventListener("click", (e) => {
      e.stopPropagation();
      const r = e.currentTarget.getBoundingClientRect();
      const mx = e.clientX - r.left;
      if (fotosList.length < 2) return;
      if (mx < r.width * 0.35) prev();
      else if (mx > r.width * 0.65) next();
    });
    const fsBtn = root.querySelector("#photoFsBtn");
    if (fsBtn)
      fsBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        openPhotoImmersive();
      });
    photoViewerNav = { next, prev };
    renderAt(0);
    setTimeout(() => stage.focus(), 50);
  }

  document.addEventListener("keydown", (ev) => {
    const imm = document.getElementById("photoImmersive");
    if (imm && !imm.hidden && ev.key === "Escape") {
      closePhotoImmersive();
      ev.preventDefault();
      return;
    }
    if (!photoViewerNav || !document.getElementById("modal").classList.contains("open")) return;
    if (ev.key === "ArrowLeft") {
      photoViewerNav.prev();
      ev.preventDefault();
    } else if (ev.key === "ArrowRight") {
      photoViewerNav.next();
      ev.preventDefault();
    }
  });

  setupImmersiveZoom();
  (function wireImmersiveChrome() {
    const x = document.getElementById("photoImmersiveExit");
    if (x) x.addEventListener("click", (e) => { e.stopPropagation(); closePhotoImmersive(); });
    const p = document.getElementById("photoImmPrev");
    if (p) p.addEventListener("click", (e) => { e.stopPropagation(); if (photoViewerNav) photoViewerNav.prev(); });
    const n = document.getElementById("photoImmNext");
    if (n) n.addEventListener("click", (e) => { e.stopPropagation(); if (photoViewerNav) photoViewerNav.next(); });
  })();

  function openModal(id) {
    const a = byId[id];
    if (!a) return;
    const calle = calleDisplay(a);
    document.getElementById("modalTitle").textContent = calle
      ? calle + " · " + (a.title_card || "Aviso " + id)
      : a.title_card || "Aviso " + id;
    const ficha = document.getElementById("modalFicha");
    ficha.href = a.url || "#";
    const gal = document.getElementById("modalGallery");
    const fotos = a.fotos || [];
    photoViewerNav = null;
    if (!fotos.length) {
      gal.innerHTML =
        '<div class="empty">Sin fotos en la respuesta API. <a href="' +
        escAttr(a.url) +
        '" target="_blank" rel="noopener" style="color:#7eb8d8">Abrir ficha</a></div>';
    } else {
      const thumbs = fotos
        .map(
          (f, i) =>
            `<button type="button" class="photo-thumb${i === 0 ? " on" : ""}" data-i="${i}" aria-label="Ir a foto ${i + 1}">` +
            `<img src="${escAttr(f.small || f.medium || f.full)}" alt="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" /></button>`
        )
        .join("");
      const first = fotos[0];
      gal.innerHTML =
        `<div class="photo-viewer">` +
        `<div class="photo-stage" id="photoStage" tabindex="-1">` +
        `<button type="button" class="photo-btn photo-prev" aria-label="Foto anterior">‹</button>` +
        `<div class="photo-frame">` +
        `<img id="photoMain" class="photo-main-img" src="${escAttr(first.full || first.medium)}" alt="Foto del aviso" referrerpolicy="no-referrer-when-downgrade" decoding="async" />` +
        `</div>` +
        `<button type="button" class="photo-btn photo-next" aria-label="Foto siguiente">›</button>` +
        `</div>` +
        `<p class="photo-counter" id="photoCounter">1 / ${fotos.length}</p>` +
        `<div class="photo-toolbar">` +
        `<button type="button" class="photo-fs-btn" id="photoFsBtn" title="Ver grande, zoom y casi pantalla completa">` +
        `<span class="photo-fs-ico" aria-hidden="true">⛶</span><span class="photo-fs-label">Ampliar / zoom</span></button>` +
        `<span class="photo-toolbar-hint">Aquí podés pellizcar y usar doble toque. También abrí la vista ampliada.</span>` +
        `</div>` +
        `<div class="photo-strip" id="photoStrip">${thumbs}</div>` +
        `</div>`;
      initPhotoViewer(gal, fotos);
    }
    document.getElementById("modal").classList.add("open");
    document.body.style.overflow = "hidden";
  }

  document.getElementById("modalClose").addEventListener("click", () => {
    closeModal();
  });
  document.getElementById("modal").addEventListener("click", (e) => {
    if (e.target.id === "modal") {
      const imm = document.getElementById("photoImmersive");
      if (imm && !imm.hidden) closePhotoImmersive();
      else closeModal();
    }
  });

  render();
})();
  </script>
</body>
</html>
"""
