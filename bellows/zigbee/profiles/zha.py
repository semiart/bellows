import enum


PROFILE_ID = 260

class DeviceType(enum.IntEnum):
    # Generic
    ON_OFF_SWITCH = 0x0000
    LEVEL_CONTROL_SWITCH = 0x0001
    ON_OFF_OUTPUT = 0x0002
    LEVEL_CONTROLLABLE_OUTPUT = 0x0003
    SCENE_SELECTOR = 0x0004
    CONFIGURATION_TOOL = 0x0005
    REMOTE_CONTROL = 0x0006
    COMBINED_INTERFACE = 0x0007
    RANGE_EXTENDER = 0x0008
    MAIN_POWER_OUTLET = 0x0009
    DOOR_LOCK = 0x000A
    DOOR_LOCK_CONTROLLER = 0x000B
    SIMPLE_SENSOR = 0x000C
    CONSUMPTION_AWARENESS_DEVICE = 0x000D
    HOME_GATEWAY = 0x0050
    SMART_PLUG = 0x0051
    WHITE_GOODS = 0x0052
    METER_INTERFACE = 0x0053
    # Lighting
    ON_OFF_LIGHT = 0x0100
    DIMMABLE_LIGHT = 0x0101
    COLOR_DIMMABLE_LIGHT = 0x0102
    ON_OFF_LIGHT_SWITCH = 0x0103
    DIMMER_SWITCH = 0x0104
    COLOR_DIMMER_SWITCH = 0x0105
    LIGHT_SENSOR = 0x0106
    OCCUPANCY_SENSOR = 0x0107
    # Closure
    SHADE = 0x0200
    SHADE_CONTROLLER = 0x0201
    WINDOW_COVERING_DEVICE = 0x0202
    WINDOW_COVERING_CONTROLLER = 0x0203
    # HVAC
    HEATING_COOLING_UNIT = 0x0300
    THERMOSTAT = 0x0301
    TEMPERATURE_SENSOR = 0x0302
    PUMP = 0x0303
    PUMP_CONTROLLER = 0x0304
    PRESSURE_SENSOR = 0x0305
    FLOW_SENSOR = 0x0306
    MINI_SPLIT_AC = 0x0307
    # Intruder Alarm Systems
    IAS_CONTROL = 0x0400  # IAS Control and Indicating Equipment
    IAS_ANCILLARY_CONTROL = 0x0401  # IAS Ancillary Control Equipment
    IAS_ZONE = 0x0402
    IAS_WARNING_DEVICE = 0x0403


CLUSTERS = {
    # Generic
    DeviceType.ON_OFF_SWITCH: [0x0004, 0x0005, 0x0006],
    DeviceType.SMART_PLUG: [0x0004, 0x0005, 0x0006],
    # Lighting
    DeviceType.ON_OFF_LIGHT: [0x0004, 0x0005, 0x0006, 0x0008],
    DeviceType.DIMMABLE_LIGHT: [0x0004, 0x0005, 0x0006, 0x0008],
    DeviceType.COLOR_DIMMABLE_LIGHT: [0x0004, 0x0005, 0x0006, 0x0008, 0x0300],
    DeviceType.ON_OFF_LIGHT_SWITCH: [0x0004, 0x0005, 0x0006],
    DeviceType.DIMMER_SWITCH: [0x0004, 0x0005, 0x0006, 0x0008],
    DeviceType.COLOR_DIMMER_SWITCH: [0x0004, 0x0005, 0x0006, 0x0008, 0x0300],
}
