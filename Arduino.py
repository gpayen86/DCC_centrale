import serial
import time
import datetime

class Arduino:
    def __init__(self, **kwargs):
        self.baudrate = 115200
        self.timeout = 1
        self.serial_arduino = None
        self.flag_connected = False
        self.label = ""
        self.port_com = ""
        self.message_init_in = None
        self.message_init_out = None

        self._insert_kwargs_values(kwargs)

    def _insert_kwargs_values(self, kwargs):
        if "label" in kwargs:
            self.label = kwargs["label"]
        if "port_com" in kwargs:
            self.port_com = kwargs["port_com"]

    def _waiting_received_message(self, size=256):
        i_max = 10
        for i in range(i_max):
            time.sleep(0.05)
            data_encode = self.serial_arduino.read(size)
            data = data_encode.decode("utf-8")
            if len(data) > 0:
                return data
        if i == i_max - 1:
            return None

    def _print(self, msg):
        print("{}: Arduino {}: port {}: {}".format(datetime.datetime.now(), self.label, self.port_com, msg))

    def connection_to_arduino(self, size=16):
        self._print("begin connection_to_arduino")
        self.serial_arduino = serial.Serial(port=self.port_com, baudrate=self.baudrate,
                                            timeout=self.timeout)
        time.sleep(5)
        connection_enable = self.check_message_init()

        if connection_enable:
            self._print("Connection Enable")
        else:
            self._print("Connection impossible")
            self.close_connection()

    def send_message(self, msg, size=256):
        if self.serial_arduino is None:
            self._print("Impossible to send data: no connection")
            return None

        # Reset in and out message in buffer
        self.serial_arduino.reset_input_buffer()
        self.serial_arduino.reset_output_buffer()
        time.sleep(0.05)
        self._print(f"msg in: {msg}")
        self.serial_arduino.write(bytes(msg, 'utf-8'))
        data = self._waiting_received_message(size=size)
        self._print(f"msg out: {data}")
        return data

    def close_connection(self):
        if self.serial_arduino is not None:
            self.serial_arduino.close()
            self.serial_arduino = None
            self._print("Connection closed")

    def check_message_init(self):
        self._print("check_message_init")
        if self.message_init_in is None or self.message_init_out is None:
            self._print("message init in or out is None")
            return True

        rcv = self.send_message(self.message_init_in)
        if rcv is None:
            self._print("No message in return")
            return False
        if rcv.find(self.message_init_out) >= 0:
            self._print("Message init received correct: {}".format(self.message_init_out))
            return True
        else:
            self._print('Message init not correct')
            self._print('  In: {}'.format(self.message_init_in))
            self._print('  Out expected: {}'.format(self.message_init_out))
            self._print('  Out received: {}'.format(rcv))
            return False
