from dash import html
import dash_bootstrap_components as dbc
import components.colors as color

def create_footer():
    link_style = {
    'color': color.PRIMARY_COLOR,
    'font-weight': 'bold',
    'font-size': '16px',
    'text-decoration': 'none'
    }
    footer = html.Footer(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            "Source Code",
                            href="https://github.com/Alfredomg49/amazon-dashboard",
                            target="_blank",
                            style=link_style
                        ),
                        className='text-center'
                    ),
                    dbc.Col(
                        html.A(
                            "Data Source",
                            href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YGLYDY",
                            target="_blank",
                            style=link_style
                        ),
                        className='text-center'
                    ),
                ],
                className='justify-content-center',
            )
        ],
        className='py-3 mt-4',
        style={
            'background-color': color.DARK_COLOR,
            'position': 'fixed',
            'bottom': '0',
            'width': '100%',
            'box-shadow': f'0 -1px 5px {color.PRIMARY_COLOR_RGBA}',
            'z-index': '1000'
        }
    )
    return footer