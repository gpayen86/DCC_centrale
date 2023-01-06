import time
import numpy as np

import main_functions as mf

from dash import Dash, dcc, html, Input, Output, State

from dcc_com import DccCom
from analogic_channel import AnalogChannel

PORT_COM_DCC = "COM10"
PORT_COM_ANALOG = "COM11"
colors = {
    'background_title': '#62c2fc',
    'text': '#7FDBFF'
}
VERSION = "1.1"

ARDUINO = [DccCom(label="dcc"), AnalogChannel(label="analog")]

MAP_DATA = [
    {
     'y': np.array([22, 22, 66, 111, 111, 65, 22, 94]),
     'x': np.array([52, 160, 206, 160, 73, 27, 52, 144]),
     'name': "Numérique"},
    {'y': np.array([54, 76, 123, 123, 77, 54, 8, 8, 54, 86, 135, 135]),
     'x': np.array([222, 222, 170, 64, 16, 16, 52, 180, 222, 232, 170, 70]),
     'name': 'Analogique'},
]

app = Dash(__name__)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Centrale de controle",
                style={
                    'textAlign': 'center',
                }),
        html.Div("Par Guillaume"),
        html.Div(f"Version : {VERSION}")
    ],
        style={
            'backgroundColor': colors["background_title"]
        }
    ),
    # Connection
    html.Div([
        html.H2("Connections"),
        html.Button('Auto', id="button_connection_auto", n_clicks=0),
        html.H4("DCC"),
        html.Div([
            dcc.Dropdown(id='port_com_dcc_value', placeholder="Select DCC controler"),
        ], style={'width': '80%'}),
        html.Button('Connexion DCC', id='button_connection_dcc', n_clicks=0),
        dcc.RadioItems(options=[{'label': 'Not Connected', 'value': 0, 'disabled': True},
                                {'label': 'Connected', 'value': 1, 'disabled': True}],
                       value=0,
                       id="status_connection_dcc"),
        html.Button('Mettre les rails sous tension', id='button_on_off', n_clicks=0),
        dcc.RadioItems(options=[{'label': 'Hors tension', 'value': 0, 'disabled': True},
                                {'label': 'Sous tension', 'value': 1, 'disabled': True}],
                       value=0,
                       id="status_power_dcc"),

        html.H4("Analog"),
        html.Div([
            dcc.Dropdown(id='port_com_analog_value', placeholder="Select Analog controler"),
        ], style={'width': '80%'}),
        html.Button('Connexion Analogique', id='button_connection_analog', n_clicks=0),
        dcc.RadioItems(options=[{'label': 'Not Connected', 'value': 0, 'disabled': True},
                                {'label': 'Connected', 'value': 1, 'disabled': True}],
                       value=0,
                       id="status_connection_analog"),
        html.Br(),
        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,
            n_intervals=0
        ),
        html.Div(id="status_temperature"),
        html.Div(id="status_humidity"),
    ], style={'width': '29%', 'display': 'inline-block', 'vertical-align': 'top'}
    ),
    # Trains
    html.Div([
        html.H2("Trains"),
        html.H4("DCC"),
        html.Div([
            "Numéro du train: ",
            dcc.Input(id='train_id', value=3, type='number')
        ]),
        dcc.Input(id="power_channel_dcc", value=0, type="range", min=0, max=100, step=5),
        html.Br(),
        html.Button('STOP', id='button_stop_dcc', n_clicks=0),
        html.Div([
            "Direction du train: ",
            dcc.RadioItems(['Avant', 'Arriere'], 'Avant', id="train_direction")
        ]),
        html.Div([
            "Etat du train:",
            html.Div(id="train_state")
        ]),
        html.Br(),
        html.Div("Parametres train:"),
        html.Button('Lumières', id='button_light', n_clicks=0),
        html.Div(id="state_light"),
        html.Button('Eclairage', id='button_light_cab', n_clicks=0),
        html.Div(id="state_light_cab"),
        html.Button('Klaxon', id='button_klaxon', n_clicks=0),
        html.Div(id="state_klaxon"),
        # Analog train
        html.H4("Analogique"),
        html.Div("Puissance voie (0-100) : "),
        dcc.Input(id="power_channel_analog", value=0, type="range", min=0, max=100, step=5),
        html.Div(id='power_channel_analog_text'),
        html.Br(),
        html.Button('STOP', id='button_stop_analog', n_clicks=0),
        html.Div([
            "Direction du train: ",
            dcc.RadioItems(['Avant', 'Arriere'], 'Avant', id="train_direction_analog")
        ]),
    ], style={'width': '29%', 'display': 'inline-block', 'vertical-align': 'top'}
    ),
    html.Div([
        html.H2("Plan réseau"),
        html.Div(
            dcc.Graph(id="graph_map_dcc")
        )
    ], style={'width': '39%', 'display': 'inline-block', 'vertical-align': 'top'})
])

########################
# AUTOMATIC CONNECTION #
########################
@app.callback(
    Output(component_id='port_com_dcc_value', component_property='options'),
    Output(component_id='port_com_analog_value', component_property='options'),
    Output(component_id='port_com_dcc_value', component_property='value'),
    Output(component_id='port_com_analog_value', component_property='value'),
    Output(component_id='button_connection_dcc', component_property='n_clicks'),
    Output(component_id='button_connection_analog', component_property='n_clicks'),
    Input(component_id="button_connection_auto", component_property='n_clicks'),
    State(component_id='button_connection_dcc', component_property='n_clicks'),
    State(component_id='button_connection_analog', component_property='n_clicks'),
)
def button_connection_auto(n_clicks_auto, n_clicks_dcc, n_clicks_analog):
    return mf.button_connection_auto(n_clicks_auto, n_clicks_dcc, n_clicks_analog, ARDUINO[0], ARDUINO[1])


###################
# NUMERIC CHANNEL #
###################
@app.callback(
    Output(component_id='state_klaxon', component_property='children'),
    Input(component_id='button_klaxon', component_property='n_clicks'),
    State(component_id='train_id', component_property='value'),
)
def button_klaxon(n_clicks, train_id):
    arduino = ARDUINO[0]
    if n_clicks == 0:
        return ""
    arduino.sound_klaxon(train_id)
    return ""


@app.callback(
    Output(component_id='state_light_cab', component_property='children'),
    Input(component_id='button_light_cab', component_property='n_clicks'),
    State(component_id='train_id', component_property='value'),
)
def button_light_cab(n_clicks, train_id):
    arduino = ARDUINO[0]
    if n_clicks == 0:
        return ""
    if (n_clicks % 2) == 0:
        arduino.light_cab_off(train_id)
        return 'Light cabine on'
    else:
        arduino.light_cab_on(train_id)
        return 'Light cabine off'


@app.callback(
    Output(component_id='state_light', component_property='children'),
    Input(component_id='button_light', component_property='n_clicks'),
    State(component_id='train_id', component_property='value'),
)
def button_light(n_clicks, train_id):
    arduino = ARDUINO[0]
    if n_clicks == 0:
        return ""
    if (n_clicks % 2) == 0:
        arduino.light_off(train_id)
    else:
        arduino.light_on(train_id)


@app.callback(
    Output(component_id='status_connection_dcc', component_property='value'),
    Input(component_id='button_connection_dcc', component_property='n_clicks'),
    State(component_id='port_com_dcc_value', component_property='value')
)
def connection_arduino_dcc(n_clicks, port_com_value):
    return mf.connection_arduino(n_clicks, ARDUINO[0], port_com_value)


@app.callback(
    Output(component_id='status_power_dcc', component_property='value'),
    Input(component_id='button_on_off', component_property='n_clicks'),
    Input(component_id='status_connection_dcc', component_property='value'),
    State(component_id='status_power_dcc', component_property='value'),
)
def power_on_off(n_clicks, status_connection_dcc, init_value):
    arduino = ARDUINO[0]
    if n_clicks == 0:
        return init_value
    if not status_connection_dcc == 1:
        return 0
    if init_value == 0:
        arduino.power_on()
        return 1
    else:
        arduino.power_off()
        return 0


@app.callback(
    Output(component_id='train_state', component_property='children'),
    Input(component_id="power_channel_dcc", component_property='value'),
    State(component_id='train_id', component_property='value'),
    State(component_id='train_direction', component_property='value'),
    State(component_id='status_connection_dcc', component_property='value'),
    State(component_id='status_power_dcc', component_property='value'),
)
def train(power_channel_dcc, train_id, train_direction, status_connection_dcc, status_power_dcc):
    arduino = ARDUINO[0]
    if status_connection_dcc == 0 or status_power_dcc == 0:
        return ""
    speed = int(int(power_channel_dcc) / 100 * 126)
    if train_direction == "Avant":
        direction = 1
    else:
        direction = 0
    arduino.set_speed_train(speed, int(train_id), direction)

    return f"Train ID: {train_id}, speed: {power_channel_dcc}, direction: {train_direction}"


##################
# ANALOG CHANNEL #
##################
@app.callback(
    Output(component_id='status_connection_analog', component_property='value'),
    Input(component_id='button_connection_analog', component_property='n_clicks'),
    State(component_id='port_com_analog_value', component_property='value')
)
def connection_arduino_analog(n_clicks, port_com_value):
    return mf.connection_arduino(n_clicks, ARDUINO[1], port_com_value)


@app.callback(
    Output(component_id="power_channel_analog_text", component_property="children"),
    Input(component_id="power_channel_analog", component_property="value"),
    Input(component_id="train_direction_analog", component_property="value"),
    State(component_id='status_connection_analog', component_property='value'),
)
def run_analog_channel(value_in, train_direction, status_analog_channel):
    arduino = ARDUINO[1]
    if status_analog_channel == 0:
        return ""
    try:
        if train_direction == "Avant":
            direction = 1
        else:
            direction = -1
        arduino.set_power(int(value_in) * direction)
        value_out = np.abs(arduino.get_power_value())
    except:
        value_out = 0

    msg = "{0}".format(int(value_out))
    return msg


@app.callback(
    Output(component_id="power_channel_analog", component_property="value"),
    Input(component_id="button_stop_analog", component_property="n_clicks"),
    Input(component_id='status_connection_analog', component_property='value')
)
def button_stop_analog(n_clicks, status_analog_channel):
    arduino = ARDUINO[1]
    if n_clicks == 0 or status_analog_channel == 0:
        return "0"
    arduino.set_stop()
    return 0

#########
# GRAPH #
#########
@app.callback(
    Output(component_id='graph_map_dcc', component_property="figure"),
    Input(component_id='status_connection_analog', component_property="value"),
    Input(component_id='status_connection_dcc', component_property="value"),
    Input(component_id='power_channel_analog', component_property="value"),
    Input(component_id="status_power_dcc", component_property='value'),
)
def graph_map(status_connection_analog, status_connection_dcc, power_channel_analog, status_power_dcc):
    return mf.graph_map(MAP_DATA, status_connection_analog, status_connection_dcc, power_channel_analog,
                        status_power_dcc)

#####################
# TEMP AND PRESSURE #
#####################
@app.callback(
    Output(component_id='status_temperature', component_property="children"),
    Output(component_id='status_humidity', component_property="children"),
    Input(component_id='interval-component', component_property="n_intervals"),
    Input(component_id='status_connection_analog', component_property="value")
)
def update_temp_pressure(n_intervals, status_connection_analog):
    arduino = ARDUINO[1]
    if status_connection_analog == 0:
        return ["", ""]
    temperature = arduino.get_temperature()
    time.sleep(0.5)
    humidity = arduino.get_humidity()

    temperature_string = "Temperature: {}°C".format(temperature)
    humidity_string = "Humidity: {}%".format(humidity)

    return [temperature_string, humidity_string]


if __name__ == '__main__':
    #app.run_server(debug=True, port=50000)
    app.run_server(host="192.168.1.14", port="7080")

