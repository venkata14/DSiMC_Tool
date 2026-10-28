import pandas as pd
import numpy as np
from scipy import stats
from sklearn import linear_model
import statsmodels.formula.api as smf
import streamlit as st
import src.components.chart_options as c
from scipy.stats import chi2_contingency


def summary_by_column(df):
    for i in df:
        st.write("Column Name: ", i)
        st.write(df[i].describe())


def summary_for_one_column(df, columns):
    column_name = st.selectbox("Choose the column you want to describe: ", [None]+ columns)
    if column_name:
        st.write(df[column_name].describe())


def t_test(df, columns):
    col1 = st.selectbox("what is the name of your first column? ", [None]+ columns)
    col2 = st.selectbox("what is the name of your second column? ", [None]+ columns)
    sig_input = st.number_input("what is the level of significance you want? ")
    
    sig_level = float(sig_input)
    independent = st.text_input(
        "are your samples independent? enter 'False' or 'True'. (False would run a Paired t-test.) "
    )
    if not independent:
        equalvar = st.text_input("are your variances equal?")
    Ha = st.text_input(
        "what is your alternative hypothesis? options: 'two-sided', 'less', 'greater' "
    )
    if ((col1 != None) & (col2 != None)):
        t_stat = 0.0
        p_value = 0.0
        if independent:
            t_stat, p_value = stats.ttest_ind(df[col1], df[col2], equal_var=equalvar, alternative=Ha)
        else:
            t_stat, p_value = stats.ttest_rel(df[col1], df[col2], alternative=Ha)
        st.write(f"t stat: {t_stat}; p value: {p_value}")
    
        if p_value < sig_level:
            if Ha == "two-sided":
                st.write(f"there is a significant difference between {col1} and {col2}")
            else:
                st.write(f"{col1} is {Ha} than {col2}")
        else:
            st.write(f"there is no significant difference between {col1} and {col2}")

# predictor_col - predictor (column NAME)
# binary_col - outcomes/response (column NAME)
# true_name - what outcome are you considering "true"?
# in_binary – is your binary variable already in 0/1 format?
def log_regression(df, columns):
    predictor_col = st.selectbox("what is the name of the column containing your predictor variable? ", [None]+ columns)
    
    binary_col = st.selectbox(
        "what is the name of the column containing your outcome/response variable? ", [None]+ columns)
    true_name = st.text_input(
        "what is the name of the outcome are you considering True? eg. true, 1, yes "
    )
    in_binary = st.text_input(
        "is your outcome variable already in 0/1 format? enter 'True' or 'False' "
    )

    df_copy = df

    if ((predictor_col != None) & (binary_col != None)):

        if not in_binary:
            # converting to binary data
            dummies = pd.get_dummies(df_copy[binary_col], dtype=int)
            df_copy = pd.concat(df_copy, dummies[true_name], axis=1)
            df_copy = df_copy.drop([binary_col], axis=1)
            df_copy = df_copy.rename(columns={true_name: binary_col})
    
        string_logit = binary_col + "~" + predictor_col
    
        reg = smf.logit(string_logit, data=df_copy).fit()
        st.write(reg.summary())
    
        # table of ORs, CIs
        params = reg.params
        conf = reg.conf_int()
        conf["OR"] = params
        np.exp(conf)
        conf["P Value"] = reg.pvalues
        conf.columns = ["Lower CI", "Upper CI", "OR", "P Value"]
        st.write(conf)
    
        # print interpretation: https://heds.nz/posts/logistic-regression-python/

def chi_square_test(df, columns):
    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    numeric_columns = df.select_dtypes(include=numerics).columns.values.tolist()
    numeric_columns = [None] + numeric_columns

    # Select column 1
    col1_name = c.select_column_of_interest(
        numeric_columns, text="Choose the first numerical column of Interest"
    )

    # Select column 2
    col2_name = c.select_column_of_interest(
        numeric_columns, text="Choose the second numerical column of Interest"
    )
    
    if ((col1_name != None) & (col2_name != None)):
        column1_data = df[col1_name].dropna()
        
        column2_data = df[col2_name].dropna()

        # Create contingency table
        contingency_table = pd.crosstab(column1_data, column2_data)

        # Perform chi-square test
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        # Print results
        st.write("Chi-square statistic:", chi2)
        st.write("p-value:", p)

        # Assumption is that data is independent of eachother


def paired_z_test(df, columns):
    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    numeric_columns = df.select_dtypes(include=numerics).columns.values.tolist()
    numeric_columns = [None] + numeric_columns

    # Select column 1
    col1_name = c.select_column_of_interest(
        numeric_columns, text="Choose the first numerical column of Interest"
    )

    # Select column 2
    col2_name = c.select_column_of_interest(
        numeric_columns, text="Choose the second numerical column of Interest"
    )
    
    if ((col1_name != None) & (col2_name != None)):
        data1 = df[col1_name].dropna()
        data2 = df[col2_name].dropna()

        # Ensure both columns have the same length after dropping NA
        if len(data1) != len(data2):
            raise ValueError(
                "Selected columns have different lengths after dropping NA values."
            )

        # Calculate the differences
        differences = data1 - data2

        # Calculate mean and standard deviation of the differences
        mean_diff = np.mean(differences)
        std_diff = np.std(differences, ddof=1)  # Sample standard deviation (ddof=1)

        # Number of pairs
        n = len(differences)

        # Calculate the Z-score
        z_score = mean_diff / (std_diff / np.sqrt(n))

        # Calculate the two-sided p-value
        p_value = 2 * (1 - stats.norm.cdf(np.abs(z_score)))

        # Print the results
        st.write("Z-score:", z_score)
        st.write("p-value:", p_value)

        # Return the results
        return z_score, p_value

        # Assumptions made: both sample populations have a normal distribution, samples are independent of each other
        # Recommended for sample size >=30
