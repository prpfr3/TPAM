from django.test import SimpleTestCase

from locations.management.commands import Colliery_Load


class CollieryLoadCommandTests(SimpleTestCase):
    def test_build_geometry_uses_point_from_valid_coordinates(self):
        self.assertEqual(
            Colliery_Load.build_geometry("51.5", "-2.0"),
            "POINT (-2.0 51.5)",
        )

    def test_build_geometry_falls_back_when_coordinates_are_invalid(self):
        self.assertEqual(
            Colliery_Load.build_geometry("not-a-number", "-2.0", fallback="POINT (0 0)"),
            "POINT (0 0)",
        )

    def test_build_geometry_falls_back_when_coordinates_are_blank(self):
        self.assertEqual(
            Colliery_Load.build_geometry("", "   ", fallback="POINT (0 0)"),
            "POINT (0 0)",
        )
