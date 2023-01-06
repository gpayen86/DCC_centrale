import serial.tools.list_ports
import numpy as np
import plotly.graph_objs as go
import Arduino


def button_connection_auto(n_clicks_auto: int, n_clicks_dcc: int, n_clicks_analog: int, arduino_dcc: Arduino,
                           arduino_analog: Arduino):
    # Update n_clicks buttons
    n_clicks_dcc = n_clicks_dcc + 1
    n_clicks_analog = n_clicks_analog + 1

    # Research port COM
    list_port_com_available = []
    for comport in serial.tools.list_ports.comports():
        if len(comport.description) > 7 and comport.description[0:7] == "Arduino":
            list_port_com_available.append(comport.device)

    # Search DCC port
    flag_connection = False
    for port_com in list_port_com_available:
        arduino_dcc.port_com = port_com
        arduino_dcc.connection_to_arduino()
        if arduino_dcc.serial_arduino is not None:
            if arduino_dcc.check_message_init():
                flag_connection = True
                break
    if not flag_connection:
        arduino_dcc.port_com = None
    arduino_dcc.close_connection()

    # Search Analog port
    flag_connection = False
    for port_com in list_port_com_available:
        arduino_analog.port_com = port_com
        arduino_analog.connection_to_arduino()
        if arduino_analog.serial_arduino is not None:
            if arduino_analog.check_message_init():
                flag_connection = True
                break
    if not flag_connection:
        arduino_analog.port_com = None
    arduino_analog.close_connection()

    return [list_port_com_available, list_port_com_available,
            arduino_dcc.port_com, arduino_analog.port_com, n_clicks_dcc, n_clicks_analog]


def graph_map(map_data, status_connection_analog, status_connection_dcc, power_channel_analog, status_power_dcc):
    fig = go.Figure()
    status_list = [status_connection_dcc, status_connection_analog]
    power_list = [status_power_dcc, 0]
    if float(power_channel_analog) > 0:
        power_list[1] = 1
    for i in range(len(map_data)):
        data = map_data[i]
        status = status_list[i]
        power = power_list[i]
        if status == 0:
            dash_option = 'dot'
        else:
            dash_option = 'dash'
        if power == 1:
            dash_option = None
        fig.add_trace(go.Scatter(x=data['x'], y=data["y"], name=data["name"], mode='lines',
                                 line=dict(dash=dash_option)))
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    return fig


def connection_arduino(n_click, arduino, port_com):
    if n_click == 0:
        return 0
    else:
        arduino.port_com = port_com
        if arduino.serial_arduino is None:
            arduino.connection_to_arduino()
            if arduino.check_message_init():
                return 1
            else:
                return 0
        else:
            arduino.close_connection()
            return 0
