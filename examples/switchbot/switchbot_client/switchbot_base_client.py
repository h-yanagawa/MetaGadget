import base64
import hashlib
import hmac
import time
import uuid
from typing import Protocol, Type

import httpx
from pydantic import BaseModel

from .switchbot_models import SBListDeviceResponse


class SwitchBotClientProtocol(Protocol):
    def list_devices(self) -> SBListDeviceResponse:
        pass

    def get_device_status(self, device_id: str):
        pass

    def _get_device_status_typed[T: BaseModel](self, device_id: str, cls: Type[T]) -> T:
        pass

    def commands(self, device_id: str, command: str, command_type: str = "command", parameter: str | int = "default"):
        pass

    def execute_scene(self, scene_id: str):
        pass

    def list_scenes(self):
        pass

class SwitchBotBaseClient(SwitchBotClientProtocol):
    def __init__(self, token: str, secret: str):
        self._token = token
        self._secret = secret
        self._api_url = "https://api.switch-bot.com/v1.1"

    def _generate_sign(self):
        token = self._token
        secret = self._secret
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        return token, t, nonce, sign

    def _generate_headers(self):
        token, t, nonce, sign = self._generate_sign()
        return {
            'Authorization': token,
            'Content-Type': 'application/json',
            'charset': 'utf8',
            't': str(t),
            'sign': str(sign, 'utf-8'),
            'nonce': str(nonce)
        }

    def list_devices(self) -> SBListDeviceResponse:
        res = httpx.get(f'{self._api_url}/devices', headers=self._generate_headers())
        return SBListDeviceResponse.model_validate(res.json())

    def get_device_status(self, device_id: str):
        res = httpx.get(f'{self._api_url}/devices/{device_id}/status', headers=self._generate_headers())
        return res.json()

    def _get_device_status_typed[T: BaseModel](self, device_id: str, cls: Type[T]) -> T:
        res = self.get_device_status(device_id)
        return cls.model_validate(res)

    def commands(self, device_id: str, command: str, command_type: str = "command", parameter: str | int = "default"):
        request_body = {
            "command_type": command_type,
            "command": command,
            "parameter": parameter
        }
        res = httpx.post(f'{self._api_url}/devices/{device_id}/commands', headers=self._generate_headers(), json=request_body)
        return res.json()

    def execute_scene(self, scene_id: str):
        res = httpx.post(f'{self._api_url}/scenes/{scene_id}/execute', headers=self._generate_headers())
        return res.json()

    def list_scenes(self):
        res = httpx.get(f'{self._api_url}/scenes', headers=self._generate_headers())
        return res.json()

