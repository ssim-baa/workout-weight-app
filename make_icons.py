# Generates the home-screen icons (stdlib only). Run: D:\Python313\python.exe -s make_icons.py
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))


def png(size, path):
    bg = (0, 0, 0)
    fg = (48, 209, 88)  # --work green
    # Simple dumbbell: centre bar + two plates
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            u, v = x / size, y / size
            bar = 0.25 <= u <= 0.75 and 0.46 <= v <= 0.54
            plate = (0.16 <= u <= 0.28 or 0.72 <= u <= 0.84) and 0.30 <= v <= 0.70
            row += bytes(fg if (bar or plate) else bg)
        rows.append(bytes(row))
    raw = zlib.compress(b"".join(rows), 9)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", raw) + chunk(b"IEND", b"")
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(out)
    os.replace(tmp, path)


for s in (180, 192, 512):
    png(s, os.path.join(HERE, f"icon-{s}.png"))
print("ok")
