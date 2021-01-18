import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd

# load in data
soccer = pd.read_csv('fifa_soccer_players.csv')

# Create Dash object with external style sheet
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# dictionary of unique player names
player_name_options = [{'label':i, 'value':i} for i in soccer['long_name'].unique()]

app.layout = html.Div([
    html.H1('Soccer Players Dashboard'),
    # Bootstrap grid system
    dbc.Row([
        dbc.Col(
            html.P(['Source: ',
                html.A('Sofifa', href='https://sofifa.com', target='_blank')])),
        dbc.Col([
            html.Label('Plater name: '),
            dcc.Dropdown(options=player_name_options,value=player_name_options[0]['value'])
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)