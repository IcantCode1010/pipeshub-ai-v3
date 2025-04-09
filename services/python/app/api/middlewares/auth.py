import os
from fastapi import HTTPException, status, Request
from jose import JWTError, jwt
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from app.config.configuration_service import ConfigurationService, config_node_constants

async def get_config_service(request: Request) -> ConfigurationService:    
    container = request.app.container
    config_service = container.config_service()
    return config_service

# Authentication logic
@inject
async def isJwtTokenValid(request: Request, config_service: ConfigurationService = Depends(get_config_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        secret_keys = await config_service.get_config(config_node_constants.SECRET_KEYS.value)
        jwt_secret = secret_keys.get('jwtSecret')
        
        algorithm = os.environ.get("JWT_ALGORITHM", "HS256")
        if not jwt_secret:
            raise ValueError("Missing SECRET_KEY in environment variables")

        # Get the Authorization header
        authorization: str = request.headers.get("Authorization")

        if not authorization or not authorization.startswith("Bearer "):
            raise credentials_exception

        # Extract the token
        token = authorization.split("Bearer ")[1]
        if not token:
            raise credentials_exception

        # Decode the JWT
        payload = jwt.decode(token, jwt_secret, algorithms=[algorithm])
        payload["user"] = token
        return payload
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

# Dependency for injecting authentication
async def authMiddleware(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
    try:# Validate the token
        payload = await isJwtTokenValid(request)
        # Attach the authenticated user information to the request state
        request.state.user = payload
    except HTTPException as e:
        raise e  # Re-raise HTTPException instances
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise credentials_exception
    return request
