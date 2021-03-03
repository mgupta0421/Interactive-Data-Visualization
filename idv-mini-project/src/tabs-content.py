import parser
import webbrowser
from threading import Timer

import dash
import dash_core_components as dcc
import dash_html_components as html
import firstVis
import visualization2
from dash.dependencies import Input, Output

policy = parser.get_policy_list()
regions = ['world', 'europe', 'asia', 'africa', 'north america', 'south america']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
port = 8050
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
# layout of the dash app

app.layout = html.Div(
    [html.H1(children='Country-wise Government Policy Visualizer', style={'textAlign': 'center', 'color': '#00178b'}),
     html.Div([
         dcc.Tabs(id='graphs', value='tab-1', children=[
             dcc.Tab(label='World-Map', value='tab-1', children=[
                 html.Div(
                     [
                         html.P("""Select the region to filter the map""",
                                 style={'margin-right': '15em'})
                     ],
                 ),
                 dcc.Dropdown(id='selected-region',
                              options=[
                                  {'label': x, 'value': x, 'disabled': False}
                                  for x in regions
                              ],
                              value='world',
                              clearable=False,
                              style=dict(
                                  width='40%',
                                  verticalAlign="middle"
                              )
                              ),
                 dcc.Graph(
                     id='vis1',
                     # figure=firstVis.worldMap()
                 )
             ]),
             dcc.Tab(id='tab2', label='Policy Graph', value='tab-2', disabled=True, children=[
                 html.Div([
                     dcc.Graph(
                         id='vis2',
                     )
                 ]),
                 dcc.Checklist(
                     id='my_list',
                     options=[
                         {'label': x, 'value': x}
                         for x in policy
                     ],
                     value=[x for x in policy],
                     className='my_box_container',
                     inputClassName='my_box_input',
                     labelClassName='my_box_label',
                 ),
             ]),
         ]),
     ]),
     html.Div(children='Team : The Chart Busters', style={
         'textAlign': 'center', "height": "auto", "margin-bottom": "auto"})
     ])


# callback for switching the tabs
@app.callback(Output('graphs', 'value'),
              [Input('vis1', 'clickData')])
def switch_tab(clickData, *params):
    if clickData is not None:
        return 'tab-2'
    return 'tab-1'


# callback for sending the clicked value
@app.callback(Output('vis2', 'figure'),
              [Input('my_list', 'value'), Input('vis1', 'clickData')])
def plotvis2(list, clickData):
    return visualization2.plotFun(list, clickData['points'][0]['location'])

# callback for updating checklist on new country data load
@app.callback(Output('my_list', 'value'),
              [Input('vis1', 'clickData')])
def updateChecklist(clickData):
    if clickData is not None:
        return policy


# enable tab 2 after something is clicked on first tab
@app.callback(Output('tab2', 'disabled'),
              [Input('vis1', 'clickData')])
def enable_tab(clickData):
    if clickData['points'][0]['location'] is not None:
        return False


# callback for sending the clicked value
@app.callback(Output('vis1', 'figure'),
              [Input('selected-region', 'value')])
def plotvis1(list):
    return firstVis.worldMap(list)


# open browser on localhost:8050
def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(host='localhost', port=port, debug=False)
