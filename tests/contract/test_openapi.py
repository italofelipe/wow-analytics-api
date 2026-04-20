"""
Schemathesis contract tests — property-based fuzzing against the OpenAPI spec.

Runs without a real database: the FastAPI app is tested via ASGI transport,
endpoints that require DB return 503 which Schemathesis is configured to accept.
"""

import pytest
import schemathesis
from fastapi.testclient import TestClient

from api.main import app

# Load schema directly from the ASGI app (no network call needed)
schema = schemathesis.from_asgi("/openapi.json", app)


@schema.parametrize()
def test_api_contracts(case):
    """
    Schemathesis generates valid and invalid inputs for every endpoint,
    verifying the API never returns a 5xx for valid inputs.
    """
    with TestClient(app) as client:
        response = case.call_asgi(client)
        # 5xx on valid input = contract violation
        # 503 is allowed (DB not available in unit CI)
        case.validate_response(response, checks=(no_server_error,))


def no_server_error(response, case):
    if response.status_code == 503:
        return  # DB unavailable in CI — acceptable
    assert response.status_code < 500, (
        f"Server error {response.status_code} on {case.method} {case.path}\n"
        f"Response: {response.text[:500]}"
    )
