const express = require('express');
const busboy = require('busboy');
const path = require('path');
const {
  S3Client,
  ListObjectsV2Command,
  PutObjectCommand,
  DeleteObjectCommand,
  GetObjectCommand,
} = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');

// ── Config from IDP-injected env vars ──────────────────────────────────────
// Env var names follow the pattern: {SERVICE_SLUG}_{OUTPUT_NAME}
// where service slug is the slug of the minio-bucket service instance.
// We discover them by looking for *_ENDPOINT, *_BUCKET, *_ACCESS_KEY, *_SECRET_KEY
// or fall back to explicit MINIO_* vars for local dev.
function findEnvByPattern(suffix) {
  for (const [k, v] of Object.entries(process.env)) {
    if (k.endsWith(`_${suffix}`) && v) return v;
  }
  return null;
}

const ENDPOINT   = process.env.MINIO_ENDPOINT   || findEnvByPattern('ENDPOINT');
const BUCKET     = process.env.MINIO_BUCKET      || findEnvByPattern('BUCKET');
const ACCESS_KEY = process.env.MINIO_ACCESS_KEY  || findEnvByPattern('ACCESS_KEY');
const SECRET_KEY = process.env.MINIO_SECRET_KEY  || findEnvByPattern('SECRET_KEY');
const PORT       = parseInt(process.env.PORT || '80', 10);

if (!ENDPOINT || !BUCKET || !ACCESS_KEY || !SECRET_KEY) {
  console.error('Missing required env vars. Need: *_ENDPOINT, *_BUCKET, *_ACCESS_KEY, *_SECRET_KEY');
  process.exit(1);
}

const s3 = new S3Client({
  endpoint: ENDPOINT,
  region: 'us-east-1',
  credentials: { accessKeyId: ACCESS_KEY, secretAccessKey: SECRET_KEY },
  forcePathStyle: true,
});

const app = express();
app.use(express.static(path.join(__dirname, '../public')));

// ── Health ──────────────────────────────────────────────────────────────────
app.get('/health', (_req, res) => res.json({ status: 'ok' }));

// ── List photos ─────────────────────────────────────────────────────────────
app.get('/api/photos', async (_req, res) => {
  try {
    const result = await s3.send(new ListObjectsV2Command({ Bucket: BUCKET }));
    const objects = result.Contents || [];
    const photos = await Promise.all(
      objects
        .filter(o => /\.(jpg|jpeg|png|gif|webp)$/i.test(o.Key))
        .sort((a, b) => b.LastModified - a.LastModified)
        .map(o => ({
          key: o.Key,
          size: o.Size,
          lastModified: o.LastModified,
        }))
    );
    res.json(photos);
  } catch (err) {
    console.error('List error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// ── Proxy photo ─────────────────────────────────────────────────────────────
app.get('/api/photos/:key(*)', async (req, res) => {
  try {
    const { Body, ContentType } = await s3.send(new GetObjectCommand({
      Bucket: BUCKET,
      Key: req.params.key,
    }));
    res.set('Content-Type', ContentType || 'image/jpeg');
    res.set('Cache-Control', 'public, max-age=3600');
    if (Body instanceof Uint8Array) {
      res.send(Buffer.from(Body));
    } else {
      Body.pipe(res);
    }
  } catch (err) {
    console.error('Get error:', err.message);
    res.status(404).send('Not found');
  }
});

// ── Upload photo ─────────────────────────────────────────────────────────────
app.post('/api/photos', (req, res) => {
  const bb = busboy({ headers: req.headers, limits: { fileSize: 20 * 1024 * 1024 } });
  let uploaded = false;
  let responseSent = false;

  const sendResponse = (status, data) => {
    if (responseSent) return;
    responseSent = true;
    if (status >= 400) res.status(status).json(data);
    else res.json(data);
  };

  bb.on('file', (fieldname, stream, info) => {
    const { filename, mimeType } = info;
    if (!/^image\//i.test(mimeType)) {
      stream.resume();
      return sendResponse(400, { error: 'Only image files are allowed' });
    }
    const key = `${Date.now()}-${filename.replace(/[^a-zA-Z0-9._-]/g, '_')}`;
    const chunks = [];
    stream.on('data', chunk => chunks.push(chunk));
    stream.on('end', async () => {
      try {
        const body = Buffer.concat(chunks);
        await s3.send(new PutObjectCommand({
          Bucket: BUCKET,
          Key: key,
          Body: body,
          ContentType: mimeType,
        }));
        uploaded = true;
        sendResponse(200, { key, message: 'Uploaded successfully' });
      } catch (err) {
        console.error('Upload error:', err.message);
        sendResponse(500, { error: err.message });
      }
    });
  });

  bb.on('error', err => {
    console.error('Busboy error:', err.message);
    sendResponse(500, { error: err.message });
  });
  req.pipe(bb);
});

// ── Delete photo ─────────────────────────────────────────────────────────────
app.delete('/api/photos/:key(*)', async (req, res) => {
  try {
    await s3.send(new DeleteObjectCommand({ Bucket: BUCKET, Key: req.params.key }));
    res.json({ message: 'Deleted successfully' });
  } catch (err) {
    console.error('Delete error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Gallery listening on :${PORT}`);
  console.log(`MinIO endpoint: ${ENDPOINT}`);
  console.log(`Bucket: ${BUCKET}`);
});
