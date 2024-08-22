import dash                              # pip install dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
import datetime as dt
from datetime import date
import calendar
from wordcloud import WordCloud
import base64

path = "C:/Users/Anam Ahmed/Desktop/Projects/Linkedin Project/"

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets9.lottiefiles.com/private_files/lf30_5ttqPi.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets9.lottiefiles.com/packages/lf20_8wREpI.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
url_reactions = "https://assets2.lottiefiles.com/packages/lf20_nKwET0.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


# Import App data from csv sheets **************************************
df_cnt = pd.read_csv(path+"connection.csv")
df_cnt["Connected On"] = pd.to_datetime(df_cnt["Connected On"])
df_cnt["Month"] = df_cnt["Connected On"].dt.month_name()
df_invite = pd.read_csv(path + "Invitations.csv")
df_invite["Sent At"] = pd.to_datetime(df_invite["Sent At"])

# df_react = pd.read_csv(path+"Reactions.csv")
# df_react["Date"] = pd.to_datetime(df_react["Date"])

df_msg = pd.read_csv(path + "Messaages.csv")
df_msg["DATE"] = pd.to_datetime(df_msg["DATE"])


image_filename = 'file.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())




# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image.decode())) # 150px by 45px
            ],className='mb-2'),
            dbc.Card([
                dbc.CardBody([
                    dbc.CardLink("Anam Ahmed (Data Scientist", target="_blank",
                                 href="https://www.linkedin.com/in/anam-ahmed-423ba1283/"
                    )
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.DatePickerSingle(
                        id='my-date-picker-start',
                        date=date(2023, 12, 17),
                        # clearable = True,
                        className='mr-2' ,
                        style={'zIndex': '1000',  'position': 'relative',  'backgroundColor': '#FFFFFF'},  # Adjust zIndex and backgroundColor
                        # with_full_screen_portal=True
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-end',
                        date=date(2024, 4, 4),
                        clearable = True,

                        # className='mb-2 ml-2'
                    ),
                ])
            ], color="Primary", style={'height':'18vh'}),
        ], width=8),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Connections'),
                    html.H2(id='content-connections' , children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Companies'),
                    html.H2(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Invites received'),
                    html.H2(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="53%", height="53%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Invites sent'),
                    html.H2(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_reactions)),
                dbc.CardBody([
                    html.H6('Reactions'),
                    html.H2(id='content-reactions', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
    dbc.Row([
        # dbc.Col([
        #     dbc.Card([
        #         dbc.CardBody([
        #             dcc.Graph(id='bar-chart1', figure={}, config={'displayModeBar': False}),
        #         ])
        #     ]),
        # ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
    ],className='mb-2'),
], fluid=True)


# Updating the 5 number cards ******************************************
@app.callback(
    Output('content-connections','children'),
    Output('content-companies','children'),
    Output('content-msg-in','children'),
    Output('content-msg-out','children'),
    # Output('content-reactions','children'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_small_cards(start_date, end_date):
    # Connections
    dff_c = df_cnt.copy()

    dff_c = dff_c[(dff_c['Connected On']>=start_date) & (dff_c['Connected On']<=end_date)]
    conctns_num = len(dff_c)
    compns_num = len(dff_c['Company'].unique())

    # Invitations
    dff_i = df_invite.copy()
    dff_i = dff_i[(dff_i['Sent At']>=start_date) & (dff_i['Sent At']<=end_date)]
    # print(dff_i)
    in_num = len(dff_i[dff_i['Direction']=='INCOMING'])
    out_num = len(dff_i[dff_i['Direction']=='OUTGOING'])

    # # Reactions
    # dff_r = df_react.copy()
    # dff_r = dff_r[(dff_r['Date']>=start_date) & (dff_r['Date']<=end_date)]
    # reactns_num = len(dff_r)

    return (conctns_num, compns_num, in_num, out_num
            # reactns_num
            )


@app.callback(
    Output('line-chart', 'figure'),
    [Input('my-date-picker-start', 'date'),
     Input('my-date-picker-end', 'date')]
)
def update_line(start_date, end_date):
    # Ensure that the 'Connected On' column is in datetime format
    df_cnt['Connected On'] = pd.to_datetime(df_cnt['Connected On'])

    # Filter the dataframe based on the selected date range
    dff = df_cnt[(df_cnt['Connected On'] >= start_date) & (df_cnt['Connected On'] <= end_date)]

    # Extract the month in a format that allows sorting by calendar months
    dff['Month'] = dff['Connected On'].dt.strftime('%B')

    # Count the total connections per month
    dff = dff['Month'].value_counts().rename_axis('Month').reset_index(name='Total Connections')

    # Ensure the months are in chronological order
    months_order = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
    dff['Month'] = pd.Categorical(dff['Month'], categories=months_order, ordered=True)
    dff.sort_values('Month', inplace=True)

    # Create the line chart using Plotly Express
    fig_line = px.line(dff, x='Month', y='Total Connections', template='ggplot2',
                       title="Total Connections by Month")

    # Update trace and layout properties
    fig_line.update_traces(mode="lines+markers", fill='tozeroy', line={'color': 'blue'})
    fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20) ,
    plot_bgcolor = 'rgba(0,0,0,0)',  # Transparent plot area
    paper_bgcolor = 'rgba(0,0,0,0)',  # Transparent background outside the plot area
                           )


    return fig_line


#
# Bar Chart ************************************************************
@app.callback(
    Output('bar-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_bar(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]

    dff = dff[["Company"]].value_counts().head(6)
    dff = dff.to_frame()
    dff.reset_index(inplace=True)
    dff.rename(columns={0:'Total connections'}, inplace=True)

    fig_bar = px.bar(dff, x='Total connections', y='Company', template='ggplot2',
                      orientation='h', title="Total Connections by Company")
    fig_bar.update_yaxes(tickangle=20)
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20) ,
                          plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
                          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background outside the plot area
                          )

    fig_bar.update_traces(marker_color='blue')

    return fig_bar



# Pie Chart ************************************************************
@app.callback(
    Output('pie-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_pie(start_date, end_date):
    dff = df_msg.copy()
    dff = dff[(dff['DATE']>=start_date) & (dff['DATE']<=end_date)]
    msg_sent = len(dff[dff['FROM']=='Anam Ahmed'])
    msg_rcvd = len(dff[dff['FROM'] != 'Anam Ahmed'])
    fig_pie = px.pie(names=['Sent','Received'], values=[msg_sent, msg_rcvd],
                     template='ggplot2', title="Messages Sent & Received"
                     )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20) ,
                          plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
                          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background outside the plot area
                          )

    fig_pie.update_traces(marker_colors=['red','blue'])

    return fig_pie
#
#
# Word Cloud ************************************************************
@app.callback(
    Output('wordcloud','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_pie(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff.Position[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)].astype(str)

    my_wordcloud = WordCloud(
        background_color='white',
        height=275
    ).generate(' '.join(dff))

    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2',
                              title="Total Connections by Position")
    fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20) ,
                                plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
                                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background outside the plot area
                                )

    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_wordcloud


if __name__=='__main__':
    app.run_server(debug=False, port=8004)