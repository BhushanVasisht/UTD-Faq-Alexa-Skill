# -*- coding: utf-8 -*-

import requests
from ask_sdk_model import IntentRequest
from typing import Union, Dict, List


def build_url(api_info):
    """Return a `request` compatible URL from api properties."""
    # type: (Dict, Dict) -> str
    return "http://{}/question".format(
        api_info["host"])


def http_post(url, payload):
    """Return a response JSON for a POST call from `request`."""
    # type: (str, Dict) -> Dict
    print("My data",payload,type(payload))
    response = requests.post(url=url, json=payload)
    if response.status_code < 200 or response.status_code >= 300:
        response.raise_for_status()
    return response.json()


def get_answer(data, api_info):
    """Return weather information for a city by calling API."""
    # type: (Dict, Dict) -> str, str, str
    url = build_url(api_info)

    response = http_post(url,data)
    answer = response["answer"]

    return answer


def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return request.intent.slots[slot_name].value
    except (AttributeError, ValueError, KeyError, IndexError):
        return None