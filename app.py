from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import polars as pl
import components.charts as chart
import components.inputs as input
from components.colors import DARK_COLOR
from components.footer import create_footer
from utils.format_utils import format_metric
import database.operations as db

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

purchases_file_path = 'data/amazon-purchases-prepared.csv'
df = pl.read_csv(purchases_file_path)
monthly_summary = db.get_monthly_summary(df)
state_summary = db.get_state_summary(df)

fig_style = {'height': '40vh'}
line_chart_fig = dcc.Graph(id='monthly-summary', style=fig_style)
choropleth_map_fig = dcc.Graph(id='state-summary', style=fig_style)
bar_chart_fig = dcc.Graph(id='category-summary', style=fig_style)
histogram_fig = dcc.Graph(id='metrics-distribution', style=fig_style)

summary_metrics = ['total_purchases', 'total_amount', 'total_quantity', 'average_amount', 'average_quantity', 'average_price']
summary_metric_select = input.create_select(id='summary-metric-select', options=summary_metrics)

distribution_metrics = ['Amount', 'Quantity', 'Purchase Price Per Unit']
distribution_metric_select = input.create_radio_items(id='distribution-metric-select', options=distribution_metrics)

footer = create_footer()

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2('Amazon Purchases Analysis'), md=8, sm=12, className='text-center mt-3 mb-2'),
            dbc.Col(summary_metric_select, md=4, sm=12, className='text-center mt-3 mb-4')
        ], className='mb-4'),
        dbc.Row([
            dbc.Col(line_chart_fig, lg=6, md=12, className='mb-4'),
            dbc.Col(bar_chart_fig, lg=6, md=12, className='mb-4'),
        ], className='mb-4'),
        dbc.Row([
            dbc.Col(choropleth_map_fig, lg=6, md=12, className='mb-4'),
            dbc.Col(distribution_metric_select, lg=1, md=2, className='mb-2'),
            dbc.Col(histogram_fig, lg=5, md=10, className='mb-4')
        ], className='mb-4'),
        dbc.Row([
            html.Div(className='mb-4'),
        ])
    ], fluid=True),
    footer
], style={'background-color': DARK_COLOR, 'color': 'white'})

@app.callback(
    Output('monthly-summary', 'figure'),
    Output('state-summary', 'figure'),
    Output('category-summary', 'figure'),
    Input('summary-metric-select', 'value')
)
def update_summary_figures(metric):
    formatted_metric = format_metric(metric)
    monthly_summary_fig = chart.create_line_chart(monthly_summary, x='Month', y=metric, title=f'Monthly {formatted_metric}')
    state_summary_fig = chart.create_choropleth_map(state_summary, location='Shipping Address State', z=metric, title=f'State {formatted_metric}')

    category_summary = db.get_category_summary(df, metric)
    category_summary_fig = chart.create_bar_chart(category_summary, x='Category', y=metric, title=f'Top 20 Categories by {formatted_metric}')
    return monthly_summary_fig, state_summary_fig, category_summary_fig

@app.callback(
    Output('metrics-distribution', 'figure'),
    Input('distribution-metric-select', 'value')
)
def update_distribution_figure(metric):
    metric_to_file = {
    'Amount': 'data/amount_histogram.csv',
    'Quantity': 'data/quantity_histogram.csv',
    'Purchase Price Per Unit': 'data/price_histogram.csv'
    }
    formatted_metric = format_metric(metric)
    file_path = metric_to_file.get(metric)
    if not file_path:
        return pl.DataFrame()
    histogram_df = pl.read_csv(file_path)
    distribution_fig = chart.create_histogram(histogram_df, x=metric, title=f'{formatted_metric} Distribution')
    return distribution_fig

if __name__ == '__main__':
    app.run_server(debug=True)
