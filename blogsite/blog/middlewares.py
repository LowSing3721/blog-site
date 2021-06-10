import uuid

UID_KEY = 'uid'
DAY = 60 * 60 * 24


class UidMiddleware:
    """生成基于Cookie的用户UID"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = request.COOKIES.get(UID_KEY, uuid.uuid4().hex)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(UID_KEY, uid, max_age=DAY, httponly=True)
        return response
