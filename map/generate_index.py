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
        <span style="color:#888">Paul Fishwick & Claude Code</span>
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

        function renderHeatmap() {{
            // IDW (Inverse Distance Weighting) interpolation on canvas
            const bounds = map.getBounds();
            const size = map.getSize();

            // Create canvas
            const canvas = document.createElement('canvas');
            canvas.width = size.x;
            canvas.height = size.y;
            const ctx = canvas.getContext('2d');

            // Resolution - lower = faster, higher = smoother
            const resolution = 3; // pixels per calculation
            const width = Math.ceil(canvas.width / resolution);
            const height = Math.ceil(canvas.height / resolution);

            // Precompute data point pixel positions
            const dataPoints = floridaData.map(point => {{
                const pixelPos = map.latLngToContainerPoint([point.lat, point.lon]);
                return {{
                    x: pixelPos.x,
                    y: pixelPos.y,
                    value: point[currentRP]
                }};
            }});

            // IDW parameters
            const power = 2;
            const maxDistance = 120; // Max influence distance in pixels

            // Color function returning RGB
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

            // Create image data
            const imageData = ctx.createImageData(width, height);
            const data = imageData.data;

            // Calculate interpolated values
            for (let py = 0; py < height; py++) {{
                for (let px = 0; px < width; px++) {{
                    const x = px * resolution;
                    const y = py * resolution;

                    let weightSum = 0;
                    let valueSum = 0;
                    let hasNearby = false;

                    for (const point of dataPoints) {{
                        const dx = x - point.x;
                        const dy = y - point.y;
                        const dist = Math.sqrt(dx * dx + dy * dy);

                        if (dist < maxDistance) {{
                            hasNearby = true;
                            if (dist < 1) {{
                                weightSum = 1;
                                valueSum = point.value;
                                break;
                            }}
                            const weight = 1 / Math.pow(dist, power);
                            weightSum += weight;
                            valueSum += weight * point.value;
                        }}
                    }}

                    const idx = (py * width + px) * 4;

                    if (hasNearby && weightSum > 0) {{
                        const interpolatedValue = valueSum / weightSum;
                        const [r, g, b] = getColorRGB(interpolatedValue);
                        data[idx] = r;
                        data[idx + 1] = g;
                        data[idx + 2] = b;
                        data[idx + 3] = 180;
                    }} else {{
                        data[idx + 3] = 0;
                    }}
                }}
            }}

            // Draw to temp canvas then scale up
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = width;
            tempCanvas.height = height;
            tempCanvas.getContext('2d').putImageData(imageData, 0, 0);

            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            ctx.drawImage(tempCanvas, 0, 0, width, height, 0, 0, canvas.width, canvas.height);

            // Create image overlay
            heatLayer = L.imageOverlay(canvas.toDataURL(), bounds, {{
                opacity: 0.85
            }}).addTo(map);

            // Redraw on map move
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

        function renderContours() {{
            // IDW interpolation + Marching Squares for smooth contour lines
            const thresholds = [30, 40, 45, 50, 55, 60, 70];
            const colors = ['#4575b4', '#74add1', '#abd9e9', '#fee090', '#fdae61', '#f46d43', '#d73027'];

            contourLayer.addTo(map);

            // Create interpolated grid in lat/lon space
            const bounds = map.getBounds();
            const gridRes = 0.05; // degrees per cell
            const latMin = bounds.getSouth();
            const latMax = bounds.getNorth();
            const lonMin = bounds.getWest();
            const lonMax = bounds.getEast();

            const rows = Math.ceil((latMax - latMin) / gridRes);
            const cols = Math.ceil((lonMax - lonMin) / gridRes);

            // IDW interpolation to create grid
            const power = 2;
            const maxDist = 0.3; // degrees

            const grid = [];
            for (let r = 0; r <= rows; r++) {{
                grid[r] = [];
                for (let c = 0; c <= cols; c++) {{
                    const lat = latMin + r * gridRes;
                    const lon = lonMin + c * gridRes;

                    let weightSum = 0;
                    let valueSum = 0;

                    for (const point of floridaData) {{
                        const dLat = lat - point.lat;
                        const dLon = lon - point.lon;
                        const dist = Math.sqrt(dLat * dLat + dLon * dLon);

                        if (dist < maxDist) {{
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

                    grid[r][c] = weightSum > 0 ? valueSum / weightSum : null;
                }}
            }}

            // Marching squares for each threshold
            thresholds.forEach((threshold, idx) => {{
                const color = colors[idx];
                const segments = [];

                // Find contour segments using marching squares
                for (let r = 0; r < rows; r++) {{
                    for (let c = 0; c < cols; c++) {{
                        const v00 = grid[r][c];
                        const v10 = grid[r][c + 1];
                        const v01 = grid[r + 1]?.[c];
                        const v11 = grid[r + 1]?.[c + 1];

                        if (v00 === null || v10 === null || v01 === null || v11 === null) continue;

                        // Determine cell configuration
                        const b00 = v00 >= threshold ? 1 : 0;
                        const b10 = v10 >= threshold ? 2 : 0;
                        const b01 = v01 >= threshold ? 4 : 0;
                        const b11 = v11 >= threshold ? 8 : 0;
                        const cellType = b00 + b10 + b01 + b11;

                        if (cellType === 0 || cellType === 15) continue;

                        const lat0 = latMin + r * gridRes;
                        const lat1 = latMin + (r + 1) * gridRes;
                        const lon0 = lonMin + c * gridRes;
                        const lon1 = lonMin + (c + 1) * gridRes;

                        // Interpolate edge crossings
                        const interp = (v1, v2, p1, p2) => {{
                            const t = (threshold - v1) / (v2 - v1);
                            return p1 + t * (p2 - p1);
                        }};

                        const edges = {{}};
                        if ((b00 !== 0) !== (b10 !== 0)) edges.bottom = [lat0, interp(v00, v10, lon0, lon1)];
                        if ((b01 !== 0) !== (b11 !== 0)) edges.top = [lat1, interp(v01, v11, lon0, lon1)];
                        if ((b00 !== 0) !== (b01 !== 0)) edges.left = [interp(v00, v01, lat0, lat1), lon0];
                        if ((b10 !== 0) !== (b11 !== 0)) edges.right = [interp(v10, v11, lat0, lat1), lon1];

                        // Connect edges based on cell type
                        const edgeKeys = Object.keys(edges);
                        if (edgeKeys.length >= 2) {{
                            if (cellType === 5 || cellType === 10) {{
                                // Saddle point - need special handling
                                segments.push([edges[edgeKeys[0]], edges[edgeKeys[1]]]);
                                if (edgeKeys.length === 4) {{
                                    segments.push([edges[edgeKeys[2]], edges[edgeKeys[3]]]);
                                }}
                            }} else {{
                                segments.push([edges[edgeKeys[0]], edges[edgeKeys[1]]]);
                            }}
                        }}
                    }}
                }}

                // Draw contour lines
                segments.forEach(seg => {{
                    const line = L.polyline([[seg[0][0], seg[0][1]], [seg[1][0], seg[1][1]]], {{
                        color: color,
                        weight: 2,
                        opacity: 0.8
                    }});
                    contourLayer.addLayer(line);
                }});

                // Add label at midpoint of longest segment group
                if (segments.length > 0) {{
                    const midSeg = segments[Math.floor(segments.length / 2)];
                    const labelLat = (midSeg[0][0] + midSeg[1][0]) / 2;
                    const labelLon = (midSeg[0][1] + midSeg[1][1]) / 2;
                    const label = L.marker([labelLat, labelLon], {{
                        icon: L.divIcon({{
                            className: 'contour-label',
                            html: `<span style="background:${{color}};color:white;padding:2px 4px;border-radius:3px;font-size:10px;font-weight:bold;">${{threshold}}</span>`,
                            iconSize: [30, 15]
                        }})
                    }});
                    contourLayer.addLayer(label);
                }}
            }});

            // Redraw on map move
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
