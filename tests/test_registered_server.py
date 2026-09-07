"""Exercise the launched worker pool, HTTP cookie and registered page channels."""
import asyncio
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory

import httpx
import pytest
import websockets
from genro_tytx import to_tytx

from tests.test_registered_page import RegisteredPageChecks


@pytest.mark.asyncio
async def test_real_worker_registers_pages_before_their_channels_open():
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(str(Path(p).resolve()) for p in sys.path if p)
    with TemporaryDirectory(prefix="pages-", dir="/tmp") as state:
        with open(Path(state) / "server.log", "w+") as log:
            process = subprocess.Popen(
                [sys.executable, "-m", "genro_pages", "--modules", str(root.parent),
                 "--port", str(port), "--state-dir", state],
                cwd=root, env=env, stdout=log, stderr=log, start_new_session=True)
            try:
                async with httpx.AsyncClient(base_url=f"http://127.0.0.1:{port}") as client:
                    for attempt in range(100):
                        if process.poll() is not None:
                            log.seek(0)
                            pytest.fail(log.read())
                        try:
                            first = await client.get("/")
                            break
                        except httpx.ConnectError:
                            await asyncio.sleep(0.1)
                    else:
                        pytest.fail("Worker server did not start within ten seconds")
                    first.raise_for_status()
                    cid = client.cookies["spa_connection_id"]
                    assert len(cid) == 22
                    assert "HttpOnly" in first.headers["set-cookie"]
                    second = await client.get("/?page=widgets/textBox")
                    second.raise_for_status()
                    check = RegisteredPageChecks(None)
                    pages = [check.get_startup(r.text)["page_id"] for r in (first, second)]
                    assert pages[0] != pages[1]
                    assert client.cookies["spa_connection_id"] == cid
                    assert (await client.get("/?page=missing")).status_code == 404
                    async with websockets.connect(
                        f"ws://127.0.0.1:{port}/_wsx", origin=f"http://127.0.0.1:{port}",
                        additional_headers={"Cookie": f"spa_connection_id={cid}"},
                    ) as ws:
                        for index, page_id in enumerate(pages):
                            await ws.send("WSX://" + json.dumps(dict(
                                id=str(index), method="WSK", path="/_wsx/openchannel",
                                page_id=page_id, data=to_tytx({}, "json"))))
                            answer = json.loads((await asyncio.wait_for(ws.recv(), 5))[6:])
                            assert answer["status"] == 200, answer
                            assert answer["id"] == str(index)
            finally:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=5)
