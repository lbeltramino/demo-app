# demo-app

Node.js HTTP server deployed via IDP using the `k8s-deployment` compute resource spec.

## What it does

Serves a simple HTML page showing all environment variables injected by the IDP from linked services (e.g. `MY_BUCKET_PREFIX` from the S3 bucket link).

- `GET /` — HTML page with injected parameters
- `GET /health` — `{"status":"ok"}`
- `GET /env` — JSON dump of injected env vars

## IDP setup

- App slug: `demo-app`
- Compute resource: `api-worker` (k8s-deployment spec)
- Linked service: `my-bucket` (s3-bucket) via `s3-rw-access` link

## GitHub Actions secrets/variables required

| Name | Type | Value |
|------|------|-------|
| `IDP_API_KEY` | Secret | IDP org API key |
| `IDP_HOST` | Variable | `https://idp-local.stoutcode.com` |
| `K8S_SPEC_ID` | Variable | UUID of the k8s-deployment CR spec |
