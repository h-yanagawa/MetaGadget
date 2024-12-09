import re
from typing import Self

from switchbot_client.switchbot_base_client import SwitchBotClientProtocol
from switchbot_client.switchbot_models import SBDeviceStatusResponse, PlugMiniJPStatusBody, BotStatusBody, MeterProCO2StatusBody, MotionSensorStatusBody, StripLightStatusBody, ColorBulbStatusBody, HumidifierStatusBody, Hub2StatusBody, CirculatorFanStatusBody


class SwitchBotDeviceOpsMixin:
    """
    SwitchBotClientMixin provides methods to control SwitchBot devices.
    SwitchBotデバイスごとに固有の操作のfacadesを提供する
    """

    def _turn_on(self: SwitchBotClientProtocol, device_id: str):
        return self.commands(device_id, "turnOn")

    def _turn_off(self: SwitchBotClientProtocol, device_id: str):
        return self.commands(device_id, "turnOff")

    def _toggle(self: SwitchBotClientProtocol, device_id: str):
        return self.commands(device_id, "toggle")

    def _set_brightness(self: SwitchBotClientProtocol, device_id: str, brightness: int):
        assert 1 <= brightness <= 100, "Invalid brightness, should be 1-100"
        return self.commands(device_id, "setBrightness", parameter=brightness)

    def _set_color_temperature(self: SwitchBotClientProtocol, device_id: str, color_temperature: int):
        assert 2700 <= color_temperature <= 6500, "Invalid color temperature, should be 2700-6500"
        return self.commands(device_id, "setColorTemperature", parameter=color_temperature)

    def _set_color(self: SwitchBotClientProtocol, device_id: str, color: str):
        assert re.match(r"\d{1,3}:\d{1,3}:\d{1,3}", color), "Invalid color format, should be '{0-255}:{0-255}:{0-255}'"
        assert any(0 <= int(c) <= 255 for c in color.split(":")), "Invalid color value, should be 0-255)"
        return self.commands(device_id, "setColor", parameter=color)

    # Humidifier

    def humidifier_turn_on(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_on(device_id)

    def humidifier_set_mode(self: SwitchBotClientProtocol | Self, device_id: str, mode: str | int):
        assert mode == "auto" or 0 <= int(mode) <= 103, "Invalid mode, should be 'auto' or 0-103"
        return self.commands(device_id, "set", parameter=mode)

    def humidifier_turn_off(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_off(device_id)

    # Color Bulb

    def bulb_turn_on(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_on(device_id)

    def bulb_turn_off(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_off(device_id)

    def bulb_toggle(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._toggle(device_id)

    def bulb_set_brightness(self: SwitchBotClientProtocol | Self, device_id: str, brightness: int):
        return self._set_brightness(device_id, brightness)

    def bulb_set_color_temperature(self: SwitchBotClientProtocol | Self, device_id: str, color_temperature: int):
        return self._set_color_temperature(device_id, color_temperature)

    def bulb_set_color(self: SwitchBotClientProtocol | Self, device_id: str, color: str):
        return self._set_color(device_id, color)

    # Strip Light

    def strip_turn_on(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_on(device_id)

    def strip_turn_off(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_off(device_id)

    def strip_toggle(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._toggle(device_id)

    def strip_set_brightness(self: SwitchBotClientProtocol | Self, device_id: str, brightness: int):
        return self._set_brightness(device_id, brightness)

    def strip_set_color_temperature(self: SwitchBotClientProtocol | Self, device_id: str, color_temperature: int):
        return self._set_color_temperature(device_id, color_temperature)

    def strip_set_color(self: SwitchBotClientProtocol | Self, device_id: str, color: str):
        return self._set_color(device_id, color)

    # Smart Plug

    def plug_turn_on(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_on(device_id)

    def plug_turn_off(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_off(device_id)

    def plug_toggle(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._toggle(device_id)

    # SwitchBot Bot

    def bot_turn_on(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_on(device_id)

    def bot_turn_off(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_off(device_id)

    def bot_press(self: SwitchBotClientProtocol | Self, device_id: str):
        return self.commands(device_id, "press")

    # Circulator Fan

    def circulator_fan_turn_on(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_on(device_id)

    def circulator_fan_turn_off(self: SwitchBotClientProtocol | Self, device_id: str):
        return self._turn_off(device_id)

    def circulator_fan_set_night_light_mode(self: SwitchBotClientProtocol | Self, device_id: str, mode: str | int):
        assert mode in ("off", 1, 2), "Invalid mode, should be 'off' (off), 1 (bright), or 2 (dim)"
        return self.commands(device_id, "setNightLightMode", parameter=mode)

    def circulator_fan_set_wind_mode(self: SwitchBotClientProtocol | Self, device_id: str, mode: str):
        assert mode in ("direct", "natural", "sleep", "baby"), \
            "Invalid mode, should be 'direct', 'natural', 'sleep', or 'baby'"
        return self.commands(device_id, "setWindMode", parameter=mode)

    def circulator_fan_set_wind_speed(self: SwitchBotClientProtocol | Self, device_id: str, speed: int):
        assert 1 <= speed <= 100, "Invalid speed, should be between 1 and 100"
        return self.commands(device_id, "setWindSpeed", parameter=speed)

    # get device status

    def bot_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[BotStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[BotStatusBody])

    def meter_pro_co2_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[MeterProCO2StatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[MeterProCO2StatusBody])

    def motion_sensor_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[MotionSensorStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[MotionSensorStatusBody])

    def plug_mini_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[PlugMiniJPStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[PlugMiniJPStatusBody])

    def strip_light_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[StripLightStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[StripLightStatusBody])

    def color_bulb_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[ColorBulbStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[ColorBulbStatusBody])

    def humidifier_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[HumidifierStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[HumidifierStatusBody])

    def hub2_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[Hub2StatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[Hub2StatusBody])

    def circulator_fan_get_device_status(self: SwitchBotClientProtocol | Self, device_id: str) -> SBDeviceStatusResponse[CirculatorFanStatusBody]:
        return self._get_device_status_typed(device_id, SBDeviceStatusResponse[CirculatorFanStatusBody])

