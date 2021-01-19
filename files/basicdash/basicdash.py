import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# load in dataset
happiness = pd.read_csv('world_happiness.csv')

# create dash object
app = dash.Dash()

# items in dataset for region column
region_options = [{'label': i, 'value': i} for i in happiness['region'].unique()]

# Multiple inputs
data_options = [{'label':'Happiness Score','value':'happiness_score'},{'label':'Happiness Rank','value':'happiness_rank'}]

# rendering dashboard
app.layout = html.Div([
    html.H1('World Happiness Dashboard'),
    html.P(['This dashboard shows the happipness score.',
        html.Br(),
        html.A('World Happiness Report Data Source',
            href='https://worldhappiness.report/',
            target='_blank')]),
    dcc.RadioItems(id='region-radio', options=region_options, value='North America'),
    dcc.Dropdown(id='country-dropdown'),
    dcc.RadioItems(id='data-radio',options=data_options,value='happiness_score'),
    dcc.Graph(id='happiness-graph'),
    html.Div(id='average-div')
])

# country dropdown value depending on region selected
@app.callback(
    Output('country-dropdown','options'),
    Output('country-dropdown','value'),
    Input('region-radio','value'),
)

def update_dropdown(selected_region):
    filtered_happiness = happiness[happiness['region']==selected_region]
    # get all of the unique countries based on the filtered_happiness dataset which will get the unique countries within the selected regions only
    country_options = [{'label':i,'value':i} for i in filtered_happiness['country'].unique()]
    return country_options, country_options[0]['value']

# This call back changes graph depending on selected as well as output avg values for selected country and data type
# we can omit component_id and component_property if we want
@app.callback(
    Output(component_id='happiness-graph',component_property='figure'),
    Output('average-div','children'),
    Input(component_id='country-dropdown',component_property='value'),
    Input('data-radio','value')
)

def update_graph(selected_country, selected_data):
    filtered_happiness = happiness[happiness['country']==selected_country]
    line_fig = px.line(filtered_happiness,x='year', y=selected_data,title=f'{selected_data} in {selected_country}')
    selected_avg = filtered_happiness[selected_data].mean()
    return line_fig, f'The average {selected_data} for {selected_country} is {selected_avg}'

if __name__ == '__main__':
    app.run_server(debug=True)

