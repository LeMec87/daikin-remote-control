---
name: Report another model
about: Tell us whether the integration works with your unit
---

**Indoor unit model:**
**Remote model:**
**Wi-Fi adapter / firmware** (if known):

**What works?**

**What does not work?**

If something is missing, a dump of the unit's data points helps a lot. Run this from any
computer in the same network (replace the IP address) and attach the output:

```bash
curl -s -X POST http://192.0.2.10/dsiot/multireq -H "Content-Type: application/json" \
  -d '{"requests":[{"op":2,"to":"/dsiot/edge/adr_0100.dgc_status?filter=pv,pt,md"},{"op":2,"to":"/dsiot/edge/adr_0200.dgc_status?filter=pv,pt,md"}]}'
```
