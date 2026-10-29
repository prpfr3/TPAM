import json

from django.test import RequestFactory, SimpleTestCase

from locations.utils import create_folium_map, generate_storymap


class FoliumMapTests(SimpleTestCase):
    def test_openstreetmap_layer_uses_the_tile_proxy(self):
        map_html = create_folium_map([], [])

        self.assertIn("/storymaps/proxy_tile/{z}/{x}/{y}/", map_html)
        self.assertIn(r"\u00a9 OpenStreetMap contributors", map_html)

    def test_route_storymap_uses_the_tile_proxy(self):
        storymap = json.loads(
            generate_storymap(
                RequestFactory().get("/", secure=True), "title", "text", []
            )
        )["storymap"]

        self.assertEqual(
            storymap["map_type"],
            "https://testserver/storymaps/proxy_tile/{z}/{x}/{y}/",
        )
