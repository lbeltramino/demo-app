const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 80;

// Collect IDP-injected env vars (those set from parameter values)
const injectedEnv = Object.entries(process.env)
  .filter(([k]) => k !== 'PATH' && k !== 'NODE_ENV' && k !== 'PORT' && k === k.toUpperCase())
  .reduce((acc, [k, v]) => ({ ...acc, [k]: v }), {});

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
    return;
  }

  if (req.url === '/env') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(injectedEnv, null, 2));
    return;
  }

  const html = fs.readFileSync(path.join(__dirname, '../public/index.html'), 'utf8')
    .replace('__ENV_JSON__', JSON.stringify(injectedEnv, null, 2));

  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(html);
});

server.listen(PORT, () => {
  console.log(`demo-app listening on :${PORT}`);
  console.log('Injected parameters:', Object.keys(injectedEnv).join(', ') || '(none)');
});
