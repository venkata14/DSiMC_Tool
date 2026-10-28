import streamlit as st

from src.components.ebm.ebm_hypotest_func import hypo_test_demo1
from src.components.ebm.ebm_hypotest_func import hypo_test_demo2
from src.components.ebm.ebm_hypotest_func import CI_samplesize_amolak
from src.components.ebm.ebm_hypotest_func import bias
from src.components.ebm.ebm_hypotest_func import inc_prev
from src.components.ebm.sens_spec import sens_spec
from src.components.ebm.sens_spec import interactive_2x2_table
from src.components.ebm.ebm_prog_func import rrr_arr_comp
from src.components.ebm.ebm_prog_func import or_rr_comp
from src.components.ebm.g import all

st.set_page_config(
    page_icon="🧮",
    initial_sidebar_state="collapsed"
)

st.header("Hands-On EBM: Demonstrations in Evidence Based Medicine")


ebm_option = st.selectbox(
        "Select EBM Concept",
        (None,
         "Visualization of Type I error, Type II error, and Power",
         "Visualization of CI and hypothesis testing",
         "Confidence Interval change with Increasing Sample Size",
         "Bias",
         "Incidence and Prevalence",
         "Sensitivity, Specificity, NPV, and PPV",
         "Interactive 2x2 Contingency Table for Sensitivity & Specificity",
         "RR, OR, NNT, ARR, RRR",
         "RRR vs ARR",
         "OR vs RR",
         )
    )

if ebm_option == "Visualization of Type I error, Type II error, and Power" : hypo_test_demo1()
if ebm_option == "Visualization of CI and hypothesis testing" : hypo_test_demo2()
if ebm_option == "Confidence Interval change with Increasing Sample Size" : CI_samplesize_amolak()
if ebm_option == "Bias" : bias()
if ebm_option == "Incidence and Prevalence" : inc_prev()
if ebm_option == "Sensitivity, Specificity, NPV, and PPV" : sens_spec()
if ebm_option == "Interactive 2x2 Contingency Table for Sensitivity & Specificity" : interactive_2x2_table()
if ebm_option == "RRR vs ARR" : rrr_arr_comp()
if ebm_option == "OR vs RR" : or_rr_comp()
if ebm_option == "RR, OR, NNT, ARR, RRR" : all()



st.markdown("---")
st.write("""
         This is an interactive platform designed to help students understand Evidence Based Medicine (EBM) concepts. Please send us feedback [here](mailto:data_science_in_medicine@med.wayne.edu)!
                  
         **Developed by:** Venkata Patchigolla, Hyeok Jun Lee, Amolak Singh Jhand
         """)
