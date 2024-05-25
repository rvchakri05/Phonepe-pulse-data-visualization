import pandas as pd
import numpy as np

def highlight_cells(data, color_config):

    """
    
        Modify the style of a pandas dataframe.

        Description:
            Modify the style of a pandas dataframe, with a certain color config. 
            Gives a dark color to even rows and light color to uneven rows.

        Args:
            - data (pandas.DataFrame) : data to display in the table
            - color_config (dict) : dict with color config
                - 'columns' (list) : list of str, columns to highlight
                - 'dark_color' (str) : even row color
                - 'light_color' (str) : uneven row color
                - 'header_color' (str) : header color
                - 'header_bg_color' (str) : header background color

        Returns:
            - data (pandas.DataFrame) : data with modified style
    
    """

    # Create an empty styler dataframe
    styler = pd.DataFrame('', index=data.index, columns=data.columns)
    header_styles = []

    # For each color config
    for config in color_config:
        # For each column in the config
        for col in config['columns']:
            # If the column is in the dataframe
            if col in data.columns:
                # Apply the style to the column
                styler[col] = np.where(styler.index % 2 == 0, f'background-color: {config["dark_color"]}; color: white', f'background-color: {config["light_color"]}; color: white')
                header_styles.append({
                    'selector': f'th:nth-child({data.columns.get_loc(col) + 2})',
                    'props': [
                        ('background-color', config['header_bg_color']),
                        ('color', config['header_color'])
                    ]
                })
                
    # Apply the style to the dataframe
    df_styler = data.style.apply(lambda _: styler, axis=None)
    df_styler.set_table_styles(header_styles)

    return df_styler

color_config = [
    {
        'columns': ['State', 'District','Pincodes','Year'],
        'dark_color': '#f06292',
        'light_color': '#f06292',
        'header_color': '#f06292',
        'header_bg_color': '#f06292'
    },
    {
        'columns': ['Total_Tranaction', 'Total_Amount','Total_Users','Total_User','Apps_Opens','Total_Transaction_Amount','Total_Insurance_Transaction_Amount'],
        'dark_color': '#2E4569',
        'light_color': '#2E4569',
        'header_color': '#2E4569',
        'header_bg_color': '#2E4569'
    }
]