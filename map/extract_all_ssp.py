#!/usr/bin/env python3
"""Extract Florida data for all SSP scenarios, all models, all time periods."""

import json
import os

# Florida land polygon for filtering (simplified)
FLORIDA_POLYGON = [
    (-87.5, 30.95), (-87.5, 30.1), (-86.5, 30.1), (-85.5, 29.7),
    (-85.0, 29.1), (-84.0, 29.6), (-83.5, 29.0), (-82.8, 28.0),
    (-82.7, 27.5), (-82.1, 26.5), (-81.5, 25.9), (-80.9, 25.1),
    (-80.1, 25.1), (-80.1, 26.0), (-80.1, 27.0), (-80.3, 28.0),
    (-80.6, 28.5), (-81.2, 29.5), (-81.3, 30.1), (-81.5, 30.7),
    (-82.0, 30.6), (-82.5, 30.4), (-83.0, 30.5), (-84.0, 30.5),
    (-85.0, 30.95), (-87.5, 30.95)
]

# Florida Keys
KEYS_POLYGON = [
    (-82.0, 24.5), (-81.5, 24.5), (-80.3, 25.0), (-80.0, 25.2),
    (-80.5, 25.5), (-81.0, 25.2), (-81.8, 24.7), (-82.0, 24.5)
]

def point_in_polygon(x, y, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def is_florida_land(lon, lat):
    return point_in_polygon(lon, lat, FLORIDA_POLYGON) or point_in_polygon(lon, lat, KEYS_POLYGON)

def extract_model_data(csv_path):
    """Extract Florida land points from a CSV file."""
    points = []
    with open(csv_path, 'r') as f:
        header = f.readline().strip().split(',')
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 8:
                lon = float(parts[0])  # CSV has lon first
                lat = float(parts[1])  # then lat
                # Bounding box check first
                if 24 <= lat <= 31 and -88 <= lon <= -79.5:
                    # Land check
                    if is_florida_land(lon, lat):
                        points.append({
                            'lat': round(lat, 2),
                            'lon': round(lon, 2),
                            'rp10': round(float(parts[2]), 1),
                            'rp25': round(float(parts[3]), 1),
                            'rp50': round(float(parts[4]), 1),
                            'rp100': round(float(parts[5]), 1),
                            'rp250': round(float(parts[6]), 1),
                            'rp1000': round(float(parts[7]), 1)
                        })
    return points

# Configuration
base_path = '/Volumes/Fish/CHAZ/map/exceedance_intensity/csv/per-GCM'
models = ['CESM2', 'CNRM-CM6-1', 'EC-Earth3', 'IPSL-CM6A-LR', 'MIROC6', 'UKESM1-0-LL']
ssps = ['ssp245', 'ssp370', 'ssp585']
periods = ['base', 'fut1', 'fut2']

# Extract all data
all_data = {}

for ssp in ssps:
    print(f"\nProcessing {ssp}...")
    all_data[ssp] = {}

    for model in models:
        print(f"  {model}...", end=' ')
        all_data[ssp][model] = {}

        for period in periods:
            # Actual filename format: TC_global_0300as_CHAZ_CESM2_base_ssp585_80ens_SD_H08_exceedance_intensity.csv
            csv_file = f"{base_path}/{model}/{ssp}/TC_global_0300as_CHAZ_{model}_{period}_{ssp}_80ens_SD_H08_exceedance_intensity.csv"
            if os.path.exists(csv_file):
                points = extract_model_data(csv_file)
                all_data[ssp][model][period] = points
                print(f"{period}:{len(points)}", end=' ')
            else:
                print(f"{period}:MISSING ({csv_file})", end=' ')
                all_data[ssp][model][period] = []
        print()

    # Compute multi-model mean for this SSP
    print(f"  Computing Multi-Model Mean...", end=' ')
    all_data[ssp]['MultiModelMean'] = {}

    for period in periods:
        # Get reference points from first model with data
        ref_points = None
        for model in models:
            if all_data[ssp][model][period]:
                ref_points = all_data[ssp][model][period]
                break

        if ref_points:
            mean_points = []
            for i, ref_pt in enumerate(ref_points):
                mean_pt = {
                    'lat': ref_pt['lat'],
                    'lon': ref_pt['lon']
                }
                for rp in ['rp10', 'rp25', 'rp50', 'rp100', 'rp250', 'rp1000']:
                    values = []
                    for model in models:
                        if all_data[ssp][model][period] and i < len(all_data[ssp][model][period]):
                            values.append(all_data[ssp][model][period][i][rp])
                    if values:
                        mean_pt[rp] = round(sum(values) / len(values), 1)
                    else:
                        mean_pt[rp] = 0
                mean_points.append(mean_pt)
            all_data[ssp]['MultiModelMean'][period] = mean_points
            print(f"{period}:{len(mean_points)}", end=' ')
        else:
            all_data[ssp]['MultiModelMean'][period] = []
            print(f"{period}:0", end=' ')
    print()

# Save to JSON
output_file = '/Volumes/Fish/CHAZ/map/florida_all_ssp.json'
with open(output_file, 'w') as f:
    json.dump(all_data, f)

# Report size
file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"\nOutput: {output_file}")
print(f"Size: {file_size:.1f} MB")

# Count total points
total_points = 0
for ssp in all_data:
    for model in all_data[ssp]:
        for period in all_data[ssp][model]:
            total_points += len(all_data[ssp][model][period])
print(f"Total data points: {total_points:,}")
