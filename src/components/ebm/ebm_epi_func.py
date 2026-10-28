import streamlit as st
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from scipy import stats
import random

# NOTE: This is for reseting sliders in inc_prev_factors. It is NOT a separate application
# Users can reset sliders up to the max limit of integer (there isn't a good work around found on streamlit)
def reset_sliders():
    st.session_state["slider_ver"] += 1

# Visualization of different factors on incidence and prevalence
def inc_prev_factors():
    if "slider_ver" not in st.session_state:
        st.session_state.slider_ver = 1

    st.write("""
    This part of the exercise aims to demonstrate the effect of disease factors on incidence and prevalence by playing and customizing with factors affecting Incidence and Prevalance.
    *Changing the sliders will generate a new plot (magenta) which you can compare to the original plot (black).*
    Please refer to the table to learn how each factor will influence incidence and prevalence

    Note:
    - Select "Reset Sliders" to bring parameters back to original values. Try changing one parameter at a time to isolate its effects.
    - Select "Generate New Plots" to create new plots using the same chosen values. We recommend doing this multiple times to understand the general effects.""")

    st.image("src/img/table.png")

    N = 15
    t = 20

    disease_ls1 = []
    mort_ls1 = []
    dstart_ls1 = []
    dend_ls1 = []

    disease_ls2 = []
    mort_ls2 = []
    dstart_ls2 = []
    dend_ls2 = []

    # Disease factors (for N1)
    mean_dur1 = 4
    risk_fac1 = 0.6
    mort_rate1 = 0.2
    vacc1 = 0
    diag1 = 0.6
    recov_time1 = 1
    mort_time1 = 0.4 
    treat_time1 = 0

    # Disease factors for N2
    # Note: change one at a time plz
    mort_time2 = 0.4

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            mean_dur2 = st.select_slider("Survival Time (ie Disease Duration)",
                options=[4, 5, 6, 7], value = 4, key=f"mean_dur_{st.session_state['slider_ver']}")

            mort_rate2 = st.select_slider("Mortality Rate",
                options=[0.2, 0.4, 0.6], value = 0.2, key=f"mort_rate_{st.session_state['slider_ver']}")
            
            recov_time2 = st.select_slider("Recovery Time (Proportion to original)",
                options=[0.4, 0.6, 0.8, 1], value = 1, key=f"recov_time_{st.session_state['slider_ver']}")
            
            vacc2 = st.select_slider("Vaccine Coverage",
                options=[0, 0.3, 0.6], value = 0, key=f"vacc_{st.session_state['slider_ver']}")

    with col2:
        with st.container(border=True):
            risk_fac2 = st.select_slider("Risk Factors",
                options=[0.6, 0.8, 1], value = 0.6, key=f"risk_fac_{st.session_state['slider_ver']}")

            diag2 = st.select_slider("Diagnostic Sensitivity",
                options=[0.6, 0.8, 1], value = 0.6, key=f"diag_{st.session_state['slider_ver']}")

            treat_time2 = st.select_slider("Effectiveness of Treatment",
                options=[0, 0.2, 0.4, 0.6], value = 0, key=f"treat_time_{st.session_state['slider_ver']}")

            st.button("Reset Sliders", on_click=reset_sliders)
            if st.button("Generate New Plots"):
                new_plots = True
            else:
                new_plots = True

    # Oh yea get ready for the fking brain splurge of a lifetime boyz cause its funny sht aaa
    if(new_plots):
        for i in range(0, N):
            # Set up all the random ass sht
            dis_rand = random.random()
            mort_rand = random.random()
            dstart_hold = random.random() * (t-1)
            dur_hold = abs(stats.norm(0, 0.5).rvs()) #ungodly distribution but too lazy to gamma
            mort_dur_rand = 1 - abs(stats.norm(0, 0.05).rvs())
            recov_rand = 1 - abs(stats.norm(0, 0.05).rvs())
            treat_rand = 1 - abs(stats.norm(0, 0.05).rvs())

            # See if they have disease (note if pop 1 has disease, pop 2 will also have it cause i made it that way)
            # prob of risk factor * (1 - prob of vacc) * diag sensitivtiy
            dis_prob1 = risk_fac1 * (1-vacc1) * diag1
            dis_prob2 = risk_fac2 * (1-vacc2) * diag2
            if(dis_rand <= dis_prob1):
                disease_hold1 = True
            else:
                disease_hold1 = False
            
            if(dis_rand <= dis_prob2):
                disease_hold2 = True
            else:
                disease_hold2 = False
            
            # See if they gonna die (weak)
            if(disease_hold1 and mort_rand <= mort_rate1):
                mort_hold1 = 203 #These numbers are for plotly stuff
            else:
                mort_hold1 = 219
            if(disease_hold2 and mort_rand <= mort_rate2):
                mort_hold2 = 203 #These numbers are for plotly stuff
            else:
                mort_hold2 = 219
            
            # Look at the duration of disease
            if(disease_hold1):
                # If dude gonna die, look at mortality duration
                # If not, mean duration * recovery * treatment
                if(mort_hold1==203):
                    dur1 = (dur_hold + mean_dur1) * (mort_dur_rand * mort_time1)
                else: 
                    dur1 = (dur_hold + mean_dur1) * (recov_rand * recov_time1) * (1 - treat_rand * treat_time1)
                dend_hold1 = dur1 + dstart_hold
                if(dend_hold1 > t):
                    dend_hold1 = t
                dstart_hold1 = dstart_hold
            else:
                dstart_hold1 = 100
                dend_hold1 = 100
            
            if(disease_hold2):
                # If dude gonna die, look at mortality duration
                # If not, mean duration * recovery * treatment
                if(mort_hold2==203):
                    dur2 = (dur_hold + mean_dur2) * (mort_dur_rand * mort_time2)
                else: 
                    dur2 = (dur_hold + mean_dur2) * (recov_rand * recov_time2) * (1 - treat_rand * treat_time2)
                dend_hold2 = dur2 + dstart_hold
                if(dend_hold2 > t):
                    dend_hold2 = t
                dstart_hold2 = dstart_hold
            else:
                dstart_hold2 = 100
                dend_hold2 = 100
            
            # Put into lists
            disease_ls1.append(disease_hold1)
            mort_ls1.append(mort_hold1)
            dstart_ls1.append(dstart_hold1)
            dend_ls1.append(dend_hold1)

            disease_ls2.append(disease_hold2)
            mort_ls2.append(mort_hold2)
            dstart_ls2.append(dstart_hold2)
            dend_ls2.append(dend_hold2)
        new_plots = False

    # Plot
    st.write('''
    In this figure, we represent the disease profile between 15 individuals.
    - The down arrow represents the onset of the disease
    - The horizontal line represents the duration.
    - The up arrow represents recovery from the disease
    - The cross represents death from the disease.

    We assume that death will likely result in a shorten duration of disease (likely due to increased severity).
    Compare the **original patient data (black)** to the **patient data with changed parameters (magenta)**. 
    
    *Note: The data changes everytime the above values are changed.*''')

    plt = go.Figure()
    for i in range(0, N):
        if disease_ls1[i]:
            plt.add_trace(go.Scatter(x = [dstart_ls1[i], dend_ls1[i]], y = [i+1.1, i+1.1],
                mode='lines+markers', showlegend=False, line_color = "black",
                marker={'symbol':[220,mort_ls1[i]], "size":12}, marker_color = "black"))
        if disease_ls2[i]:
            plt.add_trace(go.Scatter(x = [dstart_ls2[i], dend_ls2[i]], y = [i+0.9, i+0.9],
                mode='lines+markers', showlegend=False, line_color = "magenta",
                marker={'symbol':[220,mort_ls2[i]], "size":12}, marker_color = "magenta"))

    plt.add_vrect(
        x0=10, x1=11, fillcolor="LightSalmon", opacity=0.3, layer="below", line_width=0
    )

    plt.add_vline(x=10, line_dash="dash", opacity=0.7, line_color="blue")

    plt.update_layout(
        yaxis_title="Patient #",
        xaxis_title="Time", 
        yaxis=dict(
            range=[0, N+1],
            tickvals = list(range(1, N+1))
        ),
        xaxis=dict(
            range=[0, t+1],
            tickvals= list(range(0, t+1, 2))
        )
    )
    plt.update_yaxes(showgrid=False)
    plt.update_layout(height=500)

    st.plotly_chart(plt, use_container_width = False)

    # Optimize later (love me some O(n^2) yum)

    inc1=[]
    inc2=[]
    prev1=[]
    prev2=[]

    st.write('''
    Here we plot the incidence (top figure) and prevalence (bottom figure) of the disease based on the previous plot.
    - The incidence at time t was calculated by counting the number of *new* cases between t and t+1.
    - The prevalence at time t was calculated by counting the number of individuals who have the disease at time t.

    The plots demonstrate this calculation at week 10 (shown by the orange window and dashed line in the previous plot, and the circle in the time series plots).
    Observe how the new parameters change incidence and prevalence (shown in magenta) compared to the original parameters (shown in black).
            ''')

    for i in range(0, t):
        inc_hold = list(filter(lambda x: x >= i and x < (i+1), dstart_ls1))
        inc1.append(len(inc_hold))
        inc_hold = list(filter(lambda x: x >= i and x < (i+1), dstart_ls2))
        inc2.append(len(inc_hold))

        prev1_hold = 0
        prev2_hold = 0
        for j in range(0, len(dstart_ls1)):
            if(disease_ls1[j] and i >= dstart_ls1[j] and i <= dend_ls1[j]):
                prev1_hold += 1
            if(disease_ls2[j] and i >= dstart_ls2[j] and i <= dend_ls2[j]):
                prev2_hold += 1
        
        prev1.append(prev1_hold)
        prev2.append(prev2_hold)

    plt1 = go.Figure()
    plt1.add_trace(go.Scatter(x = list(range(0, t)), y = inc1,
                mode='lines', showlegend=False, line_color = "black", opacity=0.7))
    plt1.add_trace(go.Scatter(x = list(range(0, t)), y = inc2,
                mode='lines', showlegend=False, line_color = "magenta", opacity=0.7))
    plt1.add_trace(go.Scatter(x = [10], y = [inc1[10]],
                mode='markers', showlegend=False, marker_color = "black", opacity=0.7,
                marker={'symbol':200, "size":12}))
    plt1.add_trace(go.Scatter(x = [10], y = [inc2[10]],
                mode='markers', showlegend=False, marker_color = "magenta", opacity=0.7,
                marker={'symbol':200, "size":12}))
    plt1.update_layout(
        title="Incidence",
        xaxis_title="Time",
        xaxis=dict(
            range=[0, t],
            tickvals= list(range(0, t+1, 2))
        ),
        height=350,
        width=350
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plt1)

    plt2 = go.Figure()
    plt2.add_trace(go.Scatter(x = list(range(0, t)), y = prev1,
                mode='lines', showlegend=False, line_color = "black", opacity=0.7))
    plt2.add_trace(go.Scatter(x = list(range(0, t)), y = prev2,
                mode='lines', showlegend=False, line_color = "magenta", opacity=0.7))
    plt2.add_trace(go.Scatter(x = [10], y = [prev1[10]],
                mode='markers', showlegend=False, marker_color = "black", opacity=0.7,
                marker={'symbol':200, "size":12}))
    plt2.add_trace(go.Scatter(x = [10], y = [prev2[10]],
                mode='markers', showlegend=False, marker_color = "magenta", opacity=0.7,
                marker={'symbol':200, "size":12}))
    plt2.update_layout(
        title="Prevalence",
        xaxis_title="Time",
        xaxis=dict(
            range=[0, t],
            tickvals= list(range(0, t+1, 2))
        ),
        height=350,
        width=350
    )
    with col2:
        st.plotly_chart(plt2)