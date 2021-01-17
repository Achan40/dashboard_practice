import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

# load in dataset
happiness = pd.read_csv('world_happiness.csv')

# create dash object
app = dash.Dash()

# items in dataset for region column
region_options = [{'label': i, 'value': i} for i in happiness['region'].unique()]

# items in dataset for country column
country_options = [{'label': i, 'value': i} for i in happiness['country'].unique()]

# line plot for Happiness Score of US only
line_fig = px.line(happiness[happiness['country']=='United States'], x='year', y='happiness_score', title='Happiness Score in the USA')

# rendering dashboard
app.layout = html.Div([
    html.H1('World Happiness Dashboard'),
    html.P(['This dashboard shows the happipness score.',
        html.Br(),
        html.A('World Happiness Report Data Source',
            href='https://worldhappiness.report/',
            target='_blank')]),
    dcc.RadioItems(options=region_options, value='North America'),
    dcc.Checklist(options=region_options, value=['North America']),
    dcc.Dropdown(options=country_options, value='United States'),
    dcc.Graph(figure=line_fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

