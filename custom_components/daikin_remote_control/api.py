"""Reading and writing via POST /dsiot/multireq."""

from __future__ import annotations

from typing import Any

import aiohttp

from .const import INDOOR, OUTDOOR


class DaikinError(Exception):
    """Unit unreachable or command rejected."""


class DaikinDsiot:
    def __init__(self, session: aiohttp.ClientSession, host: str) -> None:
        self._session = session
        self._url = f"http://{host}/dsiot/multireq"

    async def _request(self, requests: list[dict]) -> dict:
        try:
            async with self._session.post(
                self._url, json={"requests": requests}, timeout=aiohttp.ClientTimeout(total=8)
            ) as response:
                response.raise_for_status()
                return await response.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError, ValueError) as err:
            raise DaikinError(str(err)) from err

    async def read(self) -> dict[str, str]:
        """Return all values keyed by their path below dgc_status, e.g. "e_1002/e_3001/p_05"."""
        response = await self._request([{"op": 2, "to": INDOOR}, {"op": 2, "to": OUTDOOR}])
        values: dict[str, str] = {}

        def walk(node: Any, path: str) -> None:
            if not isinstance(node, dict):
                return
            p = f"{path}/{node['pn']}" if path else node.get("pn", "")
            if "pv" in node and not isinstance(node["pv"], (dict, list)):
                values[p.removeprefix("dgc_status/")] = node["pv"]
            for key in ("pch", "pc"):
                x = node.get(key)
                for child in x if isinstance(x, list) else [x] if isinstance(x, dict) else []:
                    walk(child, p)

        for part in response.get("responses", []):
            walk(part.get("pc", {}), "")
        if not values:
            raise DaikinError("Empty response")
        return values

    async def write(self, changes: dict[str, str]) -> None:
        """changes: {"e_1002/e_3001/p_05": "01000000", ...}; only indoor (e_1002) points are writable."""
        tree: dict = {}
        for path, value in changes.items():
            node = tree
            for part in path.split("/")[:-1]:
                node = node.setdefault(part, {})
            node[path.split("/")[-1]] = value

        def build(node: dict) -> list[dict]:
            return [
                {"pn": k, "pch": build(v)} if isinstance(v, dict) else {"pn": k, "pv": v}
                for k, v in node.items()
            ]

        response = await self._request(
            [{"op": 3, "to": INDOOR, "pc": {"pn": "dgc_status", "pch": build(tree)}}]
        )
        rsc = (response.get("responses") or [{}])[0].get("rsc")
        if rsc != 2004:
            raise DaikinError(f"Unit rejected {changes} (rsc {rsc})")
