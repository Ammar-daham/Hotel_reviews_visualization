
import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import html, Output, Input
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from matplotlib.pyplot import figure
import plotly.express as px


df = pd.read_csv('assignment_2/data/EU_hotels_map.csv')
df

px.set_mapbox_access_token(open("data_map/Visualizing Geographical Data/mapbox_token").read())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])



# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "black",
}



sidebar = html.Div(
    [
        html.H2("Hotel Reviews", className="display-4"),
        html.Hr(),
        html.P(
            "Hotel reviews visualisation", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content, 
])





@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
           return [
                dcc.Dropdown(id="slct_city",       
                options=[{'label': s, 'value': s} for s in sorted(df.city.unique())],
                value='The Netherlands, Amsterdam',
                ),
               dcc.Graph(id='map')
           ] 
                
    elif pathname == "/page-1":
        return [
               
                ]

    elif pathname == "/page-2":
        return [
                
                ]
    # # If the user tries to reach a different page, return a 404 message
    # return dbc.Jumbotron(
    #     [
    #         html.H1("404: Not found", className="text-danger"),
    #         html.Hr(),
    #         html.P(f"The pathname {pathname} was not recognised..."),
    #     ]
    # )

@app.callback(
        Output("map", "figure"),
        [Input("slct_city", "value")],
        )
def update_graph(option_slctd):

    dff = df.copy()

    dff = dff[dff["city"] == option_slctd]

    fig = px.scatter_mapbox(
                        dff,
                        lat='lat',
                        lon='lng',
                        size = 'Average_Score',
                        size_max = 8,
                        mapbox_style='open-street-map',
                        opacity=1.0,
                        range_color=[10,28],
                        color_continuous_midpoint= 5,
                        color_continuous_scale = 'blowOrdarkblow',
                        hover_name = 'Hotel_Name',
                        color = 'Hotel_Name',
                        hover_data = {
                            'lat': True,
                            'lng': True,
                            'Hotel_Address': True,
                        },
                        zoom=10,height=650,template='plotly_dark', title='<b>European hotel reviews</b><br><br>6 countries | 1500 hotels | 515k reviews <br>')
    return fig
                    


if __name__=='__main__':
    app.run_server()












