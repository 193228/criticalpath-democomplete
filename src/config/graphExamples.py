import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': ['Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.Dropdown(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America',  #default value to show
        multi=True,
        searchable=False
    ),

    dcc.Dropdown(id='cities-dropdown', multi=True, searchable=False, placeholder="Select a city"),

    html.Div(id='display-selected-values')
])

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'options'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    if type(selected_country) == 'str':
        return [{'label': i, 'value': i} for i in all_options[selected_country]]
    else:
        return [{'label': i, 'value': i} for country in selected_country for i in all_options[country]]

if __name__ == '__main__':
    app.run_server(debug=True)