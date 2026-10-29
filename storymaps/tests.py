from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase

from storymaps.views import proxy_tile


class TileProxyTests(SimpleTestCase):
    @patch("requests.get")
    def test_proxy_sends_application_user_agent_and_referer(self, get):
        get.return_value = Mock(
            status_code=200,
            content=b"tile",
            headers={"content-type": "image/png"},
        )
        request = RequestFactory().get("/")

        response = proxy_tile(request, 1, 2, 3)

        headers = get.call_args.kwargs["headers"]
        self.assertEqual(headers["User-Agent"], "TPAM/1.0 (+https://github.com/prpfr3/TPAM)")
        self.assertEqual(headers["Referer"], request.build_absolute_uri("/"))
        self.assertEqual(response.content, b"tile")
