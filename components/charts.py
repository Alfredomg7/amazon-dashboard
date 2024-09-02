import plotly.express as px
from utils.format_utils import format_metric
import components.colors as color

def create_line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, title=title, color_discrete_sequence=[color.PRIMARY_COLOR])
    style_fig(fig)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text=format_metric(y))
    return fig

def create_bar_chart(df, x, y, title):
    fig = px.bar(df, x=y, y=x, title=title, color_discrete_sequence=[color.SECONDARY_COLOR], orientation='h')
    style_fig(fig)
    fig.update_xaxes(title_text='')
    fig.update_xaxes(title_text=format_metric(y))
    return fig

def create_choropleth_map(df, location, z, title):
    fig = px.choropleth(df, locationmode='USA-states', locations=location, color=z, title=title, scope='usa', color_continuous_scale='Sunset')
    style_fig(fig)
    fig.update_layout(geo_bgcolor=color.DARK_COLOR)
    fig.update_traces(hovertemplate='<b>%{location}</b><br>%{z} ' + format_metric(z))
    fig.update_coloraxes(colorbar=dict(title=dict(text=format_metric(z), font=dict(color=color.SOFT_COLOR)),
                                        tickfont=dict(color=color.SOFT_COLOR)))
    return fig

def create_histogram(df, x, title):
    fig = px.bar(df, x=x, y='Count', title=title, color_discrete_sequence=[color.PRIMARY_COLOR])
    style_fig(fig)
    return fig

def style_fig(fig):
    fig.update_layout(
        title=dict(
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    fig.update_layout(
        plot_bgcolor=color.DARK_COLOR,
        paper_bgcolor=color.DARK_COLOR,
        title_font=dict(color=color.SOFT_COLOR),
        xaxis=dict(title_font=dict(color=color.SOFT_COLOR), tickfont=dict(color=color.SOFT_COLOR)),
        yaxis=dict(title_font=dict(color=color.SOFT_COLOR), tickfont=dict(color=color.SOFT_COLOR)),
        legend=dict(title_font=dict(color=color.SOFT_COLOR), font=dict(color=color.SOFT_COLOR))
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)