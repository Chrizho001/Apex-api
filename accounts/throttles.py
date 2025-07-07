from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class PasswordResetThrottle(SimpleRateThrottle):
    scope = 'password_reset'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class RequestPasswordResetThrottle(SimpleRateThrottle):
    scope = 'request_password_reset'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class OTPRequestThrottle(SimpleRateThrottle):
    scope = 'otp_request'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class OTPVerifyThrottle(SimpleRateThrottle):
    scope = 'otp_verify'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
