import threading


__request_dict = threading.local()


def get_request_dict():
    try:
        return __request_dict.context
    except AttributeError:
        __request_dict.context = {}
        return __request_dict.context


def clear_request_dict():
    __request_dict.context = {}
