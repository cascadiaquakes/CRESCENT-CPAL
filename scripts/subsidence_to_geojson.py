"""Convert the Dura et al. (2025) subsidence geodatabases to GeoJSON for the CPAL viewer.

Usage:
    python subsidence_to_geojson.py <folder with CascadiaPart*.gdb> <output folder>

Writes one file per view, with one feature per estuary:
    floodplain_{2023,2100}.geojson           floodplain for that year
    added_{2023,2100}_{low,med,hi}.geojson   extra area flooded after earthquake subsidence

Layer names follow two conventions in the source data:
    Oregon estuaries:   Coos01_2023, Coos01_2023_HI, Coos01_2023_HI_Erase, ...
    Willapa, Grays Harbor, Eureka: willapa23fp, willapa23hi(_Erase), willapa2100fp, ...
In the second group the 2100 "fp" layer is the change from 2023, so their 2100
floodplain is the 2023 floodplain plus that change.

Needs geopandas, pyogrio and shapely.
"""
import glob
import os
import re
import sys

import geopandas as gpd
import pandas as pd
import pyogrio
import shapely

TOLERANCE_M = 15        # simplification tolerance
MIN_AREA_M2 = 2000      # drop slivers smaller than this
UTM = 32610
INCREMENTAL = {"willapa", "grays", "eureka"}
NAMES = {"siletztosalmon": "Siletz to Salmon", "suislaw": "Siuslaw", "grays": "Grays Harbor",
         "eureka": "Humboldt Bay (Eureka)"}


def parse(name):
    """Return (estuary, year, scenario, kind) from a layer name, or None to skip it."""
    n = name.lower()
    est = re.match(r"[a-z]+", n).group(0)
    rest = n[len(est):]
    for suf in ("fp", "hi", "med", "low"):
        if est != "siletztosalmon" and est.endswith(suf):
            est = est[: -len(suf)]
    year = "2100" if "2100" in n else ("2023" if re.search(r"2023|(?<!\d)23(?!\d)", n) else None)
    scen = next((s for s in ("hi", "med", "low")
                 if re.search(rf"(?:^|_|\d){s}(?:_|\d|$)", rest) or re.match(rf"^[a-z]+?{s}\d", n)), "base")
    kind = "added" if n.endswith("erase") else "floodplain"
    if year is None or "_er_erase" in n:   # Nestucca01_2023_LOW_Er_Erase duplicates the _Erase layer
        return None
    return est, year, scen, kind


def read_layers(src):
    rows = []
    for gdb in sorted(glob.glob(os.path.join(src, "*.gdb"))):
        for name, _ in pyogrio.list_layers(gdb):
            key = parse(name)
            if key is None:
                print("skip", name)
                continue
            g = pyogrio.read_dataframe(gdb, layer=name)
            if g.crs is not None and g.crs.is_compound:
                g = g.set_crs(g.crs.sub_crs_list[0], allow_override=True)
            # Light simplification per layer first: merging full-resolution polygons is very slow.
            geom = shapely.make_valid(shapely.simplify(g.to_crs(UTM).geometry.values, 5, preserve_topology=True))
            rows.append(dict(zip(("estuary", "year", "scenario", "kind"), key), geometry=shapely.union_all(geom)))
            print("read", name, *key, flush=True)
    return gpd.GeoDataFrame(rows, crs=UTM)


def clean(geom):
    geom = shapely.make_valid(shapely.simplify(geom, TOLERANCE_M, preserve_topology=True))
    parts = [p for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon" and p.area >= MIN_AREA_M2]
    return shapely.MultiPolygon(parts) if parts else None


def write(out, name, rows):
    df = gpd.GeoDataFrame(rows, crs=UTM)
    df["geometry"] = [clean(x) for x in df.geometry]
    df = df[df.geometry.notna()]
    df["area_km2"] = df.area.div(1e6).round(2)
    path = os.path.join(out, f"{name}.geojson")
    df.to_crs(4326).to_file(path, driver="GeoJSON", COORDINATE_PRECISION=5)
    print(f"wrote {name}: {len(df)} estuaries, {df.area_km2.sum():.1f} km2, {os.path.getsize(path) / 1e6:.1f} MB")


def union(part):
    return shapely.union_all(shapely.make_valid(part.geometry.values), grid_size=0.01)


def main(src, out):
    os.makedirs(out, exist_ok=True)
    g = read_layers(src)
    for year in ("2023", "2100"):
        rows = []
        for est, e in g.groupby("estuary"):
            base = e[(e.scenario == "base") & (e.kind == "floodplain")]
            if est in INCREMENTAL and year == "2100":
                fp = pd.concat([base[base.year == "2023"], e[(e.year == "2100") & (e.scenario == "base")]])
            else:
                fp = base[base.year == year]
            if len(fp):
                rows.append({"estuary": NAMES.get(est, est.capitalize()), "year": year, "geometry": union(fp)})
        write(out, f"floodplain_{year}", rows)
        for scen in ("low", "med", "hi"):
            rows = []
            for est, e in g.groupby("estuary"):
                a = e[(e.year == year) & (e.scenario == scen) & (e.kind == "added")]
                if len(a):
                    rows.append({"estuary": NAMES.get(est, est.capitalize()), "year": year, "scenario": scen,
                                 "geometry": union(a)})
            write(out, f"added_{year}_{scen}", rows)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
