import dash_bootstrap_components as dbc
from utils.format_utils import format_metric

def create_select(id, options):
    select = dbc.Select(
                id=id,
                options=[{'label': format_metric(metric), 'value': metric} for metric in options],
                value=options[0],
                class_name='bg-dark text-white'
            )
    return select

def create_radio_items(id, options):
    radio_items = dbc.RadioItems(
                    id=id,
                    options=[{'label': metric, 'value': metric} for metric in options],
                    value=options[0]
                )
    return radio_items