"""Render the Dura et al. (2025) subsidence polygons as web-mercator PNG tiles for the CPAL viewer.

Usage:
    python subsidence_to_tiles.py <folder with CascadiaPart*.gdb> <output folder> [--zmin 8] [--zmax 16] [--workers 4]

Writes <out>/<tileset>/<z>/<x>/<y>.png and <out>/<tileset>/index.json for these tilesets:
    floodplain_{2023,2100}           floodplain for that year (blue)
    added_{2023,2100}_{low,med,hi}   extra area flooded after earthquake subsidence (red)

index.json lists the tiles that exist so the viewer only requests real tiles.
Layers are read at full resolution and classified the same way as subsidence_to_geojson.py.
"""
import argparse
import json
import math
import os
import pickle
from multiprocessing import Pool

import numpy as np
import pyogrio
import shapely
from PIL import Image
from rasterio.features import rasterize
from rasterio.transform import from_bounds

from subsidence_to_geojson import INCREMENTAL, parse

ORIGIN = math.pi * 6378137.0
TILE = 256
SCALE = 2  # render at 2x and downsample for smooth edges
COLORS = {"floodplain": (59, 130, 246, 115), "added": (239, 68, 68, 190)}


def tile_bounds(z, x, y):
    size = 2 * ORIGIN / 2 ** z
    minx = -ORIGIN + x * size
    maxy = ORIGIN - y * size
    return minx, maxy - size, minx + size, maxy


def read_layers(src):
    """Return {(estuary, year, scenario, kind): [geometries in EPSG:3857]}."""
    layers = {}
    for name_gdb in sorted(os.listdir(src)):
        gdb = os.path.join(src, name_gdb)
        if not gdb.endswith(".gdb"):
            continue
        for name, _ in pyogrio.list_layers(gdb):
            key = parse(name)
            if key is None:
                continue
            g = pyogrio.read_dataframe(gdb, layer=name)
            if g.crs is not None and g.crs.is_compound:
                g = g.set_crs(g.crs.sub_crs_list[0], allow_override=True)
            geoms = shapely.make_valid(g.to_crs(3857).geometry.values)
            layers.setdefault(key, []).extend(geoms)
    return layers


def tilesets(layers):
    """Group layer geometries into the viewer tilesets."""
    out = {}
    for (est, year, scen, kind), geoms in layers.items():
        if kind == "floodplain" and scen == "base":
            out.setdefault(f"floodplain_{year}", []).extend(geoms)
            # Incremental estuaries store their 2100 floodplain as the change from 2023.
            if est in INCREMENTAL and year == "2023":
                out.setdefault("floodplain_2100", []).extend(geoms)
        elif kind == "added" and scen == "base" and est in INCREMENTAL and year == "2100":
            out.setdefault("floodplain_2100", []).extend(geoms)
        elif kind == "added" and scen != "base":
            out.setdefault(f"added_{year}_{scen}", []).extend(geoms)
    return out


def render(geoms, bounds, color):
    px = TILE * SCALE
    mask = rasterize(((g, 1) for g in geoms), out_shape=(px, px),
                     transform=from_bounds(*bounds, px, px), dtype="uint8")
    if not mask.any():
        return None
    alpha = Image.fromarray(mask * 255).reduce(SCALE)
    a = (np.asarray(alpha, dtype=np.float32) * (color[3] / 255.0)).astype(np.uint8)
    rgba = np.zeros((TILE, TILE, 4), dtype=np.uint8)
    rgba[..., :3] = color[:3]
    rgba[..., 3] = a
    return Image.fromarray(rgba, "RGBA")


def walk(z, x, y, geoms, zmin, zmax, color, out_dir, index):
    """Clip to this tile, write it if zmin <= z, then recurse into children."""
    b = tile_bounds(z, x, y)
    pad = (b[2] - b[0]) * 0.01
    clipped = [c for c in shapely.clip_by_rect(geoms, b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)
               if not c.is_empty]
    if not clipped:
        return
    if z >= zmin:
        img = render(clipped, b, color)
        if img is None:
            return
        path = os.path.join(out_dir, str(z), str(x))
        os.makedirs(path, exist_ok=True)
        img.save(os.path.join(path, f"{y}.png"), optimize=True)
        index.setdefault(str(z), []).append([x, y])
    if z < zmax:
        arr = np.array(clipped, dtype=object)
        for dx in (0, 1):
            for dy in (0, 1):
                walk(z + 1, 2 * x + dx, 2 * y + dy, arr, zmin, zmax, color, out_dir, index)


def build(args):
    name, prep_file, out, zmin, zmax = args
    color = COLORS["floodplain" if name.startswith("floodplain") else "added"]
    out_dir = os.path.join(out, name)
    with open(prep_file, "rb") as f:
        geoms = shapely.from_wkb(pickle.load(f))
    geoms = np.array([g for g in geoms if not g.is_empty], dtype=object)
    minx, miny, maxx, maxy = shapely.total_bounds(geoms)
    # Start from the tiles covering the data at a coarse zoom.
    z0 = min(zmin, 6)
    size = 2 * ORIGIN / 2 ** z0
    index = {}
    for x in range(math.floor((minx + ORIGIN) / size), math.floor((maxx + ORIGIN) / size) + 1):
        for y in range(math.floor((ORIGIN - maxy) / size), math.floor((ORIGIN - miny) / size) + 1):
            walk(z0, x, y, geoms, zmin, zmax, color, out_dir, index)
    lon = lambda mx: math.degrees(mx / 6378137.0)
    lat = lambda my: math.degrees(2 * math.atan(math.exp(my / 6378137.0)) - math.pi / 2)
    meta = {"minzoom": zmin, "maxzoom": zmax, "bounds": [lon(minx), lat(miny), lon(maxx), lat(maxy)],
            "tiles": index}
    with open(os.path.join(out_dir, "index.json"), "w") as f:
        json.dump(meta, f, separators=(",", ":"))
    n = sum(len(v) for v in index.values())
    print(f"{name}: {n} tiles", flush=True)
    return name, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--zmin", type=int, default=8)
    ap.add_argument("--zmax", type=int, default=16)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", nargs="*", help="limit to these tileset names")
    a = ap.parse_args()
    # Reading and cleaning the full-resolution layers is the slow part, so do it once and
    # save each tileset's geometries; workers then load only the tileset they render.
    prep = os.path.join(a.out, "_prep")
    if not os.path.isdir(prep):
        os.makedirs(prep)
        for name, geoms in tilesets(read_layers(a.src)).items():
            # 0.5 m is well under a pixel at zoom 16 and cuts the vertex count.
            geoms = shapely.simplify(np.array(geoms, dtype=object), 0.5, preserve_topology=True)
            with open(os.path.join(prep, f"{name}.pkl"), "wb") as f:
                pickle.dump(shapely.to_wkb(geoms), f)
            print("prepared", name, len(geoms), flush=True)
    names = sorted(f[:-4] for f in os.listdir(prep) if f.endswith(".pkl"))
    if a.only:
        names = [n for n in names if n in a.only]
    sizes = {n: os.path.getsize(os.path.join(prep, f"{n}.pkl")) for n in names}
    jobs = [(n, os.path.join(prep, f"{n}.pkl"), a.out, a.zmin, a.zmax) for n in sorted(names, key=lambda n: -sizes[n])]
    with Pool(a.workers) as pool:
        for name, n in pool.imap_unordered(build, jobs):
            pass


if __name__ == "__main__":
    main()
