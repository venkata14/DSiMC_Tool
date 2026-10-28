import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import math
from scipy import stats
from scipy.stats import norm
import src.components.chart_options as c
import numpy as np


def diagnostic_two_by_two_table(TP, FP, FN, TN, col_name1='Condition Present',
                                col_name2='Condition Absent', row_name1='Test Positive',
                                row_name2='Test Negative', display_eqns=False):
    col_name1 = col_name1
    col_name2 = col_name2
    row_name1 = row_name1
    row_name2 = row_name2

    TP_styled = f"<span style='color:red;'>{TP}</span>"
    FP_styled= f"<span style='color:blue;'>{FP}</span>"
    FN_styled=f"<span style='color:purple;'>{FN}</span>"
    TN_styled=f"<span style='color:green;'>{TN}</span>"

    if display_eqns:
        PPV_eqn=f'<b>PPV</b> = {TP_styled} / ({TP_styled} + {FP_styled})'
        NPV_eqn=f'<b>NPV</b> = {TN_styled} / ({TN_styled} + {FN_styled})'
        sens_eqn=f'<b>Sensitivity</b> = {TP_styled} / ({TP_styled} + {FN_styled})'
        spec_eqn=f'<b>Specificity</b> = {TN_styled} / ({TN_styled} + {FP_styled})'
    
        data = [
            [TP_styled, FP_styled, PPV_eqn],
            [FN_styled, TN_styled, NPV_eqn],
            [sens_eqn, spec_eqn, ''],
        ]
        df = pd.DataFrame(data, index=[row_name1, row_name2, ''], columns=[col_name1, col_name2, ''])
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

    else:
        data = [
            [TP_styled, FP_styled],
            [FN_styled, TN_styled]
        ]
        df = pd.DataFrame(data, index=[row_name1, row_name2], columns=[col_name1, col_name2])
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

    return df





def interactive_2x2_table():
    """Interactive 2x2 table for sensitivity and specificity visualization."""
    
    placeholder = st.empty()
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        placeholder1 = st.empty()

    placeholder2 = st.empty()
    
    # Inputs for row and column names
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Rename Table Labels")
        row_name1 = st.text_input("Row 1 Name (e.g., 'Condition Present')", value="Condition Present")
        row_name2 = st.text_input("Row 2 Name (e.g., 'Condition Absent')", value="Condition Absent")
        col_name1 = st.text_input("Column 1 Name (e.g., 'Test Positive')", value="Test Positive")
        col_name2 = st.text_input("Column 2 Name (e.g., 'Test Negative')", value="Test Negative")
    with col2:
        # Inputs for table values
        st.markdown("### Enter Table Values")
        TP = st.number_input(f"{row_name1}, {col_name1}", min_value=0, value=50)
        FN = st.number_input(f"{row_name1}, {col_name2}", min_value=0, value=10)
        FP = st.number_input(f"{row_name2}, {col_name1}", min_value=0, value=5)
        TN = st.number_input(f"{row_name2}, {col_name2}", min_value=0, value=100)

    # Create a pandas DataFrame to represent the table
    data = {
        col_name1: [TP, FP],
        col_name2: [FN, TN]
    }
    df = pd.DataFrame(data, index=[row_name1, row_name2])

    # Display the table
    placeholder.markdown("### 2x2 Contingency Table")
    placeholder1.dataframe(df.style.format("{:.0f}"))

    # Additional metrics
    sensitivity = TP / (TP + FN) if TP + FN > 0 else 0
    specificity = TN / (TN + FP) if TN + FP > 0 else 0
    placeholder2.markdown("### Metrics" + f"\n**Sensitivity:** `{sensitivity:.2f}` & **Specificity:** `{specificity:.2f}`")


def sens_spec():
    st.write('# Sensitivity, Specificity, Negative Predictive Value (NPV),\
             and Positive Predictive Value (PPV)')
    st.write('Understanding sensitivity, specificity, NPV and PPV are vital\
              to evaluating diagnostic tests. Calculations involving 2x2\
              tables are also frequently tested on STEP exams.')
    st.write('Sensitivity and specificity are fixed properties of a\
              diagnostic test, while PPV and NPV depend on the disease prevalence\
              in a population. This will become more clear as you\
              work through the examples below. The table below\
              shows how each metric is calculated.')
    
    diagnostic_two_by_two_table('TP', 'FP', 'FN', 'TN', display_eqns=True)

    st.write('## Sensitivity and Specificity')
    st.markdown('<b>Sensitivity (True Positive Rate):</b> The proportion\
              of all people with disease who test positive. It refers to\
              the ability of a test to correctly identify those with disease.',
                unsafe_allow_html=True)
    st.markdown('- Sensitivity approaching 100% indicates a low false negative rate.\
                 This is desirable for ruling out disease, which is why highly\
                 sensitive tests are used for screening. A helpful mnemonic is \
                SN-N-OUT (a test is highly SeNsitive when a Negative rules disease OUT).')

    st.markdown('<b>Specificity (True Negative Rate):</b> The proportion of all people\
                 without disease who test negative. It refers to the ability\
                 of a test to correctly identify those without disease.',
                 unsafe_allow_html=True)
    st.markdown('- Specificity approaching 100% indicates a low false positive rate.\
                 This is desirable for ruling in disease, which is why highly\
                 specific tests are used for confirmation after positive screening. \
                A helpful mnemonic is SP-P-IN (a highly SPecific test when Positive rules IN disease).')




    st.write('## Positive and Negative Predictive Values')

    st.markdown('<b>Pretest probability of disease</b> refers to the\
                 probability of one having disease before a test is\
                 performed. It increases when an individual has certain\
                 risk factors for developing disease and when the disease\
                 is more prevalent. PPV and NPV are dependent on pretest\
                 probability.', unsafe_allow_html=True)
    
    st.markdown('<b>Positive Predictive Value:</b> Probability that a person who\
                 tested positive actually has the disease.', unsafe_allow_html=True)
    st.markdown('- PPV varies directly with pretest probability (i.e.\
                 PPV is greater when a disease is more prevalent).')
    with st.expander("Click for explanation"):
        st.markdown("""
        This can be inferred from how PPV is calculated. Recall:
        
        **PPV = TP / (TP + FP)**
        
        When a disease is more prevalent, there will be more True Positives (TP)
        relative to False Positives (FP), increasing PPV.
        """)
    
    st.markdown('<b>Negative Predictive Value:</b> Probability that \
                a person who tested negative actually does not have\
                 disease.', unsafe_allow_html=True)
    st.markdown('- NPV varies inversely with pretest probability (i.e.\
                 NPV is greater when a disease is less prevalent).')
    with st.expander("Click for explanation"):
        st.markdown("""
        This can be inferred from how NPV is calculated. Recall:
        
        **NPV = TN / (TN+FN)**
        
        When a disease is less prevalent, there will be more TN relative \
        to FN, increasing NPV.
        """)



    st.write('## The Tradeoff Between Sensitivity and Specificity')
    st.markdown('In reality, there is a practical compromise between \
                the sensitivity and specificity of a diagnostic test. \
                Increasing sensitivity decreases specificity and vice versa.')

    fig1=go.Figure()
    B = st.slider("B", min_value=-1.5, max_value=1.5, value=0.0, step=0.1)

    def plot_normal_dist(fig, mu, curve_name='', color='black', sigma=1):
        x = np.linspace(mu-3*sigma, mu+3*sigma, 1000)
        y = norm.pdf(x, mu, sigma)

        fig.add_trace(go.Scatter(
            x=x,y=y,
            mode='lines',
            name=curve_name,
            line=dict(color=color)
        ))
        return fig


    def highlight_FN_and_FPs(fig, mu_smaller, mu_larger, B, sigma=1):
        x_abs = np.linspace(mu_smaller-3*sigma, mu_smaller+3*sigma, 1000)
        x_pres = np.linspace(mu_larger-3*sigma, mu_larger+3*sigma, 1000)
        y_abs = norm.pdf(x_abs, mu_smaller, sigma)
        y_pres = norm.pdf(x_pres, mu_larger, sigma)

        x_fn = np.linspace(mu_smaller, B, 500)
        y_fn = norm.pdf(x_fn, mu_larger, 1)
        y_fn = np.where(x_fn > 0, norm.pdf(x_fn, mu_smaller, 1), y_fn)
    
        fig.add_trace(go.Scatter(
            x=x_fn, y=y_fn,
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(128, 0, 128, 0.3)',
            name="FN"
        ))

        x_fp = np.linspace(B, mu_larger, 500)
        y_fp = norm.pdf(x_fp, loc=mu_smaller, scale=1)
        y_fp = np.where(x_fp < 0, norm.pdf(x_fp, mu_larger, 1), y_fp)

        fig.add_trace(go.Scatter(
            x=x_fp, y=y_fp,
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(0, 0, 255, 0.3)',
            name="FP"
        ))
        return fig


    absent_mu=-1.5
    present_mu=absent_mu*-1
    # add normal distributions to plot
    fig1=plot_normal_dist(fig1, absent_mu,'Disease Absent', 'green')
    fig1=plot_normal_dist(fig1, present_mu,'Disease Present', 'red')

    fig1 = highlight_FN_and_FPs(fig1, absent_mu, present_mu, B)

    # plot dashed lines for diagnostic test cutoffs
    for x_pos, label in [(-1.5, "A"), (1.5, "C")]:
        fig1.add_shape(
            type="line",
            x0=x_pos, x1=x_pos,
            y0=0, y1=0.4,
            line=dict(color="black", dash="dash", width=0.3)
        )
        fig1.add_annotation(
            x=x_pos,
            y=-0.02,
            text=label,
            showarrow=False,
            font=dict(size=18),
            align="center"
        )
    # Add dashed line for B:
    fig1.add_shape(
        type="line",
        x0=B, x1=B,
        y0=0, y1=0.4,
        line=dict(color="black", dash="dash", width=0.3)
    )
    fig1.add_annotation(
        x=B,
        y=-0.02,
        text="B",
        showarrow=False,
        font=dict(size=18),
        align="center"
    )

    fig1.update_layout(
        xaxis=dict(
            title="Test Results",
            showticklabels=False,

        ),
        yaxis=dict(
            title="Proportion of People",
            showticklabels=False,

        ),
    )

    st.plotly_chart(fig1)
    st.write('Consider the graph above, which depicts curves for those \
             who have disease and those who do not in a certain population. \
             The points A, B, and C represent different cutoff thresholds\
            for three diagnostic tests. Correctly identified true positives\
            and negatives occur where there is no overlap between the curves.\
            The areas where there is overlap represent false negatives or false\
            positives.')
    
    st.markdown('- **A** is the 100% sensitivity cutoff. If a test identified all\
                 people above A as being positive for disease, all true positives\
                 would be identified. However, the number of false positives would\
                 be maximized, meaning specificity would be minimized.')
    st.markdown('- **C** is the 100% specificity cutoff. If a test identified all\
                 people below C as being negative, all true negatives would be\
                 identified. However, the number of false negatives would be\
                 maximized, meaning sensitivity would be minimized.')
    st.markdown('- **B** is the tradeoff between these two at which both false\
                 positives and false negatives exist, but at lower rates.')
    st.markdown('On STEP, this concept could be assessed by asking you what\
                 happens to sensitivity, specificity, PPV, and NPV when\
                 the cutoff thresholds for a test are moved. Try the exercises\
                 below to see how these metrics are affected. Adjust the slider\
                above the graph to visualize the changes.')
    
    st.markdown('1. Let’s say the cutoff is lowered from B to A. Will sensitivity,\
                 specificity, PPV, and NPV increase or decrease?')
    with st.expander("Click for answer"):
        st.markdown("""
        Decreasing the cutoff increases the number of FPs and decreases FNs.
                     This causes sensitivity and NPV to increase. Specificity 
                    and PPV will decrease.
        """)

    st.markdown('2. Let’s say the cutoff is increased from B to C. Will sensitivity,\
                 specificity, PPV, and NPV increase or decrease?')
    with st.expander("Click for answer"):
        st.markdown("""
            Increasing the cutoff increases the number of FNs and
            decreases FPs. This causes specificity and PPV to 
            increase. Sensitivity and NPV decrease will decrease.
        """)
    return None
