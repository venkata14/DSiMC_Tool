import plotly.express as px
import streamlit as st
import src.components.chart_options as c

def histogram(df, columns):
    """This creates the UI to interact with and on submit will create a histogram. 
    
    This is ONLY for making histograms

    Args:
        df (pandas.DataFrame): the data as a pandas DataFrame
        columns (list): DataFrame columns names
    """
    with st.container(border=True):
        cols = st.columns(2)

        with cols[0]:
            chosen_column = c.select_column_of_interest(columns)
            hist_highlight = c.select_column_of_interest([None,] + (columns), text="Layer Another Column")
            nbins = c.select_number()
            theme = c.graph_theme()
        
        with cols[1]:
            title, xaxis_label, yaxis_label, title_size, x_size, y_size = c.title_x_y_label()
            show_count_in_bar = c.checkbox("Show Count in Each Bar")

        xaxis_order = c.reorder_xaxis(
            df[chosen_column].unique().tolist()
        )
        x_tick_size=c.x_tick_size()
        # TODO: Explain this
        if hist_highlight is not None:
            legend_order = c.reorder_xaxis(
                df[hist_highlight].unique().tolist(),
                text="Reorder the Legend Values (Drag and Drop)"
            )
        # button = st.button("Generate Graph")
    
    # TODO: Should this be under the control of the `button` above?
    # aka should you only make a graph once users click submit?
    if True:
        # Create the Graph. I DO not like this solution
        # But unable to figure out a way to have `category_orders` as a fig.update_layout method
        if hist_highlight is not None:
            b = px.histogram(df, x=chosen_column, nbins=nbins, color=hist_highlight, category_orders={hist_highlight: legend_order})
        else:
            b = px.histogram(df, x=chosen_column, nbins=nbins, color=hist_highlight)
        
        # Custom Formating
        b = c.set_title_x_y_label(b, title, xaxis_label, yaxis_label, title_size, x_size, y_size)
        b = c.set_theme(b, theme)
        b=c.set_x_tick_size(b, x_tick_size)
        if show_count_in_bar:
            b = c.add_value_number_to_columns(b)

        # Default Formatting
        # TODO Make this reactive
        b.update_layout(bargap=0.02)
        if xaxis_order != False:
            b.update_xaxes(
                categoryorder="array",
                categoryarray=xaxis_order
            )
        b.update_layout(legend_traceorder="normal")

        # The st.write below is to add space
        c.show_graph(b)

    return None