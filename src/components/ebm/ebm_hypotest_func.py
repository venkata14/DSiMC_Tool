import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import math
from scipy import stats
import src.components.chart_options as c
import numpy as np
from src.components.ebm.ebm_epi_func import inc_prev_factors


# Visualization of type I error, type II error, and power
def hypo_test_demo1():
    with st.container(border=True):
        st.write('''Assume that the null and alternate hypothesis distributions are normal and both have SD of 1. 
                    The mean of the null hypothesis distribution is set to 0 for convenience.''')
        st.write("This exercise aims to visualize type I error, type II error, and power, and how they change with sample size and CI")


        mu_1 = st.select_slider("Select mean of H1 distribution",
            options=np.linspace(0.5, 1, 6), value = 0.5)

        N = st.select_slider("Select population size N",
            options=[1, 10, 30, 50, 70, 100], value = 30)
        
        CI = st.select_slider("Select CI",
            options=[80, 90, 95, 98, 99], value = 95)

    mu_0 = 0
    sd_0 = 1
    sd_1 = 1

    se_0 = sd_0/math.sqrt(N)
    se_1 = sd_1/math.sqrt(N)

    x_0 = np.arange(mu_0 - se_0*3, mu_0 + se_0*3, 0.005)
    x_1 = np.arange(mu_1 - se_1*3, mu_1 + se_1*3, 0.005)

    dst_0 = stats.norm(loc = mu_0, scale = se_0)
    dst_1 = stats.norm(loc = mu_1, scale = se_1)
    y_0 = dst_0.pdf(x_0)
    y_1 = dst_1.pdf(x_1)

    alpha = 1 - CI/100
    crit_val = dst_0.ppf(1-alpha)
    beta = dst_1.cdf(crit_val)

    plot_df = pd.DataFrame(dict(
        x0 = x_0,
        y0 = y_0,
        x1 = x_1,
        y1 = y_1
    ))

    df_fill_alpha = plot_df[plot_df['x0'] >= crit_val]
    df_fill_beta = plot_df[plot_df['x1'] <= crit_val]

    plt = go.Figure()
    plt.add_scatter(x = plot_df['x0'], y=plot_df['y0'], mode='lines', line_color='red', line_shape='spline', name = "H0")
    plt.add_scatter(x=plot_df['x1'], y=plot_df['y1'], mode='lines', line_color='blue', line_shape='spline', name = "H1")
    plt.add_trace(go.Scatter(x=df_fill_alpha['x0'], y=df_fill_alpha['y0'], mode='lines', fill='tozeroy', line_color = 'red', showlegend = False))
    plt.add_trace(go.Scatter(x=df_fill_beta['x1'], y=df_fill_beta['y1'], mode='lines', fill='tozeroy', line_color='blue', showlegend = False))
    plt.add_vline(x=crit_val)
    plt.update_yaxes(visible=False, showticklabels=False)
    st.plotly_chart(plt)

    st.write(r"$\text{Type I Error } (\alpha): $" + " " + str(round(alpha, 2)))
    st.write(r"$\text{Type II Error } (\beta): $" + " " + str(round(beta, 2)))
    st.write(r"$\text{CI } (1-\alpha): $" + " " + str(round(1-alpha, 2)))
    st.write(r"$\text{Power } (1-\beta): $" + " " + str(round(1-beta, 2)))

    st.subheader("Notes")
    st.write('''
    - Null hypothesis: No statistical difference between set of observations (difference due to chance)
    - Alternate hypothesis: Statistical difference exists between set of observations
    - Confidence interval (CI): Range of values that contain the true value of a statistic within a certain probability
    - Power: Probability of detecting a difference when it exists between a set of observations
    - Type I error: Mistakenly rejecting the null hypothesis when it is true
    - Type II error: Mistakenly accepting the null hypothesis when it is false

    In this visualization, we reject the null hypothesis if we are to the *right* of the vertical line, and we accept the null hypothesis if we are to the *left* of the vertical line.
    Then, the red area indicates type I error, while the blue area indicates type II error. 
    Changing the CI results in a trade-off between type I and II error, and increasing the sample size decreases type II error while not affecting type I error.
    ''')

    return None

# Visualization of CI and hypothesis testing
def hypo_test_demo2():
    np.random.seed(42)
    with st.container(border=True):
        st.write('''This exercise aims to visualize confidence intervals of two sample groups, 
                    how they relate to hypothesis testing, and how sample size and other factors could influence this process.''')

        mu_cols = st.columns(2)
        sd_cols = st.columns(2)

        with mu_cols[0]:
            mu_0 = st.number_input("Mean of population 1", value=0)
        with mu_cols[1]:
            mu_1 = st.number_input("Mean of population 2", value=1)

        with sd_cols[0]:
            sd_0 = st.number_input("SD of population 1", min_value=0, value=1)
        with sd_cols[1]:
            sd_1 = st.number_input("SD of population 2", min_value=0, value=1)

        N = st.slider("Select sample size N", 5, 50, 10)
        
        CI_set = st.select_slider("Select size of CI (%)",
            options=[80, 90, 95, 98, 99], value = 95)

        dst_0 = stats.norm(loc = mu_0, scale = sd_0)
        dst_1 = stats.norm(loc = mu_1, scale = sd_1)

        # Very dumb but couldn't think of a good way to resample so just doing this for now lol
        if st.button("Get new sample"):
            sample_0 = dst_0.rvs(size=N)
            sample_1 = dst_1.rvs(size=N)
        else:
            sample_0 = dst_0.rvs(size=N)
            sample_1 = dst_1.rvs(size=N)

    Z_dict = {
        80: 1.282,
        90: 1.645,
        95: 1.960,
        98: 2.326,
        99: 2.576
    }

    Z = Z_dict[CI_set]

    sample_mean_0 = np.mean(sample_0)
    sample_mean_1 = np.mean(sample_1)

    CI_upper_0 = sample_mean_0 + Z * sd_0/math.sqrt(N)
    CI_lower_0 = sample_mean_0 - Z * sd_0/math.sqrt(N)
    CI_upper_1 = sample_mean_1 + Z * sd_1/math.sqrt(N)
    CI_lower_1 = sample_mean_1 - Z * sd_1/math.sqrt(N)

    sample_df = pd.DataFrame(dict(
        group0 = sample_0,
        group1 = sample_1
    ))

    plot_sample_df = pd.melt(sample_df, value_vars = ['group0', 'group1'])
    plot_sample_df.loc[plot_sample_df['variable'] == 'group0', 'variable'] = 'Group 0'
    plot_sample_df.loc[plot_sample_df['variable'] == 'group1', 'variable'] = 'Group 1'

    plt_hold = px.strip(plot_sample_df, x = 'value', y = 'variable')
    plt_hold.update_traces(marker=dict(opacity=0.3))
    plt = go.Figure()
    plt.add_trace(plt_hold.data[0])
    plt.add_trace(go.Scatter(x = [CI_lower_0, CI_upper_0], y = ['Group 0', 'Group 0'], 
        mode='lines+markers', marker = dict(size = 12, symbol = 142), 
        line_color = "red", marker_color = "red", showlegend=False))
    plt.add_trace(go.Scatter(x = [CI_lower_1, CI_upper_1], y = ['Group 1', 'Group 1'], 
        mode='lines+markers', marker = dict(size = 12, symbol = 142), 
        line_color = "red", marker_color = "red", showlegend=False))

    st.plotly_chart(plt)

    if(CI_upper_0 >= CI_lower_1):
        st.write(r"$H_0$" + " is NOT rejected")
        st.write("The CIs between the two groups DO overlap, meaning results are NOT significant")
    else:
        st.write(r"$H_0$" + " is rejected")
        st.write("The CIs between the two groups DO NOT overlap, meaning results ARE significant")

    st.subheader("Notes")
    st.write('''
    *Note:* For each set of parameters, click on "Get new sample" several times to see if it generally accepts or rejects null hypothesis as exceptions can happen by chance.
    
    As we increase the sample size, the CI of both groups decreases, resulting in a less likely chance of CIs overlapping. Hence, there is a greater chance of rejecting the null hypothesis with increased sample size.
    ''')
    
    return None

def CI_samplesize_amolak():
    """
    Demonstrates how the confidence interval changes with increasing sample size
    for a normal distribution.
    """

    st.title('Confidence Interval and Sample Size')

    st.markdown("""Let's say we want to determine the average weight of 20-year-old males in the United States.
    It's not feasible to measure everybody's weight, so we approximate this value by considering a smaller sample from the population.
    As the sample size increases, the confidence interval (the range in which we expect the true mean to lie) becomes narrower, 
    providing a more accurate estimate of the population mean.
    """)

    true_mean = 170  # Average weight of 20 year old US adult males
    true_std = 30    # Standard deviation of weight
    
    # Create a slider to adjust the sample size N
    N = st.slider("Sample Size (N)", min_value=10, max_value=1000, 
                  value=50, step=10)
    
    # Randomly generate N samples from the normal distribution
    np.random.seed(42)
    sample = np.random.normal(loc=true_mean, scale=true_std, size=N)

    # Compute sample mean and confidence interval
    sample_mean = np.mean(sample)
    sample_std = np.std(sample, ddof=1)
    
    # Calculate the 95% confidence interval (CI)
    ci_lower = sample_mean - 1.96 * (sample_std / np.sqrt(N))
    ci_upper = sample_mean + 1.96 * (sample_std / np.sqrt(N))

    # Display the sample scatter plot
    fig1 = px.scatter(y=sample, title=f"Weight of 20 Year Old Men in the US N={N}", 
                      labels={"y": "Weight (lbs)", 'x': 'Sample Number'})
    st.plotly_chart(fig1)

    # Display the confidence interval on a separate graph
    st.subheader(f"Confidence Interval for the Mean Weight")
    fig2 = go.Figure()

    # Add a horizontal line for the true mean
    fig2.add_trace(go.Scatter(x=[0, 1], y=[true_mean, true_mean], 
                              mode='lines', name='True Mean', line=dict(color='green')))
    
    # Add a line for the sample mean with CI
    fig2.add_trace(go.Scatter(x=[0.5, 0.5], y=[ci_lower, ci_upper], 
                              mode='lines', name='95% CI', line=dict(color='blue', width=5)))
    
    # Show the sample mean
    fig2.add_trace(go.Scatter(x=[0.5], y=[sample_mean], mode='markers', 
                              name='Sample Mean', marker=dict(color='red', size=10)))

    # Update layout to make it clearer
    fig2.update_layout(
        title=f"Sample Mean and 95% Confidence Interval (N={N})",
        yaxis_title="Weight (lbs)",
        xaxis=dict(showticklabels=False),  # Hide x-axis labels since we're only showing 1 point
        yaxis=dict(range=[155,185])
    )
    
    st.plotly_chart(fig2)

    st.write(f"Sample Mean: {sample_mean:.2f} lbs")
    st.write(f"95% Confidence Interval: [{ci_lower:.2f}, {ci_upper:.2f}] lbs")
    st.write("""
### Observations:
- As the sample size increases, the confidence interval becomes narrower, indicating greater precision in estimating the population mean.
- You can adjust both the sample size to see how the interval changes dynamically.
""")

    return None

def bias():
    # SelectBox for selecting the bias concept
    concept = st.selectbox("Select a Bias Concept", ["Selection Bias", "Measurement Bias"])

    # Selection Bias Section
    if concept == "Selection Bias":
        import plotly.graph_objects as go
        
        np.random.seed(42)
        st.title("Understanding Selection Bias")
        
        st.write("Selection bias occurs when certain groups in a population are over or underrepresented.")
        
        # simulate a population with different groups
        population_size = 1000
        group1 = np.random.normal(loc=50, scale=10, size=population_size//2)
        group2 = np.random.normal(loc=70, scale=10, size=population_size//2)
        
        sample_size_group1 = st.slider("Sample Size for Group 1 (Mean = 50)", 0, population_size//2, population_size//4)
        sample_size_group2 = st.slider("Sample Size for Group 2 (Mean = 70)", 0, population_size//2, population_size//4)
        
        sample_group1 = np.random.choice(group1, size=sample_size_group1, replace=False)
        sample_group2 = np.random.choice(group2, size=sample_size_group2, replace=False)
        
        total_sample = np.concatenate([sample_group1, sample_group2])
        
        # I don't like this
        fig = go.Figure()

        # population groups
        fig.add_trace(go.Histogram(x=group1, opacity=0.5, name='Population Group 1', nbinsx=20))
        fig.add_trace(go.Histogram(x=group2, opacity=0.5, name='Population Group 2', nbinsx=20))

        # sample
        fig.add_trace(go.Histogram(x=total_sample, opacity=0.7, name='Sample', nbinsx=20))

        # Update the layout
        fig.update_layout(
            barmode='overlay',  # need this
            xaxis_title='Value',
            yaxis_title='Count',
            title='Population vs Sample Distribution',
            legend_title="Groups"
        )

        st.write(f"The mean of the sample is `{np.mean(total_sample):.2f}`, while the true population means are `50` and `70`.")

        # Plit
        st.plotly_chart(fig)

    # Measurement Bias Section. This could use improvement ? Ask Benjamins
    elif concept == "Measurement Bias":
        st.title("Understanding Measurement Bias")
        
        st.write("Measurement bias occurs when data collection tools or methods systematically affect the measurements.")
        
        # Simulate the bias
        np.random.seed(42)
        true_value = np.random.normal(loc=100, scale=5, size=100)
        measurement_error = st.slider("Measurement Error (%)", 0, 10, 5)
        measured_value = true_value + np.random.normal(loc=0, scale=measurement_error, size=100)
        
        # Need to make a DataFrame for Plotly to render a overlay
        df = pd.DataFrame(dict(
            series=np.concatenate((["True Value"] * len(true_value), ["Measured Value"] * len(measured_value))), 
            data=np.concatenate((true_value, measured_value))
        ))
        fig = px.histogram(df, x="data", color="series", barmode="overlay")
        fig.update_layout(
            xaxis_range=[75, 125],
            yaxis_range=[0, 25]
        )
        
        # Plot
        st.plotly_chart(fig)
        
    return None

def t_test():
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import ttest_ind, skewnorm

    np.random.seed(42)
    
    def generate_normal_data(mean, std, size):
        return np.random.normal(mean, std, size)

    def generate_skewed_data(mean, size, skewness):
        skewed_data = skewnorm.rvs(skewness, size=size)
        # Scale to match the desired mean
        scaled_data = (skewed_data - np.mean(skewed_data)) / np.std(skewed_data)
        scaled_data = scaled_data * np.std(skewed_data) + mean
        return scaled_data

    def plot_distributions(normal_data, skewed_data, skewness):
        plt.figure(figsize=(10, 6))
        plt.hist(normal_data, bins=30, alpha=0.6, label='Normal Data', color='blue')
        plt.hist(skewed_data, bins=30, alpha=0.6, label=f'Skewed Data (skew={skewness})', color='red')
        plt.axvline(np.mean(normal_data), color='blue', linestyle='dashed', linewidth=2)
        plt.axvline(np.mean(skewed_data), color='red', linestyle='dashed', linewidth=2)
        plt.legend()
        plt.title("Normal vs Skewed Data")
        st.pyplot(plt)

    st.title("T-Test Demo: Normality Assumption and Skewness Impact")

    mean = st.slider("Mean of both datasets", 0.0, 10.0, 5.0)
    sample_size = st.slider("Sample Size", 10, 5000, 600)
    skewness = st.slider("Skewness for Skewed Data", -100.0, 100.0, 0.0)

    normal_data = generate_normal_data(mean, 1, sample_size)
    # normal_data = generate_skewed_data(mean, sample_size, -skewness)
    skewed_data = generate_skewed_data(mean, sample_size, skewness)

    t_stat, p_value = ttest_ind(normal_data, skewed_data)

    # Show the t-test results
    st.write(f"**T-Test Results**")
    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"P-value: {p_value:.4f}")
    if p_value < 0.05:
        st.write("**Conclusion: Reject the null hypothesis (significant difference)**")
    else:
        st.write("**Conclusion: Fail to reject the null hypothesis (no significant difference)**")

    plot_distributions(normal_data, skewed_data, skewness)


def remove_trace_by_name(fig, trace_name):
    fig.data = [trace for trace in fig.data if trace.name != trace_name]


def plot_samples(fig, samples_dict):
    for patient, data in samples_dict.items():
        # Plot line
        fig.add_trace(go.Scatter(
            x=[data['start_time'], data['end_time']],
            y=[patient, patient],
            mode='lines',
            name=f'Patient{patient}',
            line=dict(color='black', width=2),
            showlegend=False
        ))

        # Plot black dot at start_time (diagnosis)
        fig.add_trace(go.Scatter(
            x=[data['start_time']],
            y=[patient],
            mode='markers',
            name=f'Start{patient}',
            marker=dict(color='black', size=10, symbol='circle'),
            showlegend=False
        ))

        # Plot green dot or red "X" at end_time based on outcome
        if data['outcome'] == 'cured':
            fig.add_trace(go.Scatter(
                x=[data['end_time']],
                y=[patient],
                mode='markers',
                name=f'End{patient}',
                marker=dict(color='green', size=10, symbol='circle'),
                showlegend=False
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[data['end_time']],
                y=[patient],
                mode='markers',
                name=f'End{patient}',
                marker=dict(color='red', size=12, symbol='x'),
                showlegend=False
            ))


def update_fig_end_time(fig, samples_dict, patient_num, new_value):
    if samples_dict[patient_num]['end_time'] < new_value:
        remove_trace_by_name(fig, f'Patient{patient_num}')
        remove_trace_by_name(fig, f'Start{patient_num}')
        remove_trace_by_name(fig, f'End{patient_num}')
    else:
        remove_trace_by_name(fig, f'End{patient_num}')
    return


def inc_prev():
    """
    Demonstrates incidence and prevalence rates.
    """
    st.write('# Incidence and Prevalence')
    st.write('## _Demo to learn Incidence and Prevalence_')

    st.markdown("""Consider this simplified example of 5 new cases of a viral illness in a population 
                of 20 people. Each horizontal line represents one person.""")
    st.markdown('<span style="color:black; font-weight:bold">Black Dot</span> - Date of disease onset', 
                unsafe_allow_html=True)
    st.markdown('<span style="color:green; font-weight:bold">Green Dot</span> - Date of recovery', 
                unsafe_allow_html=True)
    st.markdown('<span style="color:red; font-weight:bold">Red X</span> - Date of death', 
                unsafe_allow_html=True)

    SAMPLES_DICT = {
        1: {'start_time': 450, 'end_time': 750, 'outcome': 'cured'},
        2: {'start_time': 300, 'end_time': 500, 'outcome': 'passed'},
        3: {'start_time': 100, 'end_time': 625, 'outcome': 'cured'},
        4: {'start_time': 250, 'end_time': 700, 'outcome': 'passed'},
        5: {'start_time': 150, 'end_time': 900, 'outcome': 'cured'}
    }
    N_samples=len(SAMPLES_DICT.keys())

    fig1 = go.Figure()

    # Add horizontal lines at specific x positions corresponding to the years
    for x_val in [200, 400, 600, 800]:
        fig1.add_shape(
            type="line",
            x0=x_val, y0=0,
            x1=x_val, y1=10,  # Ending point of the line
            line=dict(color="Blue", width=1),
            name=f'Horiz{x_val}'
        )
    plot_samples(fig1,SAMPLES_DICT)

    fig1.update_layout(
        title="Viral Cases",
        xaxis_title="Years",
        yaxis_title="Person #",
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 200, 400, 600, 800, 1000],
            ticktext=['2019', '2020', '2021', '2022', '2023','2024'],
            range=[0, 1000]
        ),
        yaxis=dict(            
            tickmode='array',
            tickvals=list(range(1,6)),
            ticktext=list(range(1,6)),
            range=[1-.25,N_samples+.25]
            )
    )
    
    st.plotly_chart(fig1)

    with st.expander("Explanation for Point Prevalence, Period Prevalence and Incidence of the above Graph"):
        st.markdown('### **Prevalence**')
        st.markdown("""<p style="font-size:20px;"><strong>Point prevalence</strong> is the proportion 
                    of people with a disease at a particular time point:</p>""", unsafe_allow_html=True)
        st.latex(r"\mathbf{Point  Prevalence} = \frac{\mathbf{\# \text{ of people with disease at a particular\
                time point}}}{\mathbf{\# \text{ of people in population at a particular time point}}}")
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown("""As an exercise, let's calculate the prevalence of the viral illness 
                    at the beginning of 2022:""")
        
        info_latex = r"\text{Point Prevalence Jan 1st, 2022} = \frac{\text{4 (\# alive at beginning of\
                2022)}}{\text{20 (initial population size) - 1 (1 person died before 2022)}} = \
                \frac{\text{4}}{\text{19}} = 21\%"
        st.write(f"${info_latex}$")
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown("""<p style="font-size:20px;"><strong>Period prevalence</strong> is the proportion 
                    of people with a disease over a particular time period.</p>""", unsafe_allow_html=True)
        st.latex(r"\text{Period Prevalence 2019-2024} = \frac{\mathbf{\text{5}}}{\mathbf{\text{20}}} = 25\%")


        st.markdown('### **Incidence**')
        st.markdown("""<p style="font-size:20px;"><strong>Incidence</strong> is the occurence of NEW cases  
                    in a population over a period of time:</p>""", unsafe_allow_html=True)
        st.latex(r"\mathbf{Incidence} = \frac{\mathbf{\# \text{ of NEW cases over a period of time}}}{\mathbf{\# \text{ of disease free people}}}")
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown("""The incidence of the viral illness between 2020 and 2021 can be calculated as 
                    follows:""")
        info_latex_1 = r"\text{Incidence 2020-2021} = \frac{\text{2 (\# who contracted virus between 2020\
                and 2021)}}{\text{20 (initial population size) - 2 (2 people already contracted\
                the virus before 2020)}} = \frac{\text{2}}{\text{18}} = 11.1\%"
        st.write(f'${info_latex_1}$')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        
    with st.container(border=True):
        st.markdown('### **Factors Affecting Incidence and Prevalence**')
        st.markdown("""Various factors can affect incidence and prevalence. Select a factor 
                    to see it's impact:""")


        # Add buttons for interactive factor selection
        increase_survival=st.button("Increased Survival Time")
        increase_mortality = st.button("Increased Mortality")
        increase_recovery = st.button("Decreased (Faster) Recovery Time / Increased Efffective Treatment")
        increase_vaccine_coverage = st.button("Increased Vaccine Coverage")
        increase_cases = st.button("Increased Risk Factors / Diagnostic Sensitivity")


    if increase_survival:
        fig2 = go.Figure(fig1.to_dict())

        passed_pts=[2,4]
        for pt in passed_pts:
            remove_trace_by_name(fig2, f'End{pt}')
            new_end_time=SAMPLES_DICT[pt]['end_time']+150
            fig2.add_trace(go.Scatter(
                x=[SAMPLES_DICT[pt]['end_time'], new_end_time], 
                y=[pt, pt],
                mode='lines',
                name=f'Patient{pt}_longer',
                line=dict(color='black', width=2, dash='dash'),
                showlegend=False
            ))
            fig2.add_trace(go.Scatter(
                x=[new_end_time],
                y=[pt],
                mode='markers',
                name=f'End{pt}',
                marker=dict(color='red', size=12, symbol='x'),
                showlegend=False
            ))
        st.plotly_chart(fig2)
        with st.container(border=True):
            st.markdown('### **Increasing Survival Time Increases Prevalence**')
            st.markdown("""Notice patients 2 and 4 now live longer. Let\'s recalculate the point prevalence
                        at the beginning of 2022:""")
            st.latex(r"\text{Point Prevalence Jan 1st, 2022} = \frac{\text{5}}{\text{20}} = 25\%")
            st.markdown("""All patients are now living at the beginning of 2022. <strong>Point 
                        prevalence has increased</strong> from 21 to 25\%!""", unsafe_allow_html=True)
            st.markdown("""The number of new cases has not changed, so <strong>incidence remains 
                        unchanged.</strong>""", unsafe_allow_html=True)


    if increase_mortality:
        fig2 = go.Figure(fig1.to_dict())
        pt=3
        remove_trace_by_name(fig2, f'End{pt}')
        remove_trace_by_name(fig2, f'Patient{pt}')
        new_end_time=SAMPLES_DICT[pt]['end_time']-75
        fig2.add_trace(go.Scatter(
            x=[SAMPLES_DICT[pt]['start_time'], new_end_time], 
            y=[pt, pt],
            mode='lines',
            name=f'Patient{pt}_longer',
            line=dict(color='black', width=2),
            showlegend=False
        ))
        fig2.add_trace(go.Scatter(
            x=[new_end_time, SAMPLES_DICT[pt]['end_time']], 
            y=[pt, pt],
            mode='lines',
            name=f'Patient{pt}_longer',
            line=dict(color='black', width=2, dash='dash'),
            showlegend=False
        ))
        fig2.add_trace(go.Scatter(
            x=[new_end_time],
            y=[pt],
            mode='markers',
            name=f'End{pt}',
            marker=dict(color='red', size=12, symbol='x'),
            showlegend=False
        ))          
        st.plotly_chart(fig2)
        with st.container(border=True):
            st.markdown('### **Increasing Mortality Decreases Prevalence**')
            st.markdown("""Notice patient 3 now does not recover from illness, and has passed away a bit sooner. \
                        Let\'s recalculate the point prevalence at the beginning of 2022:""")
            st.latex(r"\text{Point Prevalence Jan 1st, 2022} = \frac{\text{3}}{\text{18}} = 16.7\%")
            st.markdown("""The numerator and denominator both decrease by one as there is one fewer case
                        at the beginning of 2022. <strong>Point 
                        prevalence has decreased!</strong>""", unsafe_allow_html=True)
            st.markdown("""The number of new cases has not changed, so <strong>incidence remains 
                        unchanged.</strong>""", unsafe_allow_html=True)


    if increase_recovery:
        fig2 = go.Figure(fig1.to_dict())
        for pt in [1,3,5]:
            remove_trace_by_name(fig2, f'End{pt}')
            remove_trace_by_name(fig2, f'Patient{pt}')
            new_end_time=SAMPLES_DICT[pt]['end_time']-80
            fig2.add_trace(go.Scatter(
                x=[SAMPLES_DICT[pt]['start_time'], new_end_time], 
                y=[pt, pt],
                mode='lines',
                name=f'Patient{pt}_longer',
                line=dict(color='black', width=2),
                showlegend=False
            ))
            fig2.add_trace(go.Scatter(
                x=[new_end_time, SAMPLES_DICT[pt]['end_time']], 
                y=[pt, pt],
                mode='lines',
                name=f'Patient{pt}_longer',
                line=dict(color='black', width=2, dash='dash'),
                showlegend=False
            ))
            fig2.add_trace(go.Scatter(
                x=[new_end_time],
                y=[pt],
                mode='markers',
                name=f'End{pt}',
                marker=dict(color='green', size=12, symbol='circle'),
                showlegend=False
            ))          
        st.plotly_chart(fig2)
        with st.container(border=True):
            st.markdown('### **Decreasing Recovery Time or Making Treatment More Effective Decrease Prevalence**')
            st.markdown("""Notice the pateints who recovered now recover faster. \
                        Let\'s recalculate the point prevalence at the beginning of 2022:""")
            st.latex(r"\text{Point Prevalence Jan 1st, 2022} = \frac{\text{3}}{\text{18}} = 16.7\%")
            st.markdown("""The numerator and denominator both decrease by one as there is one fewer case
                        at the beginning of 2022. <strong>Point 
                        prevalence has decreased!</strong>""", unsafe_allow_html=True)
            st.markdown("""The number of new cases has not changed, so <strong>incidence remains 
                        unchanged.</strong>""", unsafe_allow_html=True)
        

    if increase_vaccine_coverage:
        fig2 = go.Figure(fig1.to_dict())
        pt=3
        remove_trace_by_name(fig2, f'End{pt}')
        remove_trace_by_name(fig2, f'Patient{pt}')
        remove_trace_by_name(fig2, f'Start{pt}')

        st.plotly_chart(fig2)
        with st.container(border=True):
            st.markdown('### **Increasing Vaccine Coverage Decreases Both Incidence and Prevalence**')
            st.markdown("""Due to increased protection, patient 3 never aquires the infection. \
                        Let\'s recalculate the point prevalence at the beginning of 2022:""")
            st.latex(r"\text{Point Prevalence Jan 1st, 2022} = \frac{\text{3}}{\text{19}} = 15.8\%")
            st.markdown("""The numerator decreased by 1 as there is one fewer case
                        at the beginning of 2022. <strong>Point prevalence has decreased!</strong>""", 
                        unsafe_allow_html=True)
            st.markdown("""Since the number of new cases decreased by 1, <strong>incidence also decreases.</strong>""", 
                        unsafe_allow_html=True)
            info_latex_2 = r"\text{Incidence 2020-2021} = \frac{\text{2 (\# who contracted virus between 2020\
                and 2021)}}{\text{20 (initial population size) - 1 (now, only 1 person already contracted\
                the virus before 2020)}} = \frac{\text{2}}{\text{19}} = 10.5\%"
            st.write(f"${info_latex_2}$")

    if increase_cases:
        fig2 = go.Figure(fig1.to_dict())
        more_pts = {
            6: {'start_time': 500, 'end_time': 700, 'outcome': 'cured'},
            7: {'start_time': 50, 'end_time': 500, 'outcome': 'cured'},
        }
        plot_samples(fig2,more_pts)
        fig2.update_layout(
            yaxis=dict(            
                tickmode='array',
                tickvals=list(range(1,8)),
                ticktext=list(range(1,8)),
                range=[1-.25,7+.25]
                )
        )
        st.plotly_chart(fig2)

        with st.container(border=True):
            st.markdown('### **Increasing Risk Factors or Diagnostic Sensitivity Increases Both Incidence and Prevalence**')
            st.markdown("""With more risk factors, individuals are more likely to contract disease. If diagnostic sensitivity
                        increases, more cases will be detected. In both scenarios, more individuals from a population will 
                        be identified as aquiring and living with the disease. Note that 2 more individuals 
                        (Persons 6 & 7) from our population contracted illness.
                        Let\'s recalculate the point prevalence at the beginning of 2022:""")
            st.latex(r"\text{Point Prevalence Jan 1st, 2022} = \frac{\text{5}}{\text{19}} = 26.3\%")
            st.markdown("""The numerator increased by 1 as there is one more case
                        at the beginning of 2022. <strong>Point prevalence has increased!</strong>""", 
                        unsafe_allow_html=True)
            st.markdown("""Since there are more new cases, <strong>incidence also increases.</strong> The additional case
                        that occured before 2020 decreases the denominator, increasing incidence.""", 
                        unsafe_allow_html=True)
            info_latex_3 = r"\text{Incidence 2020-2021} = \frac{\text{2 (\# who contracted virus between 2020\
                and 2021)}}{\text{20 (initial population size) - 3 (now, 3 people already contracted\
                the virus before 2020)}} = \frac{\text{2}}{\text{17}} = 11.7\%"
            st.write(f"${info_latex_3}$")

    st.write("""
             
             #### _End of Demo to learn Incidence and Prevalence_
             
             ---
             ## _Playing around with Factors affecting Incidence and Prevalance_
             """)
    inc_prev_factors()
    return None
