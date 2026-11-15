import ssl

import requests
import urllib3

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()
_original_request = requests.Session.request


def _unverified_request(self, method, url, **kwargs):
    kwargs.setdefault("verify", False)
    return _original_request(self, method, url, **kwargs)


requests.Session.request = _unverified_request