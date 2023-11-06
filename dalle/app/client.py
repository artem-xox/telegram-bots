from dataclasses import dataclass
import json
from typing import List
import requests

from app import settings


@dataclass
class RequestPayload:
    model: str
    prompt: str
    n: int = 1
    size: str = settings.RESOLUTION_LOW


@dataclass
class ResponseData:
    revised_prompt: str
    url: str


@dataclass
class ResponsePayload:
    created: int
    data: List[ResponseData]

    @property
    def urls(self):
        return [d['url'] for d in self.data]


class OpenAIClient:
    API_BASE_URL = 'https://api.openai.com/v1'

    def __init__(self, api_key):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    def generate_image(self, payload: RequestPayload) -> ResponsePayload:
        url = f'{self.API_BASE_URL}/images/generations'
        response = requests.post(
            url, data=json.dumps(payload.__dict__), headers=self.headers
        )
        if not response.ok:
            raise Exception(f"OpenAI client error: {str(response.json().get('error'))}, status {response.status_code}")

        return self._parse_response(response.json())

    @staticmethod
    def _parse_response(response_json) -> ResponsePayload:
        return ResponsePayload(**response_json)
