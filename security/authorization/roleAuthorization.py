from enum import Enum
from typing import Set

from fastapi import HTTPException, Depends

from security.SecurityContext import injectSecurityContext, SecurityContext


def _hasAnyRole(requiredRole: Set[str], userRole: Set[str]):
    return userRole.issubset(requiredRole)

def _hasAllRoles(requiredRole: Set[str], userRole: Set[str]):
    return userRole == requiredRole


def authorizeAnyRole(requiredRoles: Set[str]):

    def checker(securityContext: SecurityContext = Depends(injectSecurityContext)):
        userRole = securityContext.userAuth.roles

        if not _hasAnyRole(requiredRoles, userRole):
            raise HTTPException(status_code=403, detail="forbidden")

    return checker


def authorizeWithAllRoles(requiredRoles: Set[str]):

    def checker(securityContext: SecurityContext = Depends(injectSecurityContext)):
        userRole = securityContext.userAuth.roles

        if not _hasAllRoles(requiredRoles, userRole):
            raise HTTPException(status_code=403, detail="forbidden")

    return checker