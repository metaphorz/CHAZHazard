# CHAZ Florida Hurricane Hazard Map - Project Plan

## Overview
Create an interactive Leaflet map showing tropical cyclone wind hazard data for Florida from the CHAZ (Columbia Hazard) model.

## Data Source
- Dataset: CHAZ Hazard Maps from Dryad (doi:10.5061/dryad.qfttdz0vz)
- Type: Exceedance intensity - wind speeds (m/s) for different return periods
- Return periods available: 10, 25, 50, 100, 250, 1000 years
- Florida bounding box: lat 24-31°N, lon -88 to -79.5°W
- Approximate points for Florida: ~2,618 coastal locations

## Todo List

- [x] Extract Florida data from global CSV into a smaller JSON file
- [x] Create HTML/JS/CSS Leaflet map with:
  - [x] Base map layer
  - [x] Color-coded markers/circles for wind intensity
  - [x] Dropdown to select return period (10/25/50/100/250/1000 yr)
  - [ ] Dropdown to select climate model and scenario (future enhancement)
  - [x] Legend showing wind speed scale
  - [x] Popup on click showing detailed values
- [x] Test the visualization in browser

## File Structure
```
CHAZ/
├── index.html          # Main Leaflet map
├── florida_data.json   # Extracted Florida data
├── outputs/            # Any output files
└── projectplan.md      # This file
```

## Technical Notes
- Use CircleMarkers for efficient rendering of ~2,600 points
- Color scale: Blue (low) → Yellow → Red (high wind speeds)
- WebGL not needed - standard Leaflet can handle this point count efficiently
