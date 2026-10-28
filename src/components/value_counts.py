import plotly.express as px
import streamlit as st
import src.components.chart_options as c

def value_counts(df, columns):
    """This creates the UI to interact with and on submit will create a Value Count Charts. 
    
    This is ONLY for making Value Count Charts

    Args:
        df (pandas.DataFrame): the data as a pandas DataFrame
        columns (list): DataFrame columns names
    """
    
    with st.container(border=True):
        cols = st.columns(2)

        with cols[0]:
            chosen_column = c.select_column_of_interest(columns)
            theme = c.graph_theme()
            show_count_in_bar = c.checkbox("Show Count in Each Bar")

        with cols[1]:
            title, xaxis_label, yaxis_label, title_size, x_size, y_size = c.title_x_y_label()
        xaxis_order = c.reorder_xaxis(
            df[chosen_column].unique().tolist()
        )
        x_tick_size=c.x_tick_size()
        # button = st.button("Generate Graph")
    
    # TODO: Should this be under the control of the `button` above?
    # aka should you only make a graph once users click submit?
    if True:
        vc = df[chosen_column].value_counts()

        # Create the Graph
        b = px.bar(vc)

        # Custom Formatting
        b = c.set_title_x_y_label(b, title, xaxis_label, yaxis_label, title_size, x_size, y_size)
        b = c.set_theme(b, theme)
        b=c.set_x_tick_size(b, x_tick_size)
        if show_count_in_bar:
            b = c.add_value_number_to_columns(b)

        # Default Formatting
        if xaxis_order != False:
            b.update_xaxes(
                categoryorder="array",
                categoryarray=xaxis_order
            )
        # Will set this to False by default ... see no reason otherwise
        b.update_layout(showlegend=False)

        # The st.write below is to add space
        c.show_graph(b)
        
    return None