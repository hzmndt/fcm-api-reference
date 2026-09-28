#!/usr/bin/env bash
# fcm_api.sh - tiny CLI wrapper for the FCM (Content Manager) REST API.
#
# Usage:
#   source .env            # or export FCM_HOST / FCM_EMAIL / FCM_PASSWORD
#   ./scripts/fcm_api.sh GET  /instances
#   ./scripts/fcm_api.sh GET  "/rules?page=0&size=20"
#   ./scripts/fcm_api.sh POST /rules-validation/validations '{"content":"rule x { ... }"}'
#   ./scripts/fcm_api.sh token          # print a fresh access token
#
# The access token is cached in $FCM_TOKEN_CACHE (default: ~/.cache/fcm_token)
# and refreshed automatically when it is older than ~25 minutes.
set -euo pipefail

: "${FCM_HOST:?Set FCM_HOST (e.g. export FCM_HOST=fcm.example.com)}"
: "${FCM_EMAIL:?Set FCM_EMAIL}"
: "${FCM_PASSWORD:?Set FCM_PASSWORD}"
FCM_SCHEME="${FCM_SCHEME:-http}"
BASE="${FCM_SCHEME}://${FCM_HOST}/apis/v1"
CACHE="${FCM_TOKEN_CACHE:-$HOME/.cache/fcm_token}"
MAX_AGE=1500 # seconds (tokens expire after 30 min)

command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

get_token() {
  if [[ -f "$CACHE" ]] && (( $(date +%s) - $(stat -c %Y "$CACHE" 2>/dev/null || stat -f %m "$CACHE") < MAX_AGE )); then
    cat "$CACHE"; return
  fi
  local body token
  body=$(jq -n --arg e "$FCM_EMAIL" --arg p "$FCM_PASSWORD" '{email:$e,password:$p}')
  token=$(curl -sf -X POST "$BASE/auth/signin" -H 'Content-Type: application/json' -d "$body" | jq -r .accessToken)
  [[ -n "$token" && "$token" != "null" ]] || { echo "Sign-in failed" >&2; exit 1; }
  mkdir -p "$(dirname "$CACHE")"; umask 077; printf '%s' "$token" > "$CACHE"
  printf '%s' "$token"
}

[[ $# -ge 1 ]] || { sed -n '2,12p' "$0"; exit 1; }

if [[ "$1" == "token" ]]; then get_token; echo; exit 0; fi

METHOD="${1^^}"; PATH_Q="${2:?path required, e.g. /instances}"; DATA="${3:-}"
ARGS=(-s -X "$METHOD" "$BASE$PATH_Q" -H "Authorization: Bearer $(get_token)" -H 'Accept: application/json')
[[ -n "$DATA" ]] && ARGS+=(-H 'Content-Type: application/json' -d "$DATA")

curl "${ARGS[@]}" | (jq . 2>/dev/null || cat)
