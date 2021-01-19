import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px

# read data
electricity = pd.read_csv('electricity.csv')

# variables for max year and min year
year_min = electricity['Year'].min()
year_max = electricity['Year'].max()



# Using boot strap SOLAR theme
app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])

app.layout = html.Div([
    html.H1('Electricity Prices by US State'),
    dcc.RangeSlider(id='year-slider',
                    min=year_min, 
                    max=year_max, 
                    value=[year_min,year_max], 
                    marks={i:str(i) for i in range(year_min,year_max+1)}),
    dcc.Graph(id='map-graph'),
    dash_table.DataTable(id='price-info',
                        columns=[{'name':col, 'id':col} for col in electricity.columns])
])

# Update chloropleth map for selected range of years
@app.callback(
    Output('map-graph','figure'),
    Input('year-slider','value'),
)
def update_map_graph(selected_years):
    # filter for year between selected range
    filtered_electricity = electricity[(electricity['Year']>=selected_years[0]) & (electricity['Year']<=selected_years[1])]
    # average prices of electricity per state
    avg_price_electricity = filtered_electricity.groupby('US_State')['Residential Price'].mean().reset_index()
    # Chloropleth map figure
    map_fig = px.choropleth(avg_price_electricity,
                            locations='US_State',
                            locationmode='USA-states',
                            color='Residential Price',
                            scope='usa',
                            color_continuous_scale='reds')
    return map_fig

# update datatable for range of years and state clicked
@app.callback(
    Output('price-info','data'),
    Input('map-graph','clickData'),
    Input('year-slider','value')
)
def update_datable(clicked_data, selected_years):
    if clicked_data is None:
        return []
    # The state is stored in clickData as a dictionary which we retrive here
    us_state = clicked_data['points'][0]['location']
    # Filter by range of years selected and input state
    filtered_electricity = electricity[(electricity['Year']>=selected_years[0]) & (electricity['Year']<=selected_years[1]) & (electricity['US_State']==us_state)]
    return filtered_electricity.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)