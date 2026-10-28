import streamlit as st
from streamlit_sortables import sort_items
import numpy as np

def title_x_y_label():
    """a simple function to compartmentalize the title and x/y labels of a graph

    Returns: the title, xaxis_label, yaxis_label values
    """
    title = st.text_input("Chart Title", value="Chart Title ...")
    title_size = st.slider("Select Title Size", min_value=8, max_value=50, value=12, step=1)

    xaxis_label = st.text_input("X Axis Label", value="X Axis Label...")
    x_size = st.slider("Select X-Label Size", min_value=8, max_value=50, value=12, step=1)

    yaxis_label = st.text_input("Y Axis Label", value="Y Axis Label ...")
    y_size = st.slider("Select Y-Label Size", min_value=8, max_value=50, value=12, step=1)

    return title, xaxis_label, yaxis_label, title_size, x_size, y_size


def set_title_x_y_label(fig, title, xaxis_label, yaxis_label, title_size, x_size, y_size):
    """takes in the plotly figure object and sets the title, xaxis_label, yaxis_label values

    Args:
        fig (_type_): _description_
        title (_type_): _description_
        xaxis_label (_type_): _description_
        yaxis_label (_type_): _description_

    Returns:
        _type_: _description_
    """
    fig.update_layout(
        title={'text': title, 'font': {'size': title_size}},
        xaxis_title={'text': xaxis_label, 'font': {'size': x_size}},
        yaxis_title={'text': yaxis_label, 'font': {'size': y_size}}
    )
    # print(fig.data)
    return fig


def x_tick_size():
    """Asks users for size of x-ticks.
    
    Returns: category label size
    """
    x_tick_size = st.slider("Select X-tick Size", min_value=8, max_value=50, value=12, step=1)
    return x_tick_size


def set_x_tick_size(fig, x_tick_size):
    """Sets the font size of category labels (tick labels) on the x axes. 
    Useful for bar charts/histograms

    Args:
        fig (plotly.graph_objs._figure.Figure): Plotly figure object.
        x_tick_size (int): Font size for x-axis tick labels.
        y_tick_size (int): Font size for y-axis tick labels.

    Returns:
        plotly.graph_objs._figure.Figure: The updated Plotly figure.
    """
    fig.update_layout(
        xaxis={'tickfont': {'size': x_tick_size}}
    )

    return fig


def select_column_of_interest(columns, text="Select Column of Interest"):
    """UI component to choose a column of interest from columns(list)

    Args:
        columns (list): all the columns in a dataframe

    Returns: the user chose column
    """
    chosen_column = st.selectbox(text, columns)
    return chosen_column

templates = [
    'none', 'plotly_dark', 'plotly_white',
    'ggplot2', 'seaborn', 'simple_white', 'plotly',
    'presentation', 'xgridoff',
    'ygridoff', 'gridon'
]

def graph_theme():
    """UI component to select a graphing theme

    Returns: theme as a string
    """
    theme = st.selectbox(
            "Select a Graph Theme",
            templates
        )
    return theme

def select_number(text="Number of bins for the Histogram", val=4):
    num = st.number_input(text, value=val)
    return num

def checkbox(text, default=True):
    return st.checkbox(text, value=default)

def show_graph(fig):
    """Renders the Plotly Figure. Used to standardize the formatting

    Args:
        fig (plotly obj): a plotly figure object
    """
    st.write("---")
    st.plotly_chart(fig)

def set_theme(fig, theme):
    fig.update_layout(template=theme)
    return fig

def add_value_number_to_columns(fig):
    """added the count value to the bars in a plotly chart

    Args:
        fig (plotly obj): plotly obj

    Returns:
        fig (plotly obj): plotly obj
    """
    fig.update_traces(texttemplate = "%{y}")
    return fig

def reorder_xaxis(x: list, text: str = "Reorder X Axis Values (Drag and Drop)", ):
    """This is a componant to allow the user to rearrange the order of a list
    Uses:
        - reordering the labels on the xaxis
        - reorder the legend
    
    NOTE: If a list of numbers is given, the rearranging UI is not shown

    Args:
        x (list): a python list of items to rearrange
        text (str): the header description
        

    Returns:
        sorted_items (list): a rearranged list of the input
    """
    # Filter values. Remove all null values
    filtered_list = []
    for item in x:
        if (type(item) == str):
            if item.strip() in [np.nan, "", " "]:
                continue
        
        if item in [np.nan,]:
            continue

        # append the original item, important to make sure plotly works well
        filtered_list.append(item)

    if not is_list_of_numbers(filtered_list):
        items = [
            {'header': text,  'items': filtered_list}
        ]
        sorted_items = sort_items(items, multi_containers=True)
        
        # This returns the array because the `sorted_items` variables is a dictionary
        return sorted_items[0]["items"]
    else:
        # Should I return the filtered_list?
        return x

def is_list_of_numbers(string_list):
    """
    Checks if a list contains only elements that can be converted to numbers (integers or floats).

    Args:
        string_list: A list of strings.

    Returns:
        True if all elements are convertible to numbers, False otherwise.
    """
    try:
        for element in string_list:
            float(element)
        return True
    except ValueError:
        return False