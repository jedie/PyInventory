from inventory.request_dict import clear_request_dict, get_request_dict


class RequestDictMiddleware:
    """
    Make the "current user" information avaiable everywhere via threading.local()
    Access e.g.:
        user = get_request_dict()['user']
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        get_request_dict().update(user=request.user)

        response = self.get_response(request)

        clear_request_dict()

        return response
