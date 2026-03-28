
from security.userAuth import UserAuth

class SecurityContext:
    userAuth: UserAuth | None

    def __init__(self):
        self.userAuth = None
    def injectUserAuth(self, userAuth: UserAuth):
        self.userAuth = userAuth
    def clean(self):
        self.userAuth = None

def injectSecurityContext():
    context = None

    try:
        context = SecurityContext()
        yield context
    finally:
        print("cleaning security context")
        context.clean()

