import os
import tempfile
from uuid import uuid4

from fastapi.testclient import TestClient

# Ensure app startup uses a writable test DB URL before importing settings/app.
TEST_DB_FILE = os.path.join(tempfile.gettempdir(), "fastapifour_test.db")
os.environ["DATABASE_URL"] = f"sqlite://{TEST_DB_FILE}"
os.environ["GENERATE_SCHEMAS"] = "true"

from app import app


def _unique_signup_payload() -> dict[str, str]:
    suffix = uuid4().hex[:10]
    return {
        "email": f"qa_{suffix}@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!",
        "nickname": f"user_{suffix[:6]}",
    }


def _assert_error_shape(body: dict) -> None:
    assert body.get("ok") is False
    assert isinstance(body.get("code"), str)
    assert isinstance(body.get("message"), str)
    assert "detail" in body


def test_auth_full_flow_signup_login_me_refresh_logout() -> None:
    with TestClient(app) as client:
        signup_payload = _unique_signup_payload()

        signup_res = client.post("/api/v1/auth/signup", json=signup_payload)
        assert signup_res.status_code == 201
        assert signup_res.json()["email"] == signup_payload["email"]

        login_res = client.post(
            "/api/v1/auth/login",
            json={"email": signup_payload["email"], "password": signup_payload["password"]},
        )
        assert login_res.status_code == 200
        login_body = login_res.json()
        assert "access_token" in login_body
        assert "refresh_token" in login_body
        assert "access_expires_at" in login_body
        assert "refresh_expires_at" in login_body
        assert "expires_in" in login_body
        assert "refresh_expires_in" in login_body
        assert login_body.get("token_type") == "bearer"

        access_token = login_body["access_token"]
        refresh_token = login_body["refresh_token"]
        auth_headers = {"Authorization": f"Bearer {access_token}"}

        me_res = client.get("/api/v1/auth/me", headers=auth_headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == signup_payload["email"]

        refresh_res = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_res.status_code == 200
        refresh_body = refresh_res.json()
        new_access_token = refresh_body["access_token"]
        new_refresh_token = refresh_body["refresh_token"]

        reuse_res = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert reuse_res.status_code == 401
        reuse_body = reuse_res.json()
        _assert_error_shape(reuse_body)
        assert reuse_body["code"] in {"AUTH_REFRESH_BLACKLIST", "AUTH_REFRESH_REUSED"}

        logout_res = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {new_access_token}"},
            json={"refresh_token": new_refresh_token},
        )
        assert logout_res.status_code == 200
        assert "로그아웃 처리 완료" in logout_res.json()["message"]

        me_after_logout_res = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {new_access_token}"},
        )
        assert me_after_logout_res.status_code == 401
        me_after_logout_body = me_after_logout_res.json()
        _assert_error_shape(me_after_logout_body)
        assert me_after_logout_body["code"] == "AUTH_TOKEN_INVALID"


def test_login_failure_returns_standard_error_shape() -> None:
    with TestClient(app) as client:
        signup_payload = _unique_signup_payload()
        signup_res = client.post("/api/v1/auth/signup", json=signup_payload)
        assert signup_res.status_code == 201

        bad_login_res = client.post(
            "/api/v1/auth/login",
            json={"email": signup_payload["email"], "password": "WrongPass123!"},
        )
        assert bad_login_res.status_code == 401
        bad_login_body = bad_login_res.json()
        _assert_error_shape(bad_login_body)
        assert bad_login_body["code"] == "AUTH_INVALID_CREDENTIALS"


def test_signup_validation_error_returns_standard_error_shape() -> None:
    with TestClient(app) as client:
        invalid_payload = _unique_signup_payload()
        invalid_payload["confirm_password"] = "Mismatch123!"

        invalid_res = client.post("/api/v1/auth/signup", json=invalid_payload)
        assert invalid_res.status_code == 422
        invalid_body = invalid_res.json()
        _assert_error_shape(invalid_body)
        assert invalid_body["code"] == "REQUEST_VALIDATION_ERROR"
