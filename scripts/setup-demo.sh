#!/usr/bin/env bash
# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
# Build an isolated preview from pinned public dependencies.
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
demo_root="$repo_root/temp/collaborator-demo"
if [ -e "$demo_root" ]; then
    echo "Already exists: $demo_root. Preserve it or move it aside before setting up again." >&2
    exit 1
fi
command -v git >/dev/null
command -v npm >/dev/null
python_bin="${PYTHON:-python3.12}"
"$python_bin" --version
node --version
mkdir -p "$demo_root/client"
"$python_bin" -m venv "$demo_root/venv"
"$demo_root/venv/bin/python" -m pip install -r "$repo_root/requirements-demo.txt"
"$demo_root/venv/bin/python" -m pip install --no-deps -e "$repo_root"
git clone --branch codex/python-js-alignment https://github.com/genropy/genro-dom-js.git "$demo_root/client/genro-dom-js"
git -C "$demo_root/client/genro-dom-js" checkout --detach d888cefbb4dfb65868148afb2e00cabe84b4de08
npm ci --prefix "$demo_root/client/genro-dom-js" --ignore-scripts --no-audit --no-fund
ln -s "$demo_root/client/genro-dom-js/node_modules" "$demo_root/client/node_modules"
ln -s "$demo_root/client/node_modules/genro-bag-js" "$demo_root/client/genro-bag-js"
ln -s "$demo_root/client/node_modules/genro-tytx" "$demo_root/client/genro-tytx"
ln -s "$demo_root/client/node_modules" "$demo_root/client/genro-tytx/js/node_modules"
echo "Ready. From the genro-pages checkout:"
echo "  source temp/collaborator-demo/venv/bin/activate"
echo '  export GENRO_CLIENT_MODULES="$PWD/temp/collaborator-demo/client"'
echo '  genropages --modules "$GENRO_CLIENT_MODULES" --port 8014'
echo "Manual: genropages manual"
