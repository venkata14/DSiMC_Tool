import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import math
from scipy import stats
import numpy.random as random
# import random

# Visualization of RRR and ARR
def rrr_arr_comp():
    st.header("RRR vs ARR")
    st.write("""
    This exercise aims to demonstrate how relative risk reduction (RRR) and absolute risk reduction (ARR) are influenced by event rate. **RRR is often seeming more impressive than ARR**. For this scenario, we will be comparing the RRR and ARR for a certain event (e.g. disease) between a control group and a treatment group.
    We will also have two separate populations where the event rate will be different between the control groups.
    We will set the RRR between the control and treatment groups the same for both populations.
    """)

    with st.container(border=True):
        cols = st.columns(2)
        with cols[0]:
            control_rate1 = st.number_input("Rate of event in control group 1 (%)", value=40)
        with cols[1]:
            control_rate2 = st.number_input("Rate of event in control group 2 (%)", value=10)
        
        #RRR = st.number_input("Relative Risk Reduction", value=0.25)
        RRR = st.select_slider("Relative Risk Reduction (%)",
            options=[10, 25, 50, 75], value = 25)

    RR = 1 - RRR/100

    treat_rate1 = (control_rate1/100 * RR)*100
    treat_rate2 = (control_rate2/100 * RR)*100

    ARR_1 = control_rate1 - treat_rate1
    ARR_2 = control_rate2 - treat_rate2

    plt_df1 = pd.DataFrame({
        'Event Rate (%)': [control_rate1, treat_rate1, control_rate2, treat_rate2],
        'pop': ['Population 1', 'Population 1', 'Population 2', 'Population 2'],
        'Intervention': ['Control', 'Treatment', 'Control', 'Treatment']
    })

    plt1 = px.bar(plt_df1, x="pop", y="Event Rate (%)", color="Intervention", barmode="group")

    # NOTE: panning the graph is bad since the lines will always be there due to absolute positioning
    # However, there is no good way of formatting lines on categorical axes as of now

    st.write("""
    NOTE: Please do not pan the image or zoom in/out using the toolbar. Zoom in/out of the page itself if needed.
    If you do pan/zoom on the image, refresh the page to reset it back.
    """)

    plt1.add_shape(type="line", xref="paper", x0=0.28, x1=0.28, y0=treat_rate1, y1=control_rate1,
        line=dict(color="black")
    )
    plt1.add_shape(type="line", xref="paper", x0=0.27, x1=0.29, y0=treat_rate1, y1=treat_rate1,
        line=dict(color="black")
    )
    plt1.add_shape(type="line", xref="paper", x0=0.27, x1=0.29, y0=control_rate1, y1=control_rate1,
        line=dict(color="black")
    )

    plt1.add_shape(type="line", xref="paper", x0=0.78, x1=0.78, y0=treat_rate2, y1=control_rate2,
        line=dict(color="black")
    )
    plt1.add_shape(type="line", xref="paper", x0=0.77, x1=0.79, y0=treat_rate2, y1=treat_rate2,
        line=dict(color="black")
    )
    plt1.add_shape(type="line", xref="paper", x0=0.77, x1=0.79, y0=control_rate2, y1=control_rate2,
        line=dict(color="black")
    )

    plt1.add_annotation(text=str(round(ARR_1, 1))+" %", xref="paper", x=0.3, y=(treat_rate1+control_rate1)/2, 
        showarrow=False, xanchor='left', font=dict(size=16)
    )
    plt1.add_annotation(text=str(round(ARR_2, 1))+" %", xref="paper", x=0.8, y=(treat_rate2+control_rate2)/2, 
        showarrow=False, xanchor='left', font=dict(size=16)
    )

    plt1.update_layout(xaxis_title = None)

    st.plotly_chart(plt1)

    st.write('''
    The **ARR is represented by the two black lines in the bar graph**, along with the value of the ARR.

    Even though both populations have the **same RRR**, the **ARR for the populations with the higher event rate is greater than the one with the lower event rate**.

    ''')

# Visualization of OR vs RR
def or_rr_comp():
    st.header("OR vs RR")
    st.write("""
    This visualization aims to demonstrate how risk ratio (RR) and odds ratio (OR) changes with event rate.

    We will be looking at the RR and OR for a disease in an exposed group of 1000 individuals and unexposed group of 2000 individuals.

    Starting at a point where the disease is uncommon (disease frequency of <10% in the studied sample), we will increase the disease number by 200 in each group and calculate the OR and RR.
    """)

    N1 = 1000
    N2 = 2000
    event_increase = 200

    if st.button("Get new data"):
        rate_init1 = random.uniform(0.075, 0.1)
        rate_init2 = random.uniform(0.05, 0.075)
    else:
        rate_init1 = random.uniform(0.075, 0.1)
        rate_init2 = random.uniform(0.05, 0.075) 

    # Get event number
    dis_exp_ls = []
    dis_noexp_ls = []
    nodis_exp_ls = []
    nodis_noexp_ls = []
    rr_ls = []
    or_ls = []
    event_rate_ls = []

    for i in range(0, 4):
        dis_exp = math.floor(rate_init1*N1) + i*event_increase
        dis_noexp = math.floor(rate_init2*N2) + i*event_increase
        nodis_exp = N1 - dis_exp
        nodis_noexp = N2 - dis_noexp

        relr = (dis_exp/N1) / (dis_noexp/N2)
        oddr = (dis_exp/nodis_exp) / (dis_noexp/nodis_noexp)

        event_rate = (dis_exp + dis_noexp)/(N1 + N2)

        dis_exp_ls.append(dis_exp)
        dis_noexp_ls.append(dis_noexp)
        nodis_exp_ls.append(nodis_exp)
        nodis_noexp_ls.append(nodis_noexp)
        rr_ls.append(relr)
        or_ls.append(oddr)
        event_rate_ls.append(event_rate)

    event_rate_ls = [round(i*100) for i in event_rate_ls] #convert to %

    # Create Data Frame for Table Output
    table_df = pd.DataFrame({
        'Disease Rate (%)': event_rate_ls,
        'Disease in Exposed': dis_exp_ls,
        'Disease in Unexposed': dis_noexp_ls,
        'RR': [round(i, 2) for i in rr_ls],
        'OR': [round(i, 2) for i in or_ls]
    })

    st.dataframe(table_df, use_container_width=True)

    # Plot OR and RR
    plt = go.Figure()
    plt.add_trace(go.Scatter(x=event_rate_ls, y=or_ls, mode='lines+markers', name='OR', line_color = "blue"))
    plt.add_trace(go.Scatter(x=event_rate_ls, y=rr_ls, mode='lines+markers', name='RR', line_color = "red"))
    plt.update_layout(xaxis_title="Disease Rate (%)")
    st.plotly_chart(plt)

    st.write("""
    For uncommon events (disease frequency <10% of population), the values of RR and OR are nearly the same.

    For common events, OR may increase disproportionately while RR is relatively constrained. OR is always further away from 1 than RR.
    If exposure increases risk like in our case, then OR > RR > 1.
    """)