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
    'text': '#000000',
    'dropdown-background': '#F0F0F0',
    'dropdown-text': '#000000',
    'graph-background': '#E5E5E5',
    'graph-line-color': '#4285F4',
}

app.layout = html.Div([
    html.Div([
        html.H1('Carbon Footprint Data Representation', id='title', style={'text-align': 'center', 'font-size': '2em', 'margin-bottom': '10px', 'font-family': 'monospace'}),
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
    dcc.Checklist(
        id='theme-toggle',
        options=[
            {'label': 'Dark Mode', 'value': 'dark'},
        ],
        value=[],  # Default mode (empty list for Light Mode)
        inline=True,
        labelStyle={'display': 'block', 'margin-top': '10px', 'font-family': 'monospace'},
    ),
    dcc.Graph(id='line-plot', style={'margin-top': '20px', 'margin-bottom': '20px'}),
    html.Div(id='report', style={'margin-top': '20px', 'font-family': 'monospace', 'font-size': '1.5em'}),  # Increased font size
    html.Footer('@ Sustainable Engineering Project by Manu Emmanuel, Felix Jobi, and Nagaraj Menon K S', id='footer', style={'text-align': 'center', 'margin-top': '30px', 'font-family': 'monospace'}),
], id='main-div')

# Dynamic styles for dark and light modes
app.layout.children.append(html.Style(id='style', children=[]))

@app.callback(
    [Output('line-plot', 'figure'),
     Output('report', 'children'),
     Output('style', 'children')],
    [Input('country-dropdown', 'value'),
     Input('theme-toggle', 'value')]
)
def report(selected_country, selected_theme):
    selected_data = df[df['country'] == selected_country]

    if selected_theme == 'dark':
        colours = dark_colours
        dynamic_styles = [
            {'property': 'background-color', 'value': dark_colours['background']},
            {'property': 'color', 'value': dark_colours['text']},
        ]
    else:
        colours = light_colours
        dynamic_styles = [
            {'property': 'background-color', 'value': light_colours['background']},
            {'property': 'color', 'value': light_colours['text']},
        ]

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

    return fig, report_text, dynamic_styles

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
