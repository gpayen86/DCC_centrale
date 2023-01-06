from Arduino import Arduino
import numpy as np
import time

import train_basic_functions as tbf


class AnalogChannel(Arduino):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_init_in = "ST? "
        self.message_init_out = "Arduino gestion analogic channels"

    def get_status(self):
        return self.send_message("ST? ")

    def set_power(self, power):
        """
        Set the value of the power to the channel (in %)

        :param power: power of the channel (0 - 100)

        :return:
        """
        power = power / 100 * 255
        if power < -255:
            power = -255
        if power > 255:
            power = 255
        msg = "RUN {0}".format(np.round(power))
        return self.send_message(msg)

    def set_stop(self):
        return self.send_message("STO")

    def get_flag_stop(self):
        return self.send_message("FS?")

    def get_power_value(self):
        """
        Return the value of the power (between 0 and 100)

        :return: value of the voltage of the channel
        :rtype: int
        """

        val_out = self.send_message("VA? ")
        if val_out is None:
            val_out = 0
        if not tbf.is_string_to_int(val_out):
            val_out = 0
        val_out = np.round(int(val_out)/255*100)
        return val_out

    def get_temperature(self):
        return self.send_message("TE? ")

    def get_humidity(self):
        return self.send_message("HU? ")


if __name__ == '__main__':
    con = AnalogChannel(label="test", port_com="COM9")
    con.connection_to_arduino()
    con.close_connection()
