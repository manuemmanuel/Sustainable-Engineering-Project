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

light_colours = {
    'background': '#FFFFFF',
    'text': '#000000',  # Updated to black
    'dropdown-background': '#F0F0F0',
    'dropdown-text': '#000000',
    'graph-background': '#E5E5E5',  # Adjusted background color for better contrast
    'graph-line-color': '#4285F4',
}

app.layout = html.Div([
    html.Div([
        html.H1('Carbon Footprint Data Representation', id='title', style={'text-align': 'center', 'font-size': '2em', 'margin-bottom': '10px', 'color': dark_colours['text']}),
        html.Label('Select Country:', style={'margin-bottom': '10px', 'font-family': 'monospace', 'color': dark_colours['text'], 'text-align': 'center'}),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value='India',
            style={
                'width': '80%',
                'margin': 'auto',
                'font-family': 'monospace',
                'margin-bottom': '20px',
            },
            searchable=True,
            clearable=True,
            multi=False,
        ),
    ]),
    dcc.RadioItems(
        id='theme-toggle',
        options=[
            {'label': 'Dark Mode', 'value': 'dark'},
            {'label': 'Light Mode', 'value': 'light'},
        ],
        value='dark',  # Default mode
        labelStyle={'display': 'block', 'margin-top': '10px'},
    ),
    dcc.Graph(id='line-plot', style={'margin-top': '20px', 'margin-bottom': '20px'}),  # Add margin-top and margin-bottom to create space
    html.Div(id='report', style={'margin-top': '20px', 'font-family': 'monospace', 'color': dark_colours['text'], 'font-size': '1.2em'}),  # Increase text size
    html.Footer('@ Sustainable Engineering Project by Manu Emmanuel, Felix Jobi, and Nagaraj Menon K S', style={'text-align': 'center', 'color': dark_colours['text'], 'margin-top': '30px'}),
], style={'height': '100vh', 'margin': 'auto', 'font-family': 'monospace', 'padding': '20px'})  # Add padding to lower position

@app.callback(
    [Output('line-plot', 'figure'),
     Output('report', 'children'),
     Output('title', 'style')],
    [Input('country-dropdown', 'value'),
     Input('theme-toggle', 'value')]
)
def report(selected_country, selected_theme):
    selected_data = df[df['country'] == selected_country]

    colours = dark_colours if selected_theme == 'dark' else light_colours

    fig = px.line(selected_data, x='year', y='co2_per_capita',
                  labels={'co2_per_capita': 'CO2 per Capita', 'year': 'Year'},
                  line_shape='linear')

    fig.update_layout(title=f'CO2 per Capita - {selected_country} Over Years',
                      plot_bgcolor=colours['graph-background'],
                      paper_bgcolor=colours['background'],
                      font=dict(color=colours['text'], family='monospace'),
                      xaxis=dict(linecolor=colours['text']),
                      yaxis=dict(linecolor=colours['text']),
                      hoverlabel=dict(bgcolor=colours['background'], font_color=colours['text']),
                      legend=dict(title=dict(text='Country', font=dict(color=colours['text']))),
                      showlegend=True)

    fig.update_traces(line=dict(color=colours['graph-line-color']))

    report_text = generate_report(selected_country, selected_data)

    title_style = {'color': colours['text']}  # Set the text color of the title dynamically

    return fig, report_text, title_style

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
