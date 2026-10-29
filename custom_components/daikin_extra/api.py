"""Lesen und Schreiben über POST /dsiot/multireq."""

from __future__ import annotations

from typing import Any

import aiohttp

from .const import AUSSEN, INNEN


class DaikinFehler(Exception):
    """Anlage nicht erreichbar oder Befehl abgelehnt."""


class DaikinDsiot:
    def __init__(self, sitzung: aiohttp.ClientSession, host: str) -> None:
        self._sitzung = sitzung
        self._url = f"http://{host}/dsiot/multireq"

    async def _anfrage(self, anfragen: list[dict]) -> dict:
        try:
            async with self._sitzung.post(
                self._url, json={"requests": anfragen}, timeout=aiohttp.ClientTimeout(total=8)
            ) as antwort:
                antwort.raise_for_status()
                return await antwort.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError, ValueError) as err:
            raise DaikinFehler(str(err)) from err

    async def lesen(self) -> dict[str, Any]:
        antwort = await self._anfrage([{"op": 2, "to": INNEN}, {"op": 2, "to": AUSSEN}])
        werte: dict[str, str] = {}

        def gehe(n: Any, pfad: str) -> None:
            if not isinstance(n, dict):
                return
            p = f"{pfad}/{n['pn']}" if "pn" in n else pfad
            if "pv" in n and not isinstance(n["pv"], (dict, list)):
                werte[p] = n["pv"]
            for k in ("pch", "pc"):
                x = n.get(k)
                for kind in x if isinstance(x, list) else [x] if isinstance(x, dict) else []:
                    gehe(kind, p)

        for teil in antwort.get("responses", []):
            gehe(teil.get("pc", {}), "")
        if not werte:
            raise DaikinFehler("Leere Antwort")
        return {
            "an": werte.get("/dgc_status/e_1002/e_A002/p_01") == "01",
            "p05": werte.get("/dgc_status/e_1002/e_3001/p_05"),
            "p06": werte.get("/dgc_status/e_1002/e_3001/p_06"),
            "decke": werte.get("/dgc_status/e_1002/e_3003/p_1D") == "01",
            "schimmel": werte.get("/dgc_status/e_1002/e_3003/p_4D") == "01",
            "streamer": werte.get("/dgc_status/e_1002/e_3003/p_20") == "01",
            "powerful": werte.get("/dgc_status/e_1003/e_3002/p_44") == "01",
        }

    async def schreiben(self, gruppen: dict[str, dict[str, str]]) -> None:
        """gruppen: {"e_3001": {"p_05": "01000000"}, ...} am Innengerät (e_1002)."""
        pch = [
            {"pn": g, "pch": [{"pn": p, "pv": v} for p, v in werte.items()]}
            for g, werte in gruppen.items()
        ]
        antwort = await self._anfrage(
            [{"op": 3, "to": INNEN, "pc": {"pn": "dgc_status", "pch": [{"pn": "e_1002", "pch": pch}]}}]
        )
        rsc = (antwort.get("responses") or [{}])[0].get("rsc")
        if rsc != 2004:
            raise DaikinFehler(f"Anlage hat {gruppen} abgelehnt (rsc {rsc})")
