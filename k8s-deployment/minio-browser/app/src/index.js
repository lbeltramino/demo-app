const express = require('express');
const busboy = require('busboy');
const path = require('path');
const {
  S3Client,
  ListObjectsV2Command,
  GetObjectCommand,
  PutObjectCommand,
  DeleteObjectCommand,
} = require('@aws-sdk/client-s3');

const PORT = parseInt(process.env.PORT || '3000', 10);

// Discover all MinIO buckets from IDP-injected env vars.
// Pattern: {SERVICE_SLUG}_ENDPOINT, {SERVICE_SLUG}_BUCKET,
//          {SERVICE_SLUG}_ACCESS_KEY, {SERVICE_SLUG}_SECRET_KEY
function discoverBuckets() {
  const buckets = {};
  for (const [key, val] of Object.entries(process.env)) {
    const m = key.match(/^(.+)_ENDPOINT$/);
    if (!m || !val) continue;
    const prefix = m[1];
    const bucket    = process.env[`${prefix}_BUCKET`];
    const accessKey = process.env[`${prefix}_ACCESS_KEY`];
    const secretKey = process.env[`${prefix}_SECRET_KEY`];
    if (bucket && accessKey && secretKey) {
      buckets[prefix.toLowerCase()] = { endpoint: val, bucket, accessKey, secretKey };
    }
  }
  return buckets;
}

const BUCKETS = discoverBuckets();

if (!Object.keys(BUCKETS).length) {
  console.error('No MinIO buckets discovered. Need {PREFIX}_ENDPOINT/BUCKET/ACCESS_KEY/SECRET_KEY env vars.');
  process.exit(1);
}

console.log(`Discovered buckets: ${Object.keys(BUCKETS).join(', ')}`);

function clientFor(slug) {
  const cfg = BUCKETS[slug];
  if (!cfg) return null;
  return {
    s3: new S3Client({
      endpoint: cfg.endpoint,
      region: 'us-east-1',
      credentials: { accessKeyId: cfg.accessKey, secretAccessKey: cfg.secretKey },
      forcePathStyle: true,
    }),
    bucket: cfg.bucket,
  };
}

const app = express();
app.use(express.static(path.join(__dirname, '../public')));

app.get('/health', (_req, res) => res.json({ status: 'ok' }));

// List all configured buckets
app.get('/api/buckets', (_req, res) => {
  res.json(Object.entries(BUCKETS).map(([slug, cfg]) => ({
    slug,
    bucket: cfg.bucket,
    endpoint: cfg.endpoint,
  })));
});

// List objects in a bucket
app.get('/api/buckets/:slug/objects', async (req, res) => {
  const conn = clientFor(req.params.slug);
  if (!conn) return res.status(404).json({ error: 'Bucket not found' });
  try {
    const result = await conn.s3.send(new ListObjectsV2Command({ Bucket: conn.bucket }));
    const objects = (result.Contents || [])
      .sort((a, b) => b.LastModified - a.LastModified)
      .map(o => ({ key: o.Key, size: o.Size, lastModified: o.LastModified }));
    res.json(objects);
  } catch (err) {
    console.error('List error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// Download an object
app.get('/api/buckets/:slug/objects/*', async (req, res) => {
  const conn = clientFor(req.params.slug);
  if (!conn) return res.status(404).json({ error: 'Bucket not found' });
  const key = req.params[0];
  try {
    const { Body, ContentType, ContentLength } = await conn.s3.send(
      new GetObjectCommand({ Bucket: conn.bucket, Key: key })
    );
    res.set('Content-Type', ContentType || 'application/octet-stream');
    res.set('Content-Disposition', `attachment; filename="${path.basename(key)}"`);
    if (ContentLength) res.set('Content-Length', String(ContentLength));
    Body.pipe(res);
  } catch (err) {
    console.error('Download error:', err.message);
    res.status(404).json({ error: err.message });
  }
});

// Upload an object
app.post('/api/buckets/:slug/objects', (req, res) => {
  const conn = clientFor(req.params.slug);
  if (!conn) return res.status(404).json({ error: 'Bucket not found' });

  const bb = busboy({ headers: req.headers, limits: { fileSize: 100 * 1024 * 1024 } });
  let responseSent = false;

  const send = (status, data) => {
    if (responseSent) return;
    responseSent = true;
    res.status(status).json(data);
  };

  bb.on('file', (_field, stream, info) => {
    const key = `${Date.now()}-${info.filename.replace(/[^a-zA-Z0-9._-]/g, '_')}`;
    const chunks = [];
    stream.on('data', c => chunks.push(c));
    stream.on('end', async () => {
      try {
        const body = Buffer.concat(chunks);
        await conn.s3.send(new PutObjectCommand({
          Bucket: conn.bucket,
          Key: key,
          Body: body,
          ContentType: info.mimeType || 'application/octet-stream',
        }));
        send(200, { key, message: 'Uploaded successfully' });
      } catch (err) {
        console.error('Upload error:', err.message);
        send(500, { error: err.message });
      }
    });
  });

  bb.on('error', err => send(500, { error: err.message }));
  req.pipe(bb);
});

// Delete an object
app.delete('/api/buckets/:slug/objects/*', async (req, res) => {
  const conn = clientFor(req.params.slug);
  if (!conn) return res.status(404).json({ error: 'Bucket not found' });
  const key = req.params[0];
  try {
    await conn.s3.send(new DeleteObjectCommand({ Bucket: conn.bucket, Key: key }));
    res.json({ message: 'Deleted successfully' });
  } catch (err) {
    console.error('Delete error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`MinIO Browser listening on :${PORT}`);
});
