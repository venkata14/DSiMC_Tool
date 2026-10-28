import plotly.express as px
import streamlit as st
import src.components.chart_options as c
import statsmodels.api as sm
import plotly.graph_objects as go
import pandas as pd


def calc_lin_reg(X, y):
    
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)

    params = model.params
    if len(params) != 2:
        return None, None, None, None, None
    intercept, slope = params
    r_squared = model.rsquared
    p_value = model.f_pvalue

    return intercept, slope, r_squared, p_value, predictions


def plot_lin_reg(fig, df, x, y):
    df[x] = pd.to_numeric(df[x], errors='coerce')
    df[y] = pd.to_numeric(df[y], errors='coerce')
    df = df.dropna(subset=[x,y])
    if len(df) < 2:
        return fig

    X = df[x].values
    Y = df[y].values

    intercept, slope, r_squared, p_value, predictions = calc_lin_reg(X,Y)
    if predictions is not None:
        fig.add_trace(go.Scatter(x=df[x], y=predictions, mode='lines', 
                                name=f'y = {intercept:.2f} + {slope:.2f}x', 
                                line=dict(color='red')))
        if p_value < 0.001:
            p_value = '< 0.001'
            fig.add_annotation(
                xref="paper", yref="paper",
                x=0.95, y=0.95,
                text=f'R² = {r_squared:.2f}, p = {p_value:}',
                showarrow=False,
                bordercolor="black",
                borderwidth=1
            )
        else:
                fig.add_annotation(
                xref="paper", yref="paper",
                x=0.95, y=0.95,
                text=f'R² = {r_squared:.2f}, p = {p_value:.3f}',
                showarrow=False,
                bordercolor="black",
                borderwidth=1
            )
    return fig


def scatter(df, columns):
    """This creates the UI to interact with and on submit will create a scatter plot. 

    Args:
        df (pandas.DataFrame): the data as a pandas DataFrame
        columns (list): DataFrame columns names
    """
    with st.container(border=True):
        cols = st.columns(2)

        with cols[0]:
            x = c.select_column_of_interest(columns, text="Select x axis")
            y = c.select_column_of_interest(columns, text="Select y axis")
            color_code = c.select_column_of_interest([None,] + (columns), 
                                                     text="Select color coding (optional)")

            theme = c.graph_theme()
        
        with cols[1]:
            title, xaxis_label, yaxis_label = c.title_x_y_label()
            plot_reg = c.checkbox("Plot regression line")

    if True:
        color_map = {}
        if color_code is not None:
            unique_values = df[color_code].unique()
            for value in unique_values:
                color_map[value] = st.color_picker(f"Pick a color for {value}", "#000000")
            b = px.scatter(df, x=x, y=y, color=color_code, color_discrete_map=color_map)
        else:
            b = px.scatter(df, x=x, y=y)

        b = c.set_title_x_y_label(b, title, xaxis_label, yaxis_label)
        b = c.set_theme(b, theme)

        if plot_reg:
            b = plot_lin_reg(b, df, x, y)

        c.show_graph(b)

    return None