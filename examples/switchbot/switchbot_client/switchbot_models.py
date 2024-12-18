from typing import TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class ListDeviceBody(BaseModel):
    deviceId: str  # Device ID
    deviceName: str  # Device name
    deviceType: str  # Device type, e.g., MeterPro(CO2)
    hubDeviceId: str  # Device's parent hub ID
    # enabledCloudService: bool  # Cloud service status

class ListDeviceBodyRoot(BaseModel):
    deviceList: list[ListDeviceBody]
    # infraredRemoteList: list[ListDeviceBody]

class SBListDeviceResponse(BaseModel):
    statusCode: int  # HTTP status code of the response
    message: str  # Response message or error description
    body: ListDeviceBodyRoot


class SBDeviceStatusResponse[T](BaseModel):
    statusCode: int  # HTTP status code of the response
    message: str  # Response message or error description
    body: T  # Body of the response containing device-specific information


class MeterProCO2StatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., MeterPro(CO2)
    hubDeviceId: str  # Device's parent hub ID
    battery: int  # Current battery level, from 0 to 100
    version: str  # Current firmware version, e.g., V4.2
    temperature: float  # Temperature in Celsius
    humidity: int  # Humidity percentage
    CO2: int  # CO2 concentration in parts per million (ppm), from 0 to 9999


class BotStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Bot
    power: str  # ON/OFF state
    battery: int  # Current battery level, from 0 to 100
    version: str  # Current firmware version, e.g., V6.3
    deviceMode: str  # Mode: pressMode, switchMode, or customizeMode
    hubDeviceId: str  # Device's parent Hub ID


class MotionSensorStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Motion Sensor
    hubDeviceId: str  # Device's parent Hub ID
    battery: int  # The current battery level, from 0 to 100
    version: str  # The current firmware version, e.g., V4.2
    moveDetected: bool  # Determines if motion is detected
    brightness: str  # The ambient brightness, bright or dim


class PlugMiniJPStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Plug Mini (JP)
    hubDeviceId: str  # Device's parent Hub ID
    voltage: float  # The voltage of the device, measured in Volts
    version: str  # The current BLE and Wi-Fi firmware version, e.g., V3.1-6.3
    weight: float  # The power consumed in a day, measured in Watts
    electricityOfDay: int  # The duration used in a day, measured in minutes
    electricCurrent: float  # The current of the device, measured in Amps


class StripLightStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Strip Light
    hubDeviceId: str  # Device's parent Hub ID
    power: str  # ON/OFF state
    version: str  # The current BLE and Wi-Fi firmware version, e.g., V3.1-6.3
    brightness: int  # The brightness, range from 1 to 100
    color: str  # The color value, RGB "255:255:255"


class ColorBulbStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Color Bulb
    hubDeviceId: str  # Device's parent Hub ID
    power: str  # ON/OFF state
    brightness: int  # Brightness value, range from 1 to 100
    version: str  # Current BLE and Wi-Fi firmware version, e.g., V3.1-6.3
    color: str  # RGB color value, e.g., "255:255:255"
    colorTemperature: int  # Color temperature, range from 2700 to 6500


class HumidifierStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Humidifier
    power: str  # ON/OFF state
    humidity: int  # Humidity percentage
    temperature: float  # Temperature in Celsius
    nebulizationEfficiency: int  # Atomization efficiency percentage
    auto: bool  # Auto Mode status
    childLock: bool  # Child lock status
    sound: bool  # Mute status
    lackWater: bool  # Empty water tank status


class Hub2StatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceType: str  # Device type, e.g., Hub 2
    hubDeviceId: str  # Equivalent to device ID
    temperature: float  # Temperature in Celsius
    lightLevel: int  # Level of ambient light, range from 1 to 20
    version: str  # Current firmware version, e.g., V4.2
    humidity: int  # Humidity percentage


class CirculatorFanStatusBody(BaseModel):
    deviceId: str  # Device ID
    deviceName: str  # Device name
    deviceType: str  # Device type, e.g., Circulator Fan
    mode: str  # Fan mode: direct, natural, sleep, or baby
    version: str  # Current firmware version, e.g., V4.2
    power: str  # ON/OFF state
    nightStatus: int  # Nightlight status, off or mode 1/2
    oscillation: str  # Horizontal oscillation state
    verticalOscillation: str  # Vertical oscillation state
    fanSpeed: int  # Fan speed, range from 1 to 100
