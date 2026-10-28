import plotly.express as px
import streamlit as st
import src.components.chart_options as c

def grouped(df, columns):
    """This creates the UI to interact with and on submit will create a Grouped graphs. 
    
    This is ONLY for making Grouped graphs

    Args:
        df (pandas.DataFrame): the data as a pandas DataFrame
        columns (list): DataFrame columns names
    """
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    numeric_columns = df.select_dtypes(include=numerics).columns.values.tolist()
    stats_list = ["mean", "median", "prod", "sum", "std", "var"]

    with st.container(border=True):
        cols = st.columns(2)
    
        with cols[0]:
            chosen_column = c.select_column_of_interest(columns)
            group_column_of_interest = c.select_column_of_interest(numeric_columns, text="Choose the numerical column of Interest")
            group_analysis_of_interest = c.select_column_of_interest(stats_list, "Choose stat method")
            theme = c.graph_theme()
        
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
        if chosen_column and group_column_of_interest and (chosen_column is not group_column_of_interest):
            group_df = df.groupby([chosen_column])
            q = group_df[group_column_of_interest].agg([group_analysis_of_interest])
            
            # Create the Graph
            b = px.bar(q)
            
            # Custom Formatting
            b = c.set_title_x_y_label(b, title, xaxis_label, yaxis_label, title_size, x_size, y_size)
            b=c.set_x_tick_size(b, x_tick_size)

            b = c.set_theme(b, theme)
            b = c.add_value_number_to_columns(b)

            # Default Formatting
            if xaxis_order != False:
                b.update_xaxes(
                    categoryorder="array",
                    categoryarray=xaxis_order
                )
            b.update_layout(showlegend=False)

            c.show_graph(b)
        else:
            if not (chosen_column):
                st.write("Error: 'Select Column of Interest' is not chosen")
            elif not (group_analysis_of_interest):
                st.write("Error: There are no 'numerical column' to select")
            elif not (numeric_columns):
                st.write("Error: There are no column that is 'numerical' to select to do the grouped analysis. If you believe this is a mistake, please contact the DSiMC team.")
            elif not (chosen_column is not group_column_of_interest):
                st.write("Error: 'Select Column to Group' and 'Numerical Column of Interest' cannot be the same.")
            else:
                st.write("We're sorry, an error occurred. Please contact the DSiMC team.")
        
    return None