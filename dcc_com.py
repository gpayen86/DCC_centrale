import serial
import time
import sys
import glob
from Arduino import Arduino


class DccCom(Arduino):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.f0_to_f4 = [0, 0, 0, 0, 0]
        self.f5_to_f8 = [0, 0, 0, 0]
        self.message_init_in = "<s>"
        self.message_init_out = "iDCC++ BASE STATION FOR ARDUINO UNO"

    def power_on(self):
        self.send_message("<1>")

    def power_off(self):
        self.send_message("<0>")

    def set_speed_train(self, speed_value, id_train=3, direction=1):
        if direction < 0:
            direction = 0
        if direction > 1:
            direction = 1
        direction = int(direction)

        if speed_value < 0:
            speed_value = 0
        if speed_value > 126:
            speed_value = 126
        speed_value = int(speed_value)

        msg = "<t 1 " + str(id_train) + " " + str(speed_value) + " " + str(direction) + ">"
        self.send_message(msg)

    def light_on(self, id_train):
        self.f0_to_f4[0] = 1
        self._apply_f0_f4(id_train)

    def light_off(self, id_train):
        self.f0_to_f4[0] = 0
        self._apply_f0_f4(id_train)

    def light_cab_on(self, id_train):
        self.f5_to_f8[0] = 1
        self._apply_f5_f8(id_train)

    def light_cab_off(self, id_train):
        self.f5_to_f8[0] = 0
        self._apply_f5_f8(id_train)

    def sound_klaxon(self, id_train):
        self.f0_to_f4[3] = 1
        self._apply_f0_f4(id_train)
        time.sleep(2)
        self.f0_to_f4[3] = 0
        self._apply_f0_f4(id_train)

    def _apply_f0_f4(self, id_train):
        val = 128 + self.f0_to_f4[0]*16 + self.f0_to_f4[1] + self.f0_to_f4[2]*2 + self.f0_to_f4[3]*4 + self.f0_to_f4[4]*8
        msg = "<f " + str(id_train) + " " + str(val) + ">"
        self.send_message(msg)

    def _apply_f5_f8(self, id_train):
        val = 176 + self.f5_to_f8[0] + self.f5_to_f8[1]*2 + self.f5_to_f8[2] * 4 + self.f5_to_f8[3] * 8
        msg = "<f " + str(id_train) + " " + str(val) + ">"
        self.send_message(msg)


if __name__ == '__main__':
    con = DccCom()
    con.connection_to_arduino()
    con.power_on()
    con.light_on(3)
    con.light_cab_on(3)
    time.sleep(5)
    con.sound_klaxon(3)
    con.power_off()
    con.close_connection()
