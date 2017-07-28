import asyncio
import serial_asyncio


class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False
        transport.write(b'\xFE\x00\x21\x01\x20')

    def data_received(self, data):
        print('data received:', ''.join('\\x{:02x}'.format(c) for c in data))
        self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/tty.usbmodemL1000991', baudrate=115200)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()