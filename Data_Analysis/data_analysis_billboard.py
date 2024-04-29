import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import pandas as pd
import webbrowser

def bar_graph_billboard():
    with open('joined_billboard.json', 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')  # Format dates
    df = df.sort_values(by='occurrences', ascending=False)  # Sort by occurrences in descending order

    # Create a Dash application (for use in a Jupyter notebook)
    app = JupyterDash(__name__)

    # Define the layout of the app
    app.layout = html.Div([
        dcc.Graph(
            id='bar-graph',
            config={'staticPlot': False},  # Allows for interaction such as zoom
            figure={
                'data': [
                    go.Bar(
                        x=df['date'],
                        y=df['occurrences'],
                        text=df['url'],  # URLs stored in text attribute, used for clicking
                        hoverinfo='text+y'
                    )
                ],
                'layout': go.Layout(
                    title='Nasa Images of the Day Based on Most Occurring Release Dates for Songs on the Billboard Hot 100 Chart',
                    xaxis=dict(title='Date', tickmode='linear'),
                    yaxis=dict(title='Occurrences'),
                    clickmode='event+select',
                    bargap=0.05  # Reduce the gap between bars to remove white space
                )
            }
        ),
        html.Pre(id='click-data')
    ])

    # Define callback to handle clicks
    @app.callback(
        Output('click-data', 'children'),
        [Input('bar-graph', 'clickData')]
    )
    def display_click_data(clickData):
        if clickData:
            url = clickData['points'][0]['text']
            # Open URL in a new tab, consider security implications and environment capabilities
            webbrowser.open(url)
        return json.dumps(clickData, indent=2)

    # Run the app inside the notebook
    app.run_server(mode='inline')

def main():
    bar_graph_billboard()

if __name__ == '__main__':
    main()