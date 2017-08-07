
import struct
import binascii as ba


class Message:
    def __init__(self, cmd=(), data=()):
        '''
        input:
            cmd: cmd and callback tuple
            data: data tuple to be sent
        '''
        self._sof = 0xfe
        self._cmd = cmd[0]
        self._callback = cmd[1]
        self._data = data
        self._data_len = len(data)
        
    def wrap(self):
        checksum = self._data_len
        for i in self._cmd:
            checksum = checksum ^ i

        for i in self._data:
            checksum = checksum ^ i
        frame = (self._sof,) + (self._data_len,) + self._cmd + self._data + (checksum,)
        return ba.a2b_hex(''.join('{:02x}'.format(i) for i in frame)), self._callback


COMMANDS = {
    '''
    command structure: ((cmd_id), (callback_id))
    if callback_id is (), there will be no callback
    '''
    # register an application's endpoint
    'AF_REGISTER':((0x24, 0x00),()),
    'AF_DATA_REQUEST':(0x24, 0x01),
    'AF_DATA_REQUEST_EXT':(),
    'AF_DATA_REQUEST_SRC_RTG':(),
    'AF_INTER_PAN_CTL':(),
    'AF_DATA_STORE':(),
    'AF_DATA_RETRIEVE':(),
    'AF_APSF_CONFIG_SET':(),
    
    # AF CALLBACKS
    'AF_DATA_CONFIRM':(0x44, 0x80),
    'AF_REFLECT_ERROR':(),
    'AF_INCOMING_MSG':(0x44, 0x81),
    'AF_INCOMING_MSG_EXT':(),

    # APP COMMANDS
    'APP_MSG':(0x29, 0x00),
    'APP_USER_TEST':(),

    # DEBUG COMMANDS
    # TO BE ADDED

    # MAC COMMANDS
    'MAC_RESET_REQ':(),
    'MAC_INIT':(),
    'MAC_START_REQ':(),
    'MAC_SYNC_REQ':(),
    'MAC_DATA_REQ':(),
    'MAC_ASSOCIATE_REQ':(),
    'MAC_ASSOCIATE_RSP':(),
    'MAC_DISASSOCIATE_REQ':(),
    'MAG_GET_REQ':(),
    'MAC_SET_REQ':(),
    'MAC_SCAN_REQ':(),
    'MAC_ORPHAN_RSP':(),
    'MAC_POLL_REQ':(),
    'MAC_PURGE_REQ':(),
    'MAC_SET_RX_GAIN_REQ':(),

    # MAC CALLBACKS
    'MAC_SYNC_LOSS_IND':(),
    'MAC_ASSOCIATE_IND':(),
    'MAC_BEACON_NOTIFY_IND':(),
    'MAC_DATA_CNF':(),
    'MAC_DATA_IND':(),
    'MAC_DISASSOCIATE_IND':(),
    'MAC_DISASSOCIATE_CNF':(),
    'MAC_ORPHAN_IND':(),
    'MAC_POLL_CNF':(),
    'MAC_SCAN_CNF':(),
    'MAC_COMM_STATUS_IND':(),
    'MAC_START_CNF':(),
    'MAC_RX_ENABLE_CNF':(),
    'MAC_PURGE_CNF':(),

    'ZB_SYSTEM_RESET':(0x46, 0x09),
    'ZB_START_REQUEST':(0x26, 0x00),
    'ZB_PERMIT_JOINING_REQUEST':(0x26, 0x08),
    'ZB_BIND_DEVICE':(0x26, 0x01),
    'ZB_ALLOW_BIND':(0x26, 0x02),
    'ZB_SEND_DATA_REQUEST':(0x26, 0x03),
    'ZB_READ_CONFIGURATION':(0x26, 0x04),
    'ZB_WRITE_CONFIGRATION':(0x26, 0x05),
    'ZB_GET_DEVICE_INFO':(0x26, 0x06),
    'ZB_FIND_DEVICE_REQUEST':(0x26, 0x07),

    # SIMPLE API CALLBACKS
    'ZB_START_CONFIRM':(0x46, 0x80),
    'ZB_BIND_CONFIRM':(0x46, 0x81),
    'ZB_ALLOW_BIND_CONFIRM':(0x46, 0x82),
    'ZB_SEND_DATA_CONFIRM':(0x46, 0x83),
    'ZB_RECEIVE_DATA_INDICATION':(0x46, 0x87),
    'ZB_FIND_DEVICE_CONFIRM':(0x46, 0x85),

    # SYS COMMANDS
    'SYS_RESET_REQ':(),
    'SYS_PING':((0x21, 0x01), ()),
    'SYS_VERSION':((0x21, 0x02), ()),
    'SYS_SET_EXTADDR':((0x21, 0x03), ()),
    'SYS_GET_EXTADDR':(),
    'SYS_RAM_READ':(),
    'SYS_RAM_WRITE':(),
    'SYS_OSAL_NV_READ':((0x21, 0x08), ()),
    'SYS_OSAL_NV_WRITE':((0x21, 0x09), ()),
    'SYS_OSAL_NV_DELTE':(),
    'SYS_OSAL_NV_LENGTH':(),
    'SYS_OSAL_START_TIMER':(),
    'SYS_OSAL_STOP_TIMER':(),
    'SYS_RANDOM':(),
    'SYS_ADC_READ':(),
    'SYS_GPIO':(),
    'SYS_STACK_TUNE':(),
    'SYS_SET_TIME':(),
    'SYS_GET_TIME':(),
    'SYS_SET_TX_POWER':(),
    'SYS_ZDIAGS_INIT_STATS':(),
    'SYS_ZGIAGS_CLEAR_STATS':(),
    'SYS_ZDIAGS_GET_STATS':(),
    'SYS_ZDIAGS_RESTORE_STATS_NV':(),
    'SYS_ZDIAGS_SAVE_STATS_TO_NV':(),
    'SYS_NV_CREATE':(),
    'SYS_NV_LENGTH':(),
    'SYS_NV_READ':(),
    'SYS_NV_WRITE':(),
    'SYS_NV_UPDATE':(),
    'SYS_NV_COMPACT':(),
    'SYS_OSAL_NV_READ_EXT':(),
    'SYS_OSAL_NV_WRITE_EXT':(),

    # SYS CALLBACKS
    'SYS_RESET_IND':(),
    'SYS_OSAL_TIMER_EXPIRED':(),

    # UTIL COMMANDS
    'UTIL_GET_DEVICE_INFO':((0X27, 0X00), ()),
    'UTIL_GET_NV_INFO':((0X27, 0X01), ()),
    'UTIL_SET_PANID':((0X27, 0X02), ()),
    'UTIL_SET_CHANNELS':((0X27, 0X03), ()),
    'UTIL_SET_SECLEVEL':((0X27, 0X04), ()),
    'UTIL_SET_PRECFGKEY':((0X27, 0X05), ()),
    'UTIL_CALLBACK_SUB_CMD':((0X27, 0X06), ()),
    'UTIL_KEY_EVENT':((0X27, 0X07), ()),
    'UTIL_TIME_ALIVE':(),
    'UTIL_LED_CONTROL':(),
    'UTIL_LOOPBACK':(),
    'UTIL_DATA_REQ':((0X27, 0X11), ()),
    'UTIL_SRC_MATCH_ENABLE':(),
    'UTIL_SRC_MATCH_ADD_ENTRY':(),
    'UTIL_SRC_MATCH_DEL_ENTRY':(),
    'UTIL_SRC_MATCH_CHECK_SRC_ADDR':(),
    'UTIL_SRC_MATCH_ACK_ALL_PENDING':(),
    'UTIL_SRC_MATCH_CHECK_ALL_PENDING':(),
    'UTIL_ADDRMGR_EXT_ADDR_LOOKUP':(),
    'UTIL_ADDRMGR_NWK_ADDR_LOOKUP':(),
    'UTIL_APSME_LINK_KEY_DATA_GET':(),
    'UTIL_APSME_LINK_KEY_NV_ID_GET':(),
    'UTIL_APSME_REQUEST_KEY_CMD':(),
    'UTIL_ASSOC_COUNT':((0X27, 0X48), ()),
    'UTIL_ASSOC_FIND_DEVICE':((0X27, 0X49), ()),
    'UTIL_ASSOC_GET_WITH_ADDRESS':((0X27, 0X4A), ()),
    'UTIL_BIND_ADD_ENTRY':((0X27, 0X4D), ()),
    'UTIL_ZCL_KEY_EST_INIT_EST':((0X27, 0X80), ()),
    'UTIL_ZCL_KEY_EST_SIGN':((0X27, 0X81), ()),
    'UTIL_SRNG_GEN':((0X27, 0X4C), ()),

    # UTIL CALLBACKS
    'UTIL_SYNC_REQ':(0X47, 0XE0),
    'UTIL_ZCL_KEY_ESTABLISH_IND':(0X47, 0XE1),

    # ZDO COMMANDS
    'ZDO_NWK_ADDR_REQ':((0X25, 0X00), (0X45, 0X80)),
    'ZDO_IEEE_ADDR_REQ':((0X25, 0X01), (0X45, 0X81)),
    'ZDO_NODE_DESC_REQ':((0X25, 0X02), (0X45, 0X82)),
    'ZDO_POWER_DESC_REQ':((0X25, 0X03), (0X45, 0X83)),
    'ZDO_SIMPLE_DESC_REQ':((0X25, 0X04), (0X45, 0X84)),
    'ZDO_ACTIVE_EP_REQ':((0X25, 0X05), (0X45, 0X85)),
    'ZDO_MATCH_DESC_REQ':((0X25, 0X06), (0X45, 0X86)),
    'ZDO_COMPLEX_DESC_REQ':((0X25, 0X07), (0X45, 0X87)),
    'ZDO_USER_DESC_REQ':((0X25, 0X08), (0X45, 0X88)),
    'ZDO_END_DEVICE_ANNCE':((0X25, 0X0A), (0X45, 0XC1)),
    'ZDO_USER_DESC_SET':(0X25, 0X0B),
    'ZDO_SERVER_DISC_REQ':((0X25, 0X0C), (0X45, 0X8A)),
    'ZDO_END_DEVICE_BIND_REQ':((0X25, 0X20), (0X45, 0X0A)),
    'ZDO_BIND_REQ':((0X25, 0X21), (0X45, 0XA1)),
    'ZDO_UNBIND_REQ':((0X25, 0X22), (0X45, 0XA2)),
    'ZDO_MGMT_NWK_DISC_REQ':((0X25, 0X30), (0X45, 0XB0)),
    'ZDO_MGMT_LQI_REQ':((0X25, 0X31),(0X45, 0XB1)),
    'ZDO_MGMT_RTG_REQ':((0X25, 0X32),(0X45, 0XB2)),
    'ZDO_MGMT_BIND_REQ':((0X25, 0X33),(0X45, 0XB3)),
    'ZDO_MGMT_LEAVE_REQ':((0X25, 0X34),(0X45, 0XB4)),
    'ZDO_MGMT_DIRECT_JOIN_REQ':((0X25, 0X35), (0X45, 0XB5)),
    'ZOD_MGMT_PERMT_JOIN_REQ':((0X25, 0X36), (0X45, 0XB6)),
    'ZDO_MGMT_NWK_UPDATE_REQ':(0X25, 0X37),
    'ZDO_MSG_CB_REGSITER':(0X25, 0X3E),
    'ZDO_MSG_CB_REMOVE':(0X25, 0X3F),
    'ZDO_STARTUP_FROM_APP':(0X25, 0X40),
    'ZDO_AUTO_FIND_DESTINATION':(0X25, 0X45),
    'ZDO_SET_LINK_KEY':(0X25, 0X23),
    'ZDO_REMOVE_LINK_KEY':(0X25, 0X24),
    'ZDO_GET_LINK_KEY':(0X25, 0X25),
    'ZDO_NWK_DISCOVERY_REQ':(0X25, 0X26),
    'ZDO_JOIN_REQ':(0X25, 0X27),
    'ZDO_SET_REJOIN_PARAMETERS':(0X25, 0X26),
    'ZDO_SEC_ADD_LINK_KEY':(0X25, 0X42),
    'ZDO_SEC_ENTRY_LOOKUP_EXT':(),
    'ZDO_SEC_DEVICE_REMOVE':(0X25, 0X44),
    'ZDO_EXT_ROUTE_DISC':(),
    'ZDO_EXT_ROUTE_CHECK':(),
    'ZDO_EXT_REMOVE_GROUP':(),
    'ZDO_EXT_REMOVE_ALL_GROUP':(),
    'ZDO_EXT_FIND_ALL_GROUPS_ENDPOINT':(),
    'ZDO_EXT_FIND_GROUP':(),
    'ZDO_EXT_ADD_GROUP':(),
    'ZDO_EXT_COUNT_ALL_GROUP':(),
    'ZDO_EXT_RX_IDLE':(),
    'ZDO_EXT_UPDATE_NWK_KEY':(),
    'ZDO_EXT_SWITCH_NWK_KEY':(),
    'ZDO_EXT_NWK_INFO':(),
    'ZDO_EXT_SEC_APS_REMOVE_REQ':(),
    'ZDO_FORCE_CONCENTRATOR_CHANGE':(),
    'ZDO_EXT_SET_PARAMS':(),

    # ZDO CALLBACKS
    'ZDO_USER_DESC_CONF':(0X45, 0X89),
    'ZDO_MATCH_DESC_RSP_SENT':(0X45, 0XC2),
    'ZDO_STATUS_ERROR_RSP':(0X45, 0XC3),
    'ZDO_SRC_RTG_IND':(0X45, 0XC4),
    'ZDO_BEACON_NOTIFY_IND':(0X45, 0XC5),
    'ZDO_JOIN_CNF':(0X45, 0XC6),
    'ZDO_NWK_DISCOVERY_CNF':(0X45, 0XC7),
    'ZDO_LEAVE_IND':(0X45, 0XC9),
    'ZDO_MSG_CB_INCOMING':(0X45, 0XFF),
}