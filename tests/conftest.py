"""Shared fixtures for the tests under tests/.

pytest loads this file by itself -- a test that declares a `base_url` or
`http_client` parameter gets it from here, with no import.

`http_client` deliberately does NOT follow redirects. Several endpoints are
specified as redirects (GET /api/links/pmb -> 302 with a Location header), and
a client that follows them would report 200 from the destination site, so the
test would pass while proving nothing about our own API.
"""

import os

import pytest
import requests

DEFAULT_BASE_URL = "http://localhost:5000/api"


@pytest.fixture(scope="session")
def base_url() -> str:
    """Where the API is, without a trailing slash.

    From ROUTEOPTIMIZER_API_BASE_URL, so CI can point the same tests at
    whatever host the workflow started (see S5_SETUP_COMMAND).
    """
    return os.environ.get("ROUTEOPTIMIZER_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


@pytest.fixture(scope="session")
def api_root(base_url: str) -> str:
    """The server root, i.e. base_url without the /api suffix -- /health and
    other top-level endpoints live there, not under /api."""
    return base_url[: -len("/api")] if base_url.endswith("/api") else base_url


@pytest.fixture
def http_client(base_url: str):
    """A requests.Session rooted at base_url that never follows redirects.

    Relative paths are resolved against base_url, so a test asks for
    "/links/pmb" rather than repeating the host.
    """

    class Client(requests.Session):
        def request(self, method, url, *args, **kwargs):  # noqa: D102
            if url.startswith("/"):
                url = f"{base_url}{url}"
            kwargs.setdefault("timeout", 30)
            kwargs.setdefault("allow_redirects", False)
            return super().request(method, url, *args, **kwargs)

    with Client() as client:
        yield client
