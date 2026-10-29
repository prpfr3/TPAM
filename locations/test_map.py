from django.test import SimpleTestCase

from locations.utils import create_folium_map


class FoliumMapTests(SimpleTestCase):
    def test_openstreetmap_layer_uses_the_tile_proxy(self):
        map_html = create_folium_map([], [])

        self.assertIn("/storymaps/proxy_tile/{z}/{x}/{y}/", map_html)
        self.assertIn(r"\u00a9 OpenStreetMap contributors", map_html)
