# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites.extend([{'label': site, 'value': site}
                    for site in spacex_df['Launch Site'].unique()])
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layouta
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(df.Year.unique(), value=2005, id='year')
                                dcc.Dropdown(options=launch_sites, id='site-dropdown', value='ALL',
                                             searchable=True, placeholder="Select a Launch Site here"),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(min=0, max=10000, value=[
                                                min_payload, max_payload], id='payload-slider', step=1000),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Sucess of all Launch Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        pie_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_counts = pie_data['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'count']
        class_counts['class'] = class_counts['class'].map(
            {0: 'Failure', 1: 'Success'})
        fig = px.pie(class_counts, values='count', names='class',
                     title='Sucess rate for Launch Site {}'.format(entered_site))
        return fig

        # TASK 4:
        # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
        # Run the app


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
              )
def get_scatter_chart(site, payload_range):

    if site == 'ALL':
        scatter_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (
            spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig2 = px.scatter(scatter_data, x='Payload Mass (kg)',
                          y='class', color='Booster Version Category')
        return fig2
    else:
        scatter_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (
            spacex_df['Launch Site'] == site) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig2 = px.scatter(scatter_data, x='Payload Mass (kg)',
                          y='class', color='Booster Version Category')
        return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
