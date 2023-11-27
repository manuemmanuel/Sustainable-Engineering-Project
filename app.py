
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('data.csv')

app = dash.Dash(__name__, title='Carbon Footprint Explorer')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dark_colours = {
    'background': '#000000', 
    'text': '#FFFFFF',
    'dropdown-background': '#333333',
    'dropdown-text': '#000000',  
    'graph-background': '#1E1E1E',
    'graph-line-color': '#00CC96',
}

app.layout = html.Div([
    html.H1('Carbon Footprint Data Representation', style={'color': dark_colours['text'], 'text-align': 'center', 'font-size': '2em', 'margin-bottom': '10px'}),
    html.Label('Select Country:', style={'margin-bottom': '10px', 'font-family': 'monospace', 'color': dark_colours['text'], 'text-align': 'center'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['country'].unique()],
        value='India', 
        style={
            'width': '80%',
            'margin': 'auto',
            'font-family': 'monospace',
            'background-color': dark_colours['dropdown-background'],
            'color': dark_colours['dropdown-text'],
            'border': 'none', 
            'box-shadow': 'none', 
            'margin-bottom': '20px',  
        },
        searchable=True,
        clearable=True,
        multi=False,
    ),
    dcc.Graph(id='line-plot', style={'margin-top': '20px', 'margin-bottom': '20px'}),  # Add margin-top and margin-bottom to create space
    html.Div(id='report', style={'margin-top': '20px', 'font-family': 'monospace', 'color': dark_colours['text'], 'font-size': '1.2em'}),  # Increase text size
    html.Footer('@ Sustainable Engineering Project by Manu Emmanuel, Felix Jobi, and Nagaraj Menon K S', style={'text-align': 'center', 'color': dark_colours['text'], 'margin-top': '30px'}),
], style={'height': '100vh', 'margin': 'auto', 'font-family': 'monospace', 'background-color': dark_colours['background'], 'color': dark_colours['text'], 'padding': '20px'})  # Add padding to lower position

@app.callback(
    [Output('line-plot', 'figure'),
     Output('report', 'children')],
    [Input('country-dropdown', 'value')]
)
def report(selected_country):
    selected_data = df[df['country'] == selected_country]

    fig = px.line(selected_data, x='year', y='co2_per_capita',
                  labels={'co2_per_capita': 'CO2 per Capita', 'year': 'Year'},
                  line_shape='linear')

    fig.update_layout(title=f'CO2 per Capita - {selected_country} Over Years',
                      plot_bgcolor=dark_colours['graph-background'],
                      paper_bgcolor=dark_colours['background'],
                      font=dict(color=dark_colours['text'], family='monospace'),  
                      xaxis=dict(linecolor=dark_colours['text']),
                      yaxis=dict(linecolor=dark_colours['text']),
                      hoverlabel=dict(bgcolor=dark_colours['background'], font_color=dark_colours['text']),
                      legend=dict(title=dict(text='Country', font=dict(color=dark_colours['text']))),
                      showlegend=True)

    fig.update_traces(line=dict(color=dark_colours['graph-line-color']))

    report = generate_report(selected_country, selected_data)

    return fig, report

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
