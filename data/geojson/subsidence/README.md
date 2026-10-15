# Coastal flooding after earthquake subsidence

Floodplain and earthquake-subsidence flooding polygons for 26 Pacific Northwest estuaries, shown in the "Coastal Flooding" layer of the [CPAL viewer](https://cpal.cascadiaquakes.org).

## Source

Dura, T., et al. (2025). Increased flood exposure in the Pacific Northwest following earthquake-driven subsidence and sea-level rise. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.2424659122

Original geodatabases: [DuraGEOSVT/Cascadia](https://github.com/DuraGEOSVT/Cascadia) (parts 1 to 3) and [DuraGEOSVT/Cascadia2](https://github.com/DuraGEOSVT/Cascadia2) (parts 4 to 6).

These files are a simplified copy for display. Please cite the paper above and use the original data for analysis. They are not covered by this repository's CC BY 4.0 license; the original authors' terms apply.

## Files

| File | Contents |
|---|---|
| `floodplain_2023.geojson`, `floodplain_2100.geojson` | Floodplain for that year |
| `added_{year}_{low,med,hi}.geojson` | Extra area flooded after low, medium or high earthquake subsidence |

Each file has one feature per estuary with `estuary`, `year`, `scenario` (added files only) and `area_km2`.

## How they were made

[`scripts/subsidence_to_geojson.py`](../../../scripts/subsidence_to_geojson.py) reads the geodatabases, merges each estuary's layers, simplifies them to about 15 m, drops slivers under 2000 m², and writes WGS84 GeoJSON.
