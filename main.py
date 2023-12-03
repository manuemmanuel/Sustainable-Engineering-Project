import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('data.csv')

app = dash.Dash(__name__, title='Carbon Footprint Explorer')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

light_colours = {
    'background': '#FFFFFF',
    'text': '#000000',
    'dropdown-background': '#F0F0F0',
    'dropdown-text': '#000000',
    'graph-background': '#E5E5E5',
    'graph-line-color': '#4285F4',
    'box-border-color': '#000000',  # Border color for the report box
}

app.layout = html.Div([
    html.Div([
        html.H1('Carbon Footprint Data Representation', id='title', style={'text-align': 'center', 'font-size': '3em', 'margin-bottom': '20px', 'font-family': 'monospace'}),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value='India',
            style={
                'margin': 'auto',
                'font-family': 'monospace',
                'margin-bottom': '20px',
                'width': '60% !important',  # Add important rule to enforce width
            },
            searchable=True,
            clearable=True,
            multi=False,
        ),
    ]),
    dcc.Graph(id='line-plot', style={'margin-top': '20px', 'margin-bottom': '20px'}),
    html.Div([
        html.H3('Report', style={'text-align': 'center', 'color': light_colours['text'], 'margin-bottom': '10px', 'font-family': 'monospace', 'font-size': '2em'}),
        html.Div(id='report-box', children=[
            html.Div(id='report', style={'font-family': 'monospace', 'font-size': '1.5em'}),
        ], style={'border': f'2px solid {light_colours["box-border-color"]}', 'padding': '10px', 'border-radius': '10px', 'margin': 'auto', 'width': '60%'}),
    ], style={'margin-top': '20px'}),
    html.Footer('@ Sustainable Engineering Project by Manu Emmanuel, Felix Jobi, and Nagaraj Menon K S', id='footer', style={'text-align': 'center', 'margin-top': '30px', 'font-family': 'monospace'}),
], id='main-div', style={'background-color': '#FFFFFF', 'color': '#000000'})

@app.callback(
    [Output('line-plot', 'figure'),
     Output('report', 'children')],
    [Input('country-dropdown', 'value')]
)
def update_layout(selected_country):
    selected_data = df[df['country'] == selected_country]

    fig = px.line(selected_data, x='year', y='co2_per_capita',
                  labels={'co2_per_capita': 'CO2 per Capita', 'year': 'Year'},
                  line_shape='linear')

    fig.update_layout(title=f'CO2 per Capita - {selected_country} Over Years',
                      plot_bgcolor=light_colours['graph-background'],
                      paper_bgcolor=light_colours['background'],
                      font=dict(color=light_colours['text'], family='monospace'),
                      xaxis=dict(linecolor=light_colours['text']),
                      yaxis=dict(linecolor=light_colours['text']),
                      hoverlabel=dict(bgcolor=light_colours['background'], font_color=light_colours['text']),
                      legend=dict(title=dict(text='Country', font=dict(color=light_colours['text']))),
                      showlegend=True)

    fig.update_traces(line=dict(color=light_colours['graph-line-color']))

    report_text = generate_report(selected_country, selected_data)

    return fig, report_text

def generate_report(country, data):
    start_year = data['year'].min()
    end_year = data['year'].max()
    highest_footprint = data.loc[data['co2_per_capita'].idxmax()]

    template = f"""
    {country} Carbon Footprint Report:
    
    Data from {start_year} to {end_year} is shown in the graph.
    
    The highest recorded carbon footprint for {country} was in {highest_footprint['year']} with a value of {highest_footprint['co2_per_capita']} CO2 per capita.

    """

    return template

if __name__ == '__main__':
    app.run_server(debug=True)
