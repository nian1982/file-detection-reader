from jose import jwt
from jose.exceptions import JWTError
import requests
from fastapi import (Depends, HTTPException, status)
from fastapi.security import (HTTPBearer, HTTPAuthorizationCredentials)
from shared.config.settings import settings

security = HTTPBearer()
_jwks = None


def _get_jwks():
    global _jwks

    if _jwks is None:
        try:
            response = requests.get(
                settings.KEYCLOAK_JWKS_URL,
                timeout=10
            )

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

        decode_options = {
            "verify_exp": True,
            "verify_aud": settings.KEYCLOAK_VERIFY_AUDIENCE
        }

        decode_kwargs = {
            "token": token,
            "key": rsa_key,
            "algorithms": ["RS256"],
            "issuer": settings.KEYCLOAK_ISSUER,
            "options": decode_options
        }

        if settings.KEYCLOAK_VERIFY_AUDIENCE:

            decode_kwargs["audience"] = (
                settings.KEYCLOAK_CLIENT_ID
            )

        payload = jwt.decode(
            **decode_kwargs
        )

        return payload

    except JWTError:
        return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    return payload


def require_client_role(client_id: str, required_role: str):

    def role_checker(payload: dict = Depends(get_current_user)):
        resource_access = payload.get("resource_access", {})

        client_roles = (
            resource_access
            .get(client_id, {})
            .get("roles", [])
        )

        if required_role not in client_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Se requiere el rol '{required_role}' "
                    f"para el cliente '{client_id}'"
                )
            )

        return payload

    return role_checker