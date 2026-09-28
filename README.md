# FCM API Reference

Scriptable reference for the **FCM / SecOps Content Manager** REST API (`Content Manager API v1.1.0`) — **194 endpoints across 26 groups** (rules, reference lists, data tables, feeds, parsers, extensions, dashboards, exclusions, curated rules, instances, publisher, adoption, tags, users/roles, auth, maintenance…).

| File | Purpose |
|---|---|
| [`API_REFERENCE.md`](API_REFERENCE.md) | Every endpoint grouped by area, with query params and request-body fields |
| [`spec/openapi.json`](spec/openapi.json) | Raw OpenAPI 3 spec, as served by the FCM server at `/apis/docs-json` |
| [`scripts/fcm_api.sh`](scripts/fcm_api.sh) | Bash wrapper: signs in, caches the token, calls any endpoint |
| [`scripts/gen_doc.py`](scripts/gen_doc.py) | Regenerates `API_REFERENCE.md` from a (re-downloaded) spec |
| [`.env.example`](.env.example) | Template for your connection settings |

## Quick start

```bash
cp .env.example .env        # fill in your real values (.env is git-ignored)
set -a; source .env; set +a

./scripts/fcm_api.sh GET /instances
./scripts/fcm_api.sh GET "/rules?page=0&size=20"
./scripts/fcm_api.sh token  # print a fresh bearer token
```

Requires `curl` and `jq`.

## Authentication in one line

```bash
curl -s -X POST http://$FCM_HOST/apis/v1/auth/signin -H 'Content-Type: application/json' \
  -d "{\"email\":\"$FCM_EMAIL\",\"password\":\"$FCM_PASSWORD\"}"
# -> {"accessToken":"<JWT, 30 min>","refreshToken":"<JWT>"}
```

Send `Authorization: Bearer <accessToken>` on every other call. Renew with
`POST /apis/v1/auth/refresh` and body `{"refreshToken":"..."}`.

## Refreshing the docs

```bash
curl -s http://$FCM_HOST/apis/docs-json -o spec/openapi.json
python3 scripts/gen_doc.py      # rewrites API_REFERENCE.md
```

> **Caution:** many endpoints are destructive (`DELETE`, `maintenance/*`, `publisher/archive`, `publisher/{instanceID}/deployed-*` deletes) and act directly on connected Chronicle/SecOps instances. Test against a non-production instance first.

## Security

No real hosts, accounts, passwords or tokens are stored in this repo — all values are placeholders (`<FCM_HOST>`, `<FCM_EMAIL>`, `<FCM_PASSWORD>`). Keep real values in `.env` or your secret manager.
