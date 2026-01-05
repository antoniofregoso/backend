import typing

from strawberry.permission import BasePermission
from strawberry.types import Info
from Middleware.JWTManager import JWTManager

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
        authentication = request.headers.get("Authentication")

        if authentication:
            token = authentication.split("Bearer ")[1]
            try:
                JWTManager.verify_token(token)
                return True
            except Exception:
                return False            

        return False