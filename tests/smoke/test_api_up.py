"""One test whose only job is to prove the CI chain works end to end.

It passes only if: GitHub Actions ran the workflow, S5_SETUP_COMMAND brought the
API up with docker compose, and pytest reached /health -- which the API answers
only once its database and Redis are reachable too (Program.cs registers
AddDbContextCheck and AddRedis).

Deliberately does NOT skip when the API is unreachable. A skip would turn a
broken pipeline into a green run, which is worse than a red one. Real
S5-generated tests may skip; this one must not, because "the API is up" is the
single thing it exists to assert.

Delete it once S5 delivers real tests under tests/<TICKET>/.
"""

import os

import pytest
import requests

BASE_URL = os.environ.get("ROUTEOPTIMIZER_API_BASE_URL", "http://localhost:5000/api")

# The health endpoint is mapped at the root, not under /api.
HEALTH_URL = BASE_URL.rsplit("/api", 1)[0] + "/health"


@pytest.mark.happyPath
@pytest.mark.integrationTest
@pytest.mark.httpApi
def test_health_endpoint_answers_200():
    response = requests.get(HEALTH_URL, timeout=30, allow_redirects=False)
    assert response.status_code == 200, (
        f"{HEALTH_URL} answered {response.status_code}: {response.text[:200]}"
    )
