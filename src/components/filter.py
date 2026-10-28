import streamlit as st
import src.components.chart_options as c #only need is_list_of_numbers function

def filter_discrete(df, colname, vals, inclusion):
    """Filters a dataframe based on a list of values from a column

    Returns: Filtered dataframe

    Args:
        df (pandas.Dataframe): data as pandas dataframe
        colname (string): name of column to filter data
        vals (list): the values from the column to filter dataframe with
        inclusion (bool): whether to include or exclude vals in dataframe   
    """

    if(inclusion):
        df_new = df[df[colname].isin(vals)]
    else:
        df_new = df[~(df[colname].isin(vals))]
   
    return df_new


def filter_cont(df, colname, vals, inclusion, endpt_inc):
    """Filters a dataframe based on the specified range of values from a column

    Returns: Filtered dataframe

    Args:
        df (pandas.Dataframe): data as pandas dataframe
        colname (string): name of column to filter data
        vals (list): list containing min and max value of specified range
        inclusion (bool): whether to include or exclude specified range in dataframe
        endpt_inc (bool): whether to include or exclude the endpoints from range
    """

    if(inclusion):
        df_new = df[(df[colname] >= vals[0]) & (df[colname] <= vals[1])]
    else:
        df_new = df[(df[colname] <= vals[0]) | (df[colname] >= vals[1])]

    if(endpt_inc == False):
        df_new = df_new[(df_new[colname] != vals[0]) & (df_new[colname] != vals[1])]
    
    return df_new


def filter_data(df, columns, session_state):
    """Creates UI to interact with and filters data

    Returns: filtered data

    Args:
        df (pandas.Dataframe): data to filter as pandas dataframe
        columns (list): dataframe column names
        session_state (streamlit Session State): Session State API for 'filter_list', check DSiMC_Tool.py for details
    """

    # Add 'None' option from name of columns
    new_cols = columns.copy()
    new_cols.insert(0, "None")

    # Check if any filters are added
    if(len(session_state.filter_list) == 0):
        df_new = df #Returns original dataframe if none
    else:
        for i in session_state.filter_list:

            # Each component of each filter requires a unique key
            # Just use a counter for now (surely someone won't add a max possible int worth of filters)
            remove_key = "remove" + str(i)
            chosen_col_key = "chosen_col" + str(i)
            selected_vals_key = "selected_vals" + str(i)
            include_vals_key = "include_vals" + str(i)
            choose_discrete_key = "choose_discrete" + str(i)
            min_val_key = "min_val" + str(i)
            max_val_key = "max_val" + str(i)
            include_endpt_key = "include_endpt" + str(i)

            # Initialize df_new at the start (df_new is inputted into filter functions)
            if(i == session_state.filter_list[0]):
                df_new = df

            # Create containers for each filter
            with st.container(border=True):
                cols = st.columns(2)
                val_cols = st.columns(2)
                cont_opt_cols = st.columns(2)

                # Option to choose column to filter data
                with cols[0]:
                    chosen_col = st.selectbox("Select column to filter", new_cols, key = chosen_col_key)
                
                # TODO: Removing filters using this does not work
                # Users can work around this by choosing 'None' for the filter column to ignore a certain filter 
                # (but the container will still remain, so may be inconvenient)
                with cols[1]:
                    if st.button("Remove", key = remove_key):
                        session_state.filter_list.remove(i)
                

                if(chosen_col != "None"):
                    vals = df_new[chosen_col].unique().tolist()

                    # If data type not numerical, use filter_discrete
                    if not c.is_list_of_numbers(vals):
                        selected_vals = st.multiselect("Choose values to include/exclude", options = vals, default = vals, key = selected_vals_key)

                        include_vals = not st.checkbox("Exclude chosen values", value = False, key = include_vals_key)

                        df_new = filter_discrete(df_new, chosen_col, selected_vals, include_vals)
                    
                    # If data numerical
                    else:
                        # Choose whether to use filter_discrete or filter_cont
                        choose_discrete = st.checkbox("Represent values discretely", value = False, key = choose_discrete_key)
                        
                        if(choose_discrete):
                            selected_vals = st.multiselect("Choose values to include/exclude", options = vals, default = vals, key = selected_vals_key)

                            include_vals = not st.checkbox("Exclude chosen values", value = False, key = include_vals_key)

                            df_new = filter_discrete(df_new, chosen_col, selected_vals, include_vals)
                        else:
                            with val_cols[0]:
                                min_val = st.number_input("Min", key = min_val_key)
                            with val_cols[1]:
                                max_val = st.number_input("Max", key = max_val_key)
                            with cont_opt_cols[0]:
                                include_endpt = st.checkbox("Include endpoints", value = True, key = include_endpt_key)
                            with cont_opt_cols[1]:
                                include_vals = not st.checkbox("Exclude chosen values", value = False, key = include_vals_key)
                            
                            df_new = filter_cont(df_new, chosen_col, [min_val, max_val], include_vals, include_endpt)

        # Display filtered dataframe
        st.write("### Resulting Dataset:")
        st.dataframe(df_new, height=200)
                    
    return df_new