"""Write the PNG from an `orca screenshot --json` result.

usage: python3 -I png.py <orca-json> <out.png>
"""
import base64, json, struct, sys

data = json.load(open(sys.argv[1]))
if not data.get("ok"):
    sys.exit("orca error: %s" % data.get("error"))
raw = base64.b64decode(data["result"]["data"])
w, h = struct.unpack(">II", raw[16:24])
open(sys.argv[2], "wb").write(raw)
print(sys.argv[2], w, "x", h, len(raw), "bytes")
