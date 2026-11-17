#!/usr/bin/env bash
# Copia site/ a $1 y antepone la subcarpeta $2 (ej. /zontes-chile) a las rutas absolutas.
set -euo pipefail
OUT="$1"; BASE="$2"
rm -rf "$OUT"; mkdir -p "$OUT"; cp -R site/. "$OUT"/
find "$OUT" -name '*.html' -print0 | xargs -0 perl -pi -e "s{(href|src)=\"/(?!/)}{\$1=\"$BASE/}g; s{<html lang=\"es\">}{<html lang=\"es\" data-base=\"$BASE\">}"
touch "$OUT/.nojekyll"
