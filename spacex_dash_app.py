# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                            id='site-dropdown',
                                             options = [
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                             ],
                                             value = 'ALL',
                                             placeholder = 'placeholder',
                                             searchable = True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(
                                    dcc.Graph(
                                        id='success-pie-chart')
                                        ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = max_payload,
                                                step = 1000,
                                                value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function moment
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'), 
              Input(component_id = 'site-dropdown', component_property = 'value'))
def createpies(site_value):
    # Check the site value that is based on the input's component property
    if site_value == 'ALL':
        certain_df = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        figure = px.pie(certain_df, values = "class", 
                        names = "Launch Site",
                        title = "Success Ratio of the Launch Sites")
        return figure
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == site_value]["class"].value_counts().reset_index()
        print(filtered_df.head())
        figure = px.pie(filtered_df, values = "count", names = "class",
                        title = f"Success Ratio of Launch Site {site_value}")
        return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdown', component_property = 'value'),
              Input(component_id = 'payload-slider', component_property = 'value'))
def createScatter(site_value,load_value):
    scatterdf = spacex_df.copy()
    if site_value != 'ALL':
        # Set to the specified site
        scatterdf = scatterdf[scatterdf['Launch Site'] == site_value]
        # For the Title
        plottitle = f"Payload Launch Successes at {site_value}"
    else:
        plottitle = "Payload Launch Successes by SpaceX"
    # Set our dataframe to be between our two values
    scatterdf = scatterdf[scatterdf["Payload Mass (kg)"].between(load_value[0], load_value[1])]
    # No need to do much else, just create a scatter based on x = payload, y is class, colors = booster version
    figure = px.scatter(scatterdf, 
                        x = "Payload Mass (kg)", 
                        y = "class", 
                        color = "Booster Version",
                        title = plottitle
                        )
    return figure
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)
