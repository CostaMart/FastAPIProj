from typing import Set

from fastapi import Depends

from exceptions.customExceptions import ForbiddenException
from security.Role import Role
from security.SecurityContext import injectSecurityContext, SecurityContext


def _hasAnyRole(requiredRole: Set[Role], userRole: Set[Role]):
    return userRole.issubset(requiredRole)

def _hasAllRoles(requiredRole: Set[Role], userRole: Set[Role]):
    return userRole == requiredRole


def authorizeAnyRole(requiredRoles: Set[Role]):

    def checker(securityContext: SecurityContext = Depends(injectSecurityContext)):
        userRole = securityContext.userAuth.roles

        if not _hasAnyRole(requiredRoles, userRole):
            raise ForbiddenException(cause = "Insufficient permissions")

    return checker


def authorizeWithAllRoles(requiredRoles: Set[Role]):

    def checker(securityContext: SecurityContext = Depends(injectSecurityContext)):
        userRole = securityContext.userAuth.roles

        if not _hasAllRoles(requiredRoles, userRole):
            raise ForbiddenException(cause = "Insufficient permissions")

    return checker