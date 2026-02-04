#!/usr/bin/env python3
"""Generate index.html with SSP scenario dropdown and tooltips."""

import json

# Load the data
with open('florida_all_ssp.json', 'r') as f:
    all_data = json.load(f)

# Count points (use ssp585/CESM2/base as reference)
num_points = len(all_data['ssp585']['CESM2']['base'])

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CHAZ Florida Hurricane Hazard Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        #map {{
            height: 100vh;
            width: 100%;
        }}
        .controls {{
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            max-width: 320px;
        }}
        .controls h3 {{
            margin-bottom: 10px;
            font-size: 14px;
            color: #333;
        }}
        .control-group {{
            margin-bottom: 12px;
            position: relative;
        }}
        .control-group label {{
            display: block;
            margin-bottom: 3px;
            font-size: 12px;
            color: #666;
            cursor: help;
        }}
        .control-group select {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
        }}
        .tooltip-text {{
            display: none;
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 11px;
            width: 280px;
            z-index: 2000;
            line-height: 1.4;
            right: 335px;
            top: 0;
        }}
        .control-group:hover .tooltip-text {{
            display: block;
        }}
        .legend {{
            position: absolute;
            bottom: 30px;
            left: 10px;
            z-index: 1000;
            background: white;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .legend h4 {{
            margin-bottom: 8px;
            font-size: 12px;
            color: #333;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 4px;
            font-size: 11px;
        }}
        .legend-color {{
            width: 20px;
            height: 12px;
            margin-right: 8px;
            border-radius: 2px;
        }}
        .info-box {{
            position: absolute;
            bottom: 30px;
            right: 10px;
            z-index: 1000;
            background: white;
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            font-size: 11px;
            max-width: 250px;
        }}
        .info-box a {{
            color: #0066cc;
        }}
    </style>
</head>
<body>
    <div id="map"></div>

    <div class="controls">
        <h3>CHAZ Hurricane Hazard Map</h3>

        <div class="control-group">
            <label for="futureScenario">Future Scenario &#9432;</label>
            <div class="tooltip-text">
                <strong>SSP Scenarios</strong> (Shared Socioeconomic Pathways) represent different future emissions trajectories:<br><br>
                <strong>SSP245:</strong> Moderate mitigation, ~2.7°C warming by 2100<br>
                <strong>SSP370:</strong> Medium-high emissions, ~3.6°C warming<br>
                <strong>SSP585:</strong> High emissions (fossil-fueled), ~4.4°C warming
            </div>
            <select id="futureScenario">
                <option value="ssp245">SSP245 (Moderate)</option>
                <option value="ssp370">SSP370 (Medium-High)</option>
                <option value="ssp585" selected>SSP585 (High Emissions)</option>
            </select>
        </div>

        <div class="control-group">
            <label for="climateModel">Climate Model &#9432;</label>
            <div class="tooltip-text">
                <strong>CMIP6 Climate Models</strong> used to drive CHAZ hurricane simulations. Different models have different assumptions about physical processes. Multi-Model Mean averages all 6 models to reduce individual model biases.
            </div>
            <select id="climateModel">
                <option value="CESM2" selected>CESM2 (USA)</option>
                <option value="CNRM-CM6-1">CNRM-CM6-1 (France)</option>
                <option value="EC-Earth3">EC-Earth3 (Europe)</option>
                <option value="IPSL-CM6A-LR">IPSL-CM6A-LR (France)</option>
                <option value="MIROC6">MIROC6 (Japan)</option>
                <option value="UKESM1-0-LL">UKESM1-0-LL (UK)</option>
                <option value="MultiModelMean">Multi-Model Mean (6 models)</option>
            </select>
        </div>

        <div class="control-group">
            <label for="timePeriod">Time Period &#9432;</label>
            <div class="tooltip-text">
                <strong>Historical:</strong> Baseline conditions (1995-2014)<br>
                <strong>Mid-Century:</strong> Near-future projection (2041-2060)<br>
                <strong>Late-Century:</strong> End-of-century projection (2081-2100)
            </div>
            <select id="timePeriod">
                <option value="base" selected>Historical (1995-2014)</option>
                <option value="fut1">Mid-Century (2041-2060)</option>
                <option value="fut2">Late-Century (2081-2100)</option>
            </select>
        </div>

        <div class="control-group">
            <label for="returnPeriod">Return Period &#9432;</label>
            <div class="tooltip-text">
                <strong>Return Period</strong> is the average time between events of this intensity. A 100-year wind speed has a 1% chance of being exceeded in any given year. Higher return periods show rarer, more extreme events.
            </div>
            <select id="returnPeriod">
                <option value="rp10">10-year</option>
                <option value="rp25">25-year</option>
                <option value="rp50">50-year</option>
                <option value="rp100">100-year</option>
                <option value="rp250" selected>250-year</option>
                <option value="rp1000">1000-year</option>
            </select>
        </div>

        <div class="control-group">
            <label for="displayMode">Display &#9432;</label>
            <div class="tooltip-text">
                <strong>Circle:</strong> Individual data points as colored circles<br>
                <strong>Heatmap:</strong> Continuous heat visualization showing intensity density<br>
                <strong>Contour:</strong> Isolines connecting points of equal wind speed
            </div>
            <select id="displayMode">
                <option value="circle" selected>Circle</option>
                <option value="heatmap">Heatmap</option>
                <option value="contour">Contour</option>
            </select>
            <div id="contourNote" style="display:none; color:#666; font-size:10px; margin-top:3px; font-style:italic;">Contour values in mph</div>
        </div>

        <div style="color:#888; font-size:10px; margin-top:5px;">{num_points:,} land points</div>
    </div>

    <div class="legend">
        <h4>Wind Speed</h4>
        <table style="font-size:10px; border-collapse:separate; border-spacing:6px 2px;">
            <tr style="color:#666"><td></td><td>m/s</td><td>km/h</td><td>mph</td></tr>
            <tr><td><div class="legend-color" style="background:#313695"></div></td><td>0-20</td><td>0-72</td><td>0-45</td></tr>
            <tr><td><div class="legend-color" style="background:#4575b4"></div></td><td>20-30</td><td>72-108</td><td>45-67</td></tr>
            <tr><td><div class="legend-color" style="background:#74add1"></div></td><td>30-40</td><td>108-144</td><td>67-89</td></tr>
            <tr><td><div class="legend-color" style="background:#abd9e9"></div></td><td>40-45</td><td>144-162</td><td>89-101</td></tr>
            <tr><td><div class="legend-color" style="background:#ffffbf"></div></td><td>45-50</td><td>162-180</td><td>101-112</td></tr>
            <tr><td><div class="legend-color" style="background:#fee090"></div></td><td>50-55</td><td>180-198</td><td>112-123</td></tr>
            <tr><td><div class="legend-color" style="background:#fdae61"></div></td><td>55-60</td><td>198-216</td><td>123-134</td></tr>
            <tr><td><div class="legend-color" style="background:#f46d43"></div></td><td>60-70</td><td>216-252</td><td>134-157</td></tr>
            <tr><td><div class="legend-color" style="background:#d73027"></div></td><td>70-80</td><td>252-288</td><td>157-179</td></tr>
            <tr><td><div class="legend-color" style="background:#a50026"></div></td><td>80+</td><td>288+</td><td>179+</td></tr>
        </table>
    </div>

    <div class="info-box">
        <strong>CHAZ Hazard Maps</strong><br>
        Columbia Hazard tropical cyclone model<br>
        <a href="https://datadryad.org/dataset/doi:10.5061/dryad.qfttdz0vz" target="_blank">Data source (Dryad)</a><br>
        <a href="https://doi.org/10.5061/dryad.qfttdz0vz" target="_blank">Paper</a>: Meiler, Lee, Sobel, Camargo (2025)<br>
        <span style="color:#888">Visual Tool: Paul Fishwick & Claude Code</span>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Initialize map centered on Florida
        const map = L.map('map').setView([27.5, -82.5], 7);

        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        }}).addTo(map);

        // Color scale for wind speeds (m/s)
        function getColor(speed) {{
            return speed >= 80 ? '#a50026' :
                   speed >= 70 ? '#d73027' :
                   speed >= 60 ? '#f46d43' :
                   speed >= 55 ? '#fdae61' :
                   speed >= 50 ? '#fee090' :
                   speed >= 45 ? '#ffffbf' :
                   speed >= 40 ? '#abd9e9' :
                   speed >= 30 ? '#74add1' :
                   speed >= 20 ? '#4575b4' :
                                 '#313695';
        }}

        // Hurricane category based on wind speed (m/s)
        function getCategory(speed) {{
            const knots = speed * 1.944;
            if (knots >= 137) return 'Category 5';
            if (knots >= 113) return 'Category 4';
            if (knots >= 96) return 'Category 3';
            if (knots >= 83) return 'Category 2';
            if (knots >= 64) return 'Category 1';
            if (knots >= 34) return 'Tropical Storm';
            return 'Tropical Depression';
        }}

        // All model data embedded
        const allModelData = {json.dumps(all_data)};

        let floridaData = [];
        let markers = L.layerGroup().addTo(map);
        let heatLayer = null;
        let contourLayer = L.layerGroup();
        let currentRP = 'rp250';
        let currentPeriod = 'base';
        let currentModel = 'CESM2';
        let currentSSP = 'ssp585';
        let currentDisplay = 'circle';

        // Initialize data
        floridaData = allModelData[currentSSP][currentModel][currentPeriod];
        renderVisualization();

        function clearAllLayers() {{
            markers.clearLayers();
            if (heatLayer) {{
                map.removeLayer(heatLayer);
                heatLayer = null;
            }}
            contourLayer.clearLayers();
            map.removeLayer(contourLayer);
        }}

        function renderVisualization() {{
            clearAllLayers();

            if (currentDisplay === 'circle') {{
                renderCircles();
            }} else if (currentDisplay === 'heatmap') {{
                renderHeatmap();
            }} else if (currentDisplay === 'contour') {{
                renderContours();
            }}
        }}

        function renderCircles() {{
            floridaData.forEach(point => {{
                const windSpeed = point[currentRP];
                const color = getColor(windSpeed);

                const marker = L.circleMarker([point.lat, point.lon], {{
                    radius: 5,
                    fillColor: color,
                    color: color,
                    weight: 1,
                    opacity: 0.8,
                    fillOpacity: 0.7
                }});

                const kmh = (windSpeed * 3.6).toFixed(0);
                const mph = (windSpeed * 2.237).toFixed(0);
                const category = getCategory(windSpeed);

                marker.bindTooltip(
                    `<strong>${{point.lat.toFixed(2)}}°N, ${{Math.abs(point.lon).toFixed(2)}}°W</strong><br>` +
                    `<strong>${{windSpeed.toFixed(1)}} m/s</strong> (${{kmh}} km/h, ${{mph}} mph)<br>` +
                    `${{category}}<br><hr style="margin:4px 0">` +
                    `<span style="font-size:10px">` +
                    `10yr: ${{point.rp10}} | 25yr: ${{point.rp25}} | 50yr: ${{point.rp50}}<br>` +
                    `100yr: ${{point.rp100}} | 250yr: ${{point.rp250}} | 1000yr: ${{point.rp1000}}</span>`,
                    {{ direction: 'bottom', offset: [0, 10] }}
                );

                markers.addLayer(marker);
            }});
        }}

        // Find nearest data point to a given lat/lon
        function findNearestPoint(lat, lon) {{
            let nearest = null;
            let minDist = Infinity;
            for (const point of floridaData) {{
                const dLat = lat - point.lat;
                const dLon = lon - point.lon;
                const dist = dLat * dLat + dLon * dLon;
                if (dist < minDist) {{
                    minDist = dist;
                    nearest = point;
                }}
            }}
            // Only return if within ~0.1 degree (~11km)
            return minDist < 0.01 ? nearest : null;
        }}

        // Create a popup for heatmap/contour tooltips
        let hoverPopup = L.popup({{ closeButton: false, offset: [0, -5] }});

        function formatPointTooltip(point) {{
            const windSpeed = point[currentRP];
            const kmh = (windSpeed * 3.6).toFixed(0);
            const mph = (windSpeed * 2.237).toFixed(0);
            const category = getCategory(windSpeed);
            return `<strong>${{point.lat.toFixed(2)}}°N, ${{Math.abs(point.lon).toFixed(2)}}°W</strong><br>` +
                `<strong>${{windSpeed.toFixed(1)}} m/s</strong> (${{kmh}} km/h, ${{mph}} mph)<br>` +
                `${{category}}<br><hr style="margin:4px 0">` +
                `<span style="font-size:10px">` +
                `10yr: ${{point.rp10}} | 25yr: ${{point.rp25}} | 50yr: ${{point.rp50}}<br>` +
                `100yr: ${{point.rp100}} | 250yr: ${{point.rp250}} | 1000yr: ${{point.rp1000}}</span>`;
        }}

        function onMapMouseMove(e) {{
            if (currentDisplay === 'circle') return; // Circles have their own tooltips
            const point = findNearestPoint(e.latlng.lat, e.latlng.lng);
            if (point) {{
                hoverPopup
                    .setLatLng(e.latlng)
                    .setContent(formatPointTooltip(point))
                    .openOn(map);
            }} else {{
                map.closePopup(hoverPopup);
            }}
        }}

        function onMapMouseOut() {{
            map.closePopup(hoverPopup);
        }}

        map.on('mousemove', onMapMouseMove);
        map.on('mouseout', onMapMouseOut);

        // Florida land polygon for boundary checking
        const FLORIDA_POLYGON = [
            [-87.5, 30.95], [-87.5, 30.1], [-86.5, 30.1], [-85.5, 29.7],
            [-85.0, 29.1], [-84.0, 29.6], [-83.5, 29.0], [-82.8, 28.0],
            [-82.7, 27.5], [-82.1, 26.5], [-81.5, 25.9], [-80.9, 25.1],
            [-80.1, 25.1], [-80.1, 26.0], [-80.1, 27.0], [-80.3, 28.0],
            [-80.6, 28.5], [-81.2, 29.5], [-81.3, 30.1], [-81.5, 30.7],
            [-82.0, 30.6], [-82.5, 30.4], [-83.0, 30.5], [-84.0, 30.5],
            [-85.0, 30.95], [-87.5, 30.95]
        ];
        const KEYS_POLYGON = [
            [-82.0, 24.5], [-81.5, 24.5], [-80.3, 25.0], [-80.0, 25.2],
            [-80.5, 25.5], [-81.0, 25.2], [-81.8, 24.7], [-82.0, 24.5]
        ];

        // Point-in-polygon test
        function pointInPolygon(lon, lat, polygon) {{
            let inside = false;
            const n = polygon.length;
            let p1x = polygon[0][0], p1y = polygon[0][1];
            for (let i = 1; i <= n; i++) {{
                const p2x = polygon[i % n][0], p2y = polygon[i % n][1];
                if (lat > Math.min(p1y, p2y)) {{
                    if (lat <= Math.max(p1y, p2y)) {{
                        if (lon <= Math.max(p1x, p2x)) {{
                            if (p1y !== p2y) {{
                                const xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x;
                                if (p1x === p2x || lon <= xinters) {{
                                    inside = !inside;
                                }}
                            }}
                        }}
                    }}
                }}
                p1x = p2x; p1y = p2y;
            }}
            return inside;
        }}

        function isFloridaLand(lon, lat) {{
            return pointInPolygon(lon, lat, FLORIDA_POLYGON) || pointInPolygon(lon, lat, KEYS_POLYGON);
        }}

        // Compute data bounds from Florida points
        function getDataBounds() {{
            const lats = floridaData.map(p => p.lat);
            const lons = floridaData.map(p => p.lon);
            return {{
                latMin: Math.min(...lats),
                latMax: Math.max(...lats),
                lonMin: Math.min(...lons),
                lonMax: Math.max(...lons)
            }};
        }}

        // IDW grid generation (similar to KDE approach but for scalar values)
        function idwGrid(NX = 150, NY = 150) {{
            const bounds = getDataBounds();
            const padding = 0.05; // Small padding in degrees
            const latMin = bounds.latMin - padding;
            const latMax = bounds.latMax + padding;
            const lonMin = bounds.lonMin - padding;
            const lonMax = bounds.lonMax + padding;

            const dx = (lonMax - lonMin) / (NX - 1);
            const dy = (latMax - latMin) / (NY - 1);

            const power = 2;
            const maxDist = 0.15; // degrees - tight constraint to data

            const raw = new Float64Array(NX * NY);
            const valid = new Uint8Array(NX * NY);

            for (let iy = 0; iy < NY; iy++) {{
                const lat = latMin + iy * dy;
                for (let ix = 0; ix < NX; ix++) {{
                    const lon = lonMin + ix * dx;

                    let weightSum = 0;
                    let valueSum = 0;
                    let nearCount = 0;

                    for (const point of floridaData) {{
                        const dLat = lat - point.lat;
                        const dLon = lon - point.lon;
                        const dist = Math.sqrt(dLat * dLat + dLon * dLon);

                        if (dist < maxDist) {{
                            nearCount++;
                            if (dist < 0.001) {{
                                weightSum = 1;
                                valueSum = point[currentRP];
                                break;
                            }}
                            const weight = 1 / Math.pow(dist, power);
                            weightSum += weight;
                            valueSum += weight * point[currentRP];
                        }}
                    }}

                    const idx = iy * NX + ix;
                    if (nearCount >= 2 && weightSum > 0) {{
                        raw[idx] = valueSum / weightSum;
                        valid[idx] = 1;
                    }} else {{
                        raw[idx] = 0;
                        valid[idx] = 0;
                    }}
                }}
            }}

            let gmin = Infinity, gmax = -Infinity;
            for (let i = 0; i < raw.length; i++) {{
                if (valid[i]) {{
                    if (raw[i] < gmin) gmin = raw[i];
                    if (raw[i] > gmax) gmax = raw[i];
                }}
            }}

            return {{ raw, valid, NX, NY, lonMin, latMin, dx, dy, gmin, gmax }};
        }}

        function renderHeatmap() {{
            // Generate IDW grid
            const G = idwGrid(150, 150);
            if (!G) return;

            // Create canvas for the grid area
            const canvas = document.createElement('canvas');
            canvas.width = G.NX;
            canvas.height = G.NY;
            const ctx = canvas.getContext('2d');
            const imageData = ctx.createImageData(G.NX, G.NY);
            const data = imageData.data;

            // Color function
            function getColorRGB(speed) {{
                if (speed >= 80) return [165, 0, 38];
                if (speed >= 70) return [215, 48, 39];
                if (speed >= 60) return [244, 109, 67];
                if (speed >= 55) return [253, 174, 97];
                if (speed >= 50) return [254, 224, 144];
                if (speed >= 45) return [255, 255, 191];
                if (speed >= 40) return [171, 217, 233];
                if (speed >= 30) return [116, 173, 209];
                if (speed >= 20) return [69, 117, 180];
                return [49, 54, 149];
            }}

            // Fill image data (flip Y for canvas coordinates)
            for (let iy = 0; iy < G.NY; iy++) {{
                for (let ix = 0; ix < G.NX; ix++) {{
                    const srcIdx = iy * G.NX + ix;
                    const dstIdx = ((G.NY - 1 - iy) * G.NX + ix) * 4;

                    if (G.valid[srcIdx]) {{
                        const [r, g, b] = getColorRGB(G.raw[srcIdx]);
                        data[dstIdx] = r;
                        data[dstIdx + 1] = g;
                        data[dstIdx + 2] = b;
                        data[dstIdx + 3] = 180;
                    }} else {{
                        data[dstIdx + 3] = 0;
                    }}
                }}
            }}

            ctx.putImageData(imageData, 0, 0);

            // Create bounds for overlay
            const imageBounds = [
                [G.latMin, G.lonMin],
                [G.latMin + G.NY * G.dy, G.lonMin + G.NX * G.dx]
            ];

            heatLayer = L.imageOverlay(canvas.toDataURL(), imageBounds, {{
                opacity: 0.85
            }}).addTo(map);

            map.off('moveend', onMapMove);
            map.on('moveend', onMapMove);
        }}

        function onMapMove() {{
            if (currentDisplay === 'heatmap') {{
                if (heatLayer) {{
                    map.removeLayer(heatLayer);
                    heatLayer = null;
                }}
                renderHeatmap();
            }}
        }}

        // Linear interpolation for contour edge crossing (from genesis-codex)
        function contourInterpolate(t, vA, vB, xA, yA, xB, yB) {{
            const d = vB - vA;
            if (Math.abs(d) < 1e-12) return [(xA + xB) / 2, (yA + yB) / 2];
            const s = (t - vA) / d;
            return [xA + s * (xB - xA), yA + s * (yB - yA)];
        }}

        // Marching squares segment extraction (from genesis-codex)
        function buildSegments(field, valid, NX, NY, t, lonMin, latMin, dx, dy) {{
            const get = (ix, iy) => field[iy * NX + ix];
            const isValid = (ix, iy) => valid[iy * NX + ix];
            const segs = [];

            for (let iy = 0; iy < NY - 1; iy++) {{
                for (let ix = 0; ix < NX - 1; ix++) {{
                    // Skip if any corner is invalid
                    if (!isValid(ix, iy) || !isValid(ix + 1, iy) ||
                        !isValid(ix, iy + 1) || !isValid(ix + 1, iy + 1)) continue;

                    const tl = get(ix, iy), tr = get(ix + 1, iy);
                    const br = get(ix + 1, iy + 1), bl = get(ix, iy + 1);

                    let idx = 0;
                    if (tl >= t) idx |= 1;
                    if (tr >= t) idx |= 2;
                    if (br >= t) idx |= 4;
                    if (bl >= t) idx |= 8;

                    if (idx === 0 || idx === 15) continue;

                    const top = contourInterpolate(t, tl, tr, ix, iy, ix + 1, iy);
                    const right = contourInterpolate(t, tr, br, ix + 1, iy, ix + 1, iy + 1);
                    const bottom = contourInterpolate(t, bl, br, ix, iy + 1, ix + 1, iy + 1);
                    const left = contourInterpolate(t, tl, bl, ix, iy, ix, iy + 1);

                    const center = (tl + tr + br + bl) / 4;

                    switch (idx) {{
                        case 1: case 14: segs.push([left, top]); break;
                        case 2: case 13: segs.push([top, right]); break;
                        case 3: case 12: segs.push([left, right]); break;
                        case 4: case 11: segs.push([right, bottom]); break;
                        case 6: case 9: segs.push([top, bottom]); break;
                        case 7: case 8: segs.push([bottom, left]); break;
                        case 5:
                            if (center >= t) {{ segs.push([top, right]); segs.push([bottom, left]); }}
                            else {{ segs.push([left, top]); segs.push([right, bottom]); }}
                            break;
                        case 10:
                            if (center >= t) {{ segs.push([left, top]); segs.push([right, bottom]); }}
                            else {{ segs.push([top, right]); segs.push([bottom, left]); }}
                            break;
                    }}
                }}
            }}

            // Convert grid coordinates to lat/lon and filter to Florida land
            const result = [];
            for (const seg of segs) {{
                const lat1 = latMin + seg[0][1] * dy;
                const lon1 = lonMin + seg[0][0] * dx;
                const lat2 = latMin + seg[1][1] * dy;
                const lon2 = lonMin + seg[1][0] * dx;
                // Check midpoint is on Florida land
                const midLat = (lat1 + lat2) / 2;
                const midLon = (lon1 + lon2) / 2;
                if (isFloridaLand(midLon, midLat)) {{
                    result.push([[lat1, lon1], [lat2, lon2]]);
                }}
            }}
            return result;
        }}

        // Stitch segments into continuous polylines (from genesis-codex)
        function stitchSegments(segs) {{
            const key = (p) => p[0].toFixed(4) + "," + p[1].toFixed(4);
            const buckets = new Map();

            segs.forEach((s, i) => {{
                const k1 = key(s[0]), k2 = key(s[1]);
                if (!buckets.has(k1)) buckets.set(k1, []);
                if (!buckets.has(k2)) buckets.set(k2, []);
                buckets.get(k1).push(i);
                buckets.get(k2).push(i);
            }});

            const used = new Array(segs.length).fill(false);
            const polylines = [];

            function takeChain(startIdx) {{
                const chain = [];
                used[startIdx] = true;
                let a = segs[startIdx][0], b = segs[startIdx][1];
                chain.push(a, b);
                let cur = b;

                while (true) {{
                    const k = key(cur);
                    const cand = buckets.get(k) || [];
                    let nextIdx = -1, flip = false;

                    for (let j of cand) {{
                        if (used[j]) continue;
                        const s = segs[j];
                        const k0 = key(s[0]), k1 = key(s[1]);
                        if (k0 === k) {{ nextIdx = j; flip = false; break; }}
                        if (k1 === k) {{ nextIdx = j; flip = true; break; }}
                    }}

                    if (nextIdx < 0) break;
                    used[nextIdx] = true;
                    const s = segs[nextIdx];
                    const nextPoint = flip ? s[0] : s[1];
                    chain.push(nextPoint);
                    cur = nextPoint;
                    if (key(cur) === key(chain[0])) break; // closed loop
                }}
                return chain;
            }}

            for (let i = 0; i < segs.length; i++) {{
                if (used[i]) continue;
                polylines.push(takeChain(i));
            }}
            return polylines;
        }}

        function renderContours() {{
            const thresholds = [30, 40, 45, 50, 55, 60, 70];
            const colors = ['#4575b4', '#74add1', '#abd9e9', '#fee090', '#fdae61', '#f46d43', '#d73027'];

            contourLayer.addTo(map);

            // Generate IDW grid
            const G = idwGrid(120, 120);
            if (!G) return;

            thresholds.forEach((threshold, idx) => {{
                const color = colors[idx];

                // Build segments using marching squares
                const segments = buildSegments(G.raw, G.valid, G.NX, G.NY, threshold,
                    G.lonMin, G.latMin, G.dx, G.dy);

                if (segments.length === 0) return;

                // Stitch into continuous polylines
                const polylines = stitchSegments(segments);

                // Draw polylines and label all reasonably large ones
                const MIN_LABEL_LENGTH = 8; // Minimum points for a contour to get a label

                const mphValue = Math.round(threshold * 2.237); // Convert m/s to mph

                polylines.forEach(chain => {{
                    if (chain.length >= 2) {{
                        const line = L.polyline(chain, {{
                            color: color,
                            weight: 2.5,
                            opacity: 0.9
                        }});
                        line.bindTooltip(`${{mphValue}} mph (${{threshold}} m/s)`, {{ sticky: true }});
                        contourLayer.addLayer(line);

                        // Add label on all reasonably large contours
                        if (chain.length >= MIN_LABEL_LENGTH) {{
                            const midIdx = Math.floor(chain.length / 2);
                            const label = L.marker(chain[midIdx], {{
                                icon: L.divIcon({{
                                    className: 'contour-label',
                                    html: `<span style="background:${{color}};color:white;padding:2px 4px;border-radius:3px;font-size:10px;font-weight:bold;">${{mphValue}}</span>`,
                                    iconSize: [30, 15]
                                }})
                            }});
                            contourLayer.addLayer(label);
                        }}
                    }}
                }});
            }});

            map.off('moveend', onContourMove);
            map.on('moveend', onContourMove);
        }}

        function onContourMove() {{
            if (currentDisplay === 'contour') {{
                contourLayer.clearLayers();
                renderContours();
            }}
        }}

        // Handle future scenario (SSP) change
        document.getElementById('futureScenario').addEventListener('change', function(e) {{
            currentSSP = e.target.value;
            floridaData = allModelData[currentSSP][currentModel][currentPeriod];
            renderVisualization();
        }});

        // Handle climate model change
        document.getElementById('climateModel').addEventListener('change', function(e) {{
            currentModel = e.target.value;
            floridaData = allModelData[currentSSP][currentModel][currentPeriod];
            renderVisualization();
        }});

        // Handle time period change
        document.getElementById('timePeriod').addEventListener('change', function(e) {{
            currentPeriod = e.target.value;
            floridaData = allModelData[currentSSP][currentModel][currentPeriod];
            renderVisualization();
        }});

        // Handle return period change
        document.getElementById('returnPeriod').addEventListener('change', function(e) {{
            currentRP = e.target.value;
            renderVisualization();
        }});

        // Handle display mode change
        document.getElementById('displayMode').addEventListener('change', function(e) {{
            currentDisplay = e.target.value;
            document.getElementById('contourNote').style.display = currentDisplay === 'contour' ? 'block' : 'none';
            renderVisualization();
        }});
    </script>
</body>
</html>
'''

# Write the output
with open('index.html', 'w') as f:
    f.write(html_content)

import os
file_size = os.path.getsize('index.html') / (1024 * 1024)
print(f"Generated index.html: {file_size:.1f} MB")
