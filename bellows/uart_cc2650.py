import asyncio
import serial_asyncio
import binascii
from commands_cc2650 import COMMANDS, Message


class NcpUart(asyncio.Protocol):
    
    def __init__(self):
        super().__init__()
        self.transport = None
        # add init code here
        self._out_srsp_q = []
        self._out_callback_q = []

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        self.transport.serial.rts = False

    def data_received(self, data):
        '''
        input:
            data: date received
        output:
            none
        '''
        print('data received:', self._readable_hex(data))
        # check data integrity
        checksum = 0 
        data_len = len(data)
        for i in data[1:data_len-1]:
            checksum = checksum ^ i
        if checksum == data[data_len-1]:
            # data[0] = sof
            # data[1] = data length
            # data[2] = cmd0 (first 3bit is type of cmd)
            if (data[2] & 0xe0) == 0x60:
                self._handle_srsp(data)
            elif (data[2] & 0xe0) == 0x40:
                self._handle_callback(data)
            else:
                print('Unknow msg received: ', self._readable_hex(msg))
        else:
            print('checksum error: ', self._readable_hex(msg))

    def connection_lost(self, exc):
        self.transport.close()
        print('port closed')
        asyncio.get_event_loop().stop()

    @asyncio.coroutine
    def dispatch_sreq(self, msg):
        '''
        input: 
            msg: msg wrapped in binary format
        output: 
            srps msg
        '''
        fut = asyncio.Future()
        self.transport.write(msg)
        print('write msg: ', self._readable_hex(msg))
        self._out_srsp_q.append((msg, fut))
        try:
            result = yield from asyncio.wait_for(fut, timeout=5)
            print('srsp received: ', self._readable_hex(result))
            return result
        except asyncio.TimeoutError:
            print('uart timeout error')
            raise asyncio.TimeoutError

    @asyncio.coroutine
    def dispatch_sreq_callback(self, msg, callback, future):
        '''
        input: 
            msg: msg wrapped in binary format
            callback: callback command tuple
            future: future obj for callback function
        output:
            srsp msg
        '''
        fut = asyncio.Future()
        self.transport.write(msg)
        self._out_srsp_q.append((msg, fut))
        self._out_callback_q.append((callback, future))
        try:
            result = yield from asyncio.wait_for(fut, timeout=5)
            print('srsp received: ', self._readable_hex(result))
            return result
        except asyncio.TimeoutError:
            raise

    def _handle_srsp(self, data):
        # get sreq command from srsp 
        cmd = ((data[2] & 0x1f) + 0x20, data[3])
        _cmd = self._int2bin(cmd) 
        # get the list of msg
        _cmd_q = [i[0] for i in self._out_srsp_q]
        # find matching command in list
        ind = 0
        for i in _cmd_q:
            if i.index(_cmd) is -1:
                ind += 1
            else:
                break
        if ind is -1:
            print('cmd not in srsp queue: ', self._readable_hex(_cmd))
        else:
            # if there is a match, set the future result and remove it from the queue 
            self._out_srsp_q[ind][1].set_result(data)
            self._out_srsp_q.pop(ind)

    def _handle_callback(self, data):
        cmd = (data[2], data[3])
        cmd_q = [i[0] for i in self._out_callback_q]
        # find matching command in list
        ind = 0
        for i in cmd_q:
            if i.index(cmd) is -1:
                ind += 1
            else:
                break
        if ind is -1:
            print('cmd not in callback queue: ', self._readable_hex(cmd))
        else:
            # if there is a match, set the future result and remove it from the queue 
            self._out_callback_q[ind][1].set_result(data)
            self._out_callback_q.pop(ind)

    def _int2bin(self, data):
        return binascii.a2b_hex(''.join('{:02x}'.format(i) for i in data))

    def _readable_hex(self, data):
        return ''.join('\\x{:02x}'.format(i) for i in data)

def connect(loop, protocol=NcpUart, port='/dev/tty.usbmodemL1000991'):
    
    coro = serial_asyncio.create_serial_connection(
        loop,
        protocol,
        port,
        baudrate=115200
    )
    transport, protocol = loop.run_until_complete(coro)
    return protocol

def send_sreq(loop, protocol, msg):
    coro = protocol.dispatch_sreq(msg)
    result = loop.run_until_complete(coro)
    return result

def send_callback(loop, protocol, msg, callback, future):
    coro = protocol.dispatch_sreq_callback(msg, callback, future)
    result = loop.run_until_complete(future)
    return result

loop = asyncio.get_event_loop()
protocol = connect(loop)
msg, callback = Message(COMMANDS['SYS_PING']).wrap()
result = send_sreq(loop, protocol, msg)
loop.run_forever()
loop.close()


