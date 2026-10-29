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

    async def read(self) -> dict[str, Any]:
        response = await self._request([{"op": 2, "to": INDOOR}, {"op": 2, "to": OUTDOOR}])
        values: dict[str, str] = {}

        def walk(node: Any, path: str) -> None:
            if not isinstance(node, dict):
                return
            p = f"{path}/{node['pn']}" if "pn" in node else path
            if "pv" in node and not isinstance(node["pv"], (dict, list)):
                values[p] = node["pv"]
            for key in ("pch", "pc"):
                x = node.get(key)
                for child in x if isinstance(x, list) else [x] if isinstance(x, dict) else []:
                    walk(child, p)

        for part in response.get("responses", []):
            walk(part.get("pc", {}), "")
        if not values:
            raise DaikinError("Empty response")
        return {
            "power": values.get("/dgc_status/e_1002/e_A002/p_01") == "01",
            "p05": values.get("/dgc_status/e_1002/e_3001/p_05"),
            "p06": values.get("/dgc_status/e_1002/e_3001/p_06"),
            "ceiling": values.get("/dgc_status/e_1002/e_3003/p_1D") == "01",
            "mold_proof": values.get("/dgc_status/e_1002/e_3003/p_4D") == "01",
            "streamer": values.get("/dgc_status/e_1002/e_3003/p_20") == "01",
            "powerful": values.get("/dgc_status/e_1003/e_3002/p_44") == "01",
        }

    async def write(self, groups: dict[str, dict[str, str]]) -> None:
        """groups: {"e_3001": {"p_05": "01000000"}, ...} on the indoor unit (e_1002)."""
        pch = [
            {"pn": g, "pch": [{"pn": p, "pv": v} for p, v in values.items()]}
            for g, values in groups.items()
        ]
        response = await self._request(
            [{"op": 3, "to": INDOOR, "pc": {"pn": "dgc_status", "pch": [{"pn": "e_1002", "pch": pch}]}}]
        )
        rsc = (response.get("responses") or [{}])[0].get("rsc")
        if rsc != 2004:
            raise DaikinError(f"Unit rejected {groups} (rsc {rsc})")
