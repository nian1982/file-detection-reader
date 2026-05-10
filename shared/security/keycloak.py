from jose import jwt
from jose.exceptions import JWTError
import requests
from fastapi import (HTTPException, status)
from shared.config.settings import settings

# KEYCLOAK_URL = "http://localhost:8080"
# REALM = "muhoco"

# ISSUER = (
#     f"{KEYCLOAK_URL}/realms/{REALM}"
# )

# JWKS_URL = (
#     f"{ISSUER}/protocol/openid-connect/certs"
# )

_jwks = None


def _get_jwks():

    global _jwks

    if _jwks is None:
        try:
            response = requests.get(settings.KEYCLOAK_JWKS_URL, timeout=10)

            response.raise_for_status()

            _jwks = response.json()

        except requests.RequestException:

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Keycloak unavailable"
            )

    return _jwks


def verify_token(token: str):

    try:
        header = jwt.get_unverified_header(token)
        jwks = _get_jwks()
        rsa_key = None

        for key in jwks["keys"]:

            if key["kid"] == header["kid"]:

                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

                break

        if not rsa_key:
            return None

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            issuer=settings.KEYCLOAK_ISSUER,
            options={
                "verify_aud": False,
                "verify_exp": True
            }
        )

        return payload

    except JWTError:
        return None