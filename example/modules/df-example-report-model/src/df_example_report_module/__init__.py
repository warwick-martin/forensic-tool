from io import StringIO
from typing import List, Any, Dict

import gpxpy
from df_modules import ReportModule
import htmlmin

class Report(ReportModule):
    @staticmethod
    def version() -> str:
        """Return the version of the module."""
        return "0.1.0"

    @staticmethod
    def input_data_structures() -> List[str]:
        """Return the data structures that this module can read."""
        return ["GPX"]

    @staticmethod
    def report(data: str) -> dict[str, str]:

        print(data)
        """Generate a report from the data and return it as a string."""
        # doc = gpxpy.parse(StringIO(data))
        # data = htmlmin.minify(data, remove_comments=True, remove_empty_space=True)
        head = """
<link type="text/css" rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />    
    """
        body = f"""
<div id="map" style="height:500px;"></div>
<script src="https://unpkg.com/leaflet/dist/leaflet-src.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-gpx/2.1.0/gpx.min.js" defer></script>
<script type="module">
    const map = L.map('map').on('loaded', function(e) {{map.fitBounds(e.target.getBounds());}});
    L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        center: [39, -105],
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }}).addTo(map);
    
    // URL to your GPX file or the GPX itself as a XML string.
    const data = `{data}`;
    const options = {{
        async: true,
        polyline_options: {{color: 'red' }},
    }};
    
    const gpx = new L.GPX(data, options).on('loaded', (e) => {{
        map.fitBounds(e.target.getBounds());
    }}).addTo(map);
</script>
        """

        print(body)
        return {'head': head, 'body': body}