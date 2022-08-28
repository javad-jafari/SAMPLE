from rest_framework.throttling import UserRateThrottle


class OtpRateThrottle(UserRateThrottle):

    scope = 'otp'
    THROTTLE_RATES = {
        'otp': '1/second',
    }
    