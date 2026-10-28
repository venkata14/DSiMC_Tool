import streamlit as st
import pandas as pd

def calculate_risk_ratio(a, b, c, d):
    """Calculates the Risk Ratio."""
    if (a + b) == 0 or (c + d) == 0:
        return None  # Avoid division by zero
    risk_exposed = a / (a + b)
    risk_unexposed = c / (c + d)
    if risk_unexposed == 0:
        return None # Avoid division by zero
    return risk_exposed / risk_unexposed

def calculate_odds_ratio(a, b, c, d):
    """Calculates the Odds Ratio."""
    if b == 0 or d == 0 or c == 0 or a == 0: 
        return None
    return (a / b) / (c / d)

def all():
    def calculate_risk_ratio(a, b, c, d):
        """Calculates the Risk Ratio."""
        if (a + b) == 0 or (c + d) == 0:
            return None
        risk_exposed = a / (a + b)
        risk_unexposed = c / (c + d)
        if risk_unexposed == 0:
            return None
        return risk_exposed / risk_unexposed

    def calculate_odds_ratio(a, b, c, d):
        """Calculates the Odds Ratio."""
        if b == 0 or d == 0 or c == 0 or a == 0:
            return None
        return (a / b) / (c / d)

    def calculate_eer(a, b):
        """Calculates Experimental Event Rate (Risk in Exposed Group)."""
        if (a + b) == 0:
            return None
        return a / (a + b)

    def calculate_cer(c, d):
        """Calculates Control Event Rate (Risk in Unexposed Group)."""
        if (c + d) == 0:
            return None
        return c / (c + d)

    def calculate_arr(eer, cer):
        """Calculates Absolute Risk Reduction."""
        if eer is None or cer is None:
            return None
        return cer - eer

    def calculate_rrr(eer, cer):
        """Calculates Relative Risk Reduction."""
        if cer is None or cer == 0 or eer is None: # Avoid division by zero or if CER is zero which implies no baseline risk
            return None
        return (cer - eer) / cer

    def calculate_nnt(arr):
        """Calculates Number Needed to Treat."""
        if arr is None or arr == 0:
            return None
        return 1 / arr if arr != 0 else float('inf')

    # --- Streamlit App Start ---
    st.title("Risk Ratio, Odds Ratio, Number Needed to Treat, Absolute Risk Reduction and Relative Risk Reduction")

    st.markdown("""
    **Risk Ratios**, **Odds Ratios**, **Relative Risk Reduction (RRR)**, **Absolute Risk Reduction (ARR)**, and **Number Needed to Treat (NNT)** are key measures used in epidemiology and clinical research to assess and compare outcomes between groups, especially when evaluating interventions/exposures.
    """)

    # --- Intro ---
    st.header("Understanding Risk Ratios, Odds Ratios, and Risk Reductions")

    st.markdown("""
    **Contingency Table (2x2 Table):**  All these measures are calculated from a 2x2 contingency table. Let's define the table:

    |                  | **Outcome Present (e.g., Disease)** | **Outcome Absent (e.g., No Disease)** | **Total** |
    |------------------|---------------------------------------|----------------------------------------|-----------|
    | **Exposed Group (e.g., Treatment)** | **a**                                 | **b**                                  | **a + b** |
    | **Unexposed Group (e.g., Control)** | **c**                                 | **d**                                  | **c + d** |
    | **Total**          | **a + c**                             | **b + d**                              | **N (Total)**|

    *   **a:** Number of exposed individuals with the outcome.
    *   **b:** Number of exposed individuals without the outcome.
    *   **c:** Number of unexposed individuals with the outcome.
    *   **d:** Number of unexposed individuals without the outcome.

    """)
    
    
    with st.expander("**Definitions and Formulas**"):
        st.subheader("Risk Ratio Definition & Formula")
        st.markdown("""
            **Definition:**  Compares the risk of an event in one group to the risk in another.
            
            Always used in the setting of a **Cohort Study**. A Cohort study is a study that involves a group of people who are exposed to a treatment/intervention, and then followed up with a follow-up period. **AKA**, the variables that are controlled in this study are the *exposures (treatment/intervention)* and we wait for the future to see the dependent variable *(disease/no disease)*. This is what the RR calculates for. You will notice that the RR formula (below) is along the **row** as the exposures are along the row. Remember the "r"s in RR for "r"ow.
            
            **Formula:**

            Risk Ratio = (Risk in Exposed Group) / (Risk in Unexposed Group)

            Risk in Exposed Group =  a / (a + b)

            Risk in Unexposed Group = c / (c + d)

            **Therefore:**

            **Risk Ratio = [ a / (a + b) ]  /  [ c / (c + d) ]**
            """)

        st.subheader("Odds Ratio Definition & Formula")
        st.markdown("""
            **Definition:** Compares the odds of an event happening in one group to the odds in another.
            
            Always used in the setting of a Case Control Study. A Case Control study a research method that compares people who currently have a disease/condition with people who do not and then looks "back in time" to identify the exposures of the two groups. **AKA**, the variables that are controlled in this study are *disease/condition* and we look back in the past to see the dependent variable *(exposures)*. This is what the OR calculates for. You will notice that the OR formula (below) is along the **column** as the disease outcomes are along the column. Remember the "o"s in OR c"o"lumn.

            **Formula:**

            Odds Ratio = (Odds of Outcome in Exposed Group) / (Odds of Outcome in Unexposed Group)

            Odds of Outcome in Exposed Group (First Column) = a / b

            Odds of Outcome in Unexposed Group (Second Column) = c / d

            **Therefore:**

            **Odds Ratio = (a / c)  /  (b / d)  = (a * d) / (b * c)**
            """)

        st.subheader("Absolute Risk Reduction (ARR) Definition & Formula")
        st.markdown("""
            **Definition:** The actual difference in risk of an outcome between the treated/exposed group and the control/unexposed group. It tells you by how much the intervention *reduces* the risk in absolute terms.

            **Formula:**

            ARR = (Risk in Unexposed Group) - (Risk in Exposed Group)

            ARR = CER - EER

            ARR = [c / (c + d)] - [a / (a + b)]
            """)

        st.subheader("Relative Risk Reduction (RRR) Definition & Formula")
        st.markdown("""
            **Definition:**  The *proportional* reduction in risk in the treated/exposed group compared to the control/unexposed group. It expresses how much the intervention reduces risk *relative* to the baseline risk (risk in the control group).

            **Formula:**

            RRR = (Risk in Unexposed Group - Risk in Exposed Group) / (Risk in Unexposed Group)
            
            **RRR = 1 - Risk Ratio**

            RRR = (CER - EER) / CER
            
            RRR =  { [c / (c + d)] - [a / (a + b)] }  /  [c / (c + d)]
            """)

        st.subheader("Number Needed to Treat (NNT) Definition & Formula")
        st.markdown("""
            **Definition:** The number of patients you need to treat with an intervention to prevent one additional harmful outcome. It is a measure of clinical impact.

            **Formula:**

            **NNT = 1 / ARR**

            NNT = 1 / (CER - EER)

            NNT =  1 / { [c / (c + d)] - [a / (a + b)] }
            """)

    # --- Interactive Contingency Table Input ---
    st.subheader("Enter Data into the Contingency Table")
    st.write("**Modify the numbers in the table below to see how all these measures change!**")
    
    default_data = pd.DataFrame({
        "Outcome Present": [30, 50],
        "Outcome Absent": [50, 70]
    }, index=["Exposed Group", "Unexposed Group"])

    edited_data = st.data_editor(default_data, num_rows="dynamic")

    a = edited_data["Outcome Present"]["Exposed Group"]
    b = edited_data["Outcome Absent"]["Exposed Group"]
    c = edited_data["Outcome Present"]["Unexposed Group"]
    d = edited_data["Outcome Absent"]["Unexposed Group"]


    # --- Calculations and Display ---
    st.header("Calculated Measures")

    # Calculate all measures
    risk_ratio = calculate_risk_ratio(a, b, c, d)
    odds_ratio = calculate_odds_ratio(a, b, c, d)
    eer = calculate_eer(a, b)
    cer = calculate_cer(c, d)
    arr = calculate_arr(eer, cer)
    rrr = calculate_rrr(eer, cer)
    nnt = calculate_nnt(arr)

    col1, col2 = st.columns(2)
    st.subheader(" ")
    c1, c2 = st.columns(2)
    st.subheader(" ")
    c3, c4 = st.columns(2)

    with col1:
        st.subheader("Risk Ratio")
        with st.expander("Calculation"):
            st.markdown(f"""
    |                  | Outcome Present (e.g., Disease) | Outcome Absent (e.g., No Disease) |
    |------------------|---------------------------------------|----------------------------------------|
    | Exposed Group (e.g., Treatment) | <div style="color: red">{a}</div> | <div style="color: red">{b}</div> |
    | Unexposed Group (e.g., Control) | <div style="color: blue">{c}</div> | <div style="color: blue">{d}</div> |
    
    **Risk Ratio = [ <span style="color: red">a / (a + b)</span> ] /  [ <span style="color: blue">c / (c + d)</span> ]**
    <br />
    $=$
    <br />
    [ <span style="color: red">{a} / ({a + b})</span> ] /  [ <span style="color: blue">{c} / ({c + d})</span> ] = {risk_ratio:.2f}
    """, unsafe_allow_html=True)

        if risk_ratio is not None:
            st.metric("Risk Ratio", f"{risk_ratio:.2f}")
            st.markdown(f"""
                **Interpretation** (*Only in Cohort Study*):
                *   A Risk Ratio of {risk_ratio:.2f} means the **risk of the outcome in the exposed group is {risk_ratio:.2f} times the risk in the unexposed group.**
                *   **RR > 1:** Increased risk. **RR < 1:** Decreased risk. **RR = 1:** No difference.
                """)
        else:
            st.warning("Cannot calculate Risk Ratio (invalid input).")

    with c1:
        st.subheader("Absolute Risk Reduction (ARR)")
        with st.expander("Calculation"):
            st.markdown(f"""
    |                  | Outcome Present | Outcome Absent|
    |------------------|---------------------------------------|----------------------------------------|
    | Exposed | <div style="color: red">{a}</div> | <div style="color: red">{b}</div> |
    | Unexposed | <div style="color: blue">{c}</div> | <div style="color: blue">{d}</div> |

    **ARR = [ <span style="color: blue">c / (c + d)</span> ] /  [ <span style="color: red">a / (a + b</span> ]**
    <br />
    $=$
    <br />
    [ <span style="color: blue">{c} / ({c + d})</span> ] /  [ <span style="color: red">{a} / ({a + b})</span> ] = {arr:.2f}
    """, unsafe_allow_html=True)
        if arr is not None:
            st.metric("ARR", f"{arr*100:.2f}%") # Display as percentage
            st.markdown(f"""
                **Interpretation:**
                *   ARR of {arr*100:.2f}% means the **intervention reduces the absolute risk of the outcome by {arr*100:.2f} percentage points** compared to the control.
                *   It's the *actual* difference in risk.
                """)
        else:
            st.warning("Cannot calculate ARR (invalid input).")


    with col2:
        st.subheader("Odds Ratio")
        with st.expander("Calculation"):
            st.markdown(f"""
    |                  | Outcome Present (e.g., Disease) | Outcome Absent (e.g., No Disease) |
    |------------------|---------------------------------------|----------------------------------------|
    | Exposed Group (e.g., Treatment) | <div style="color: red">{a}</div> | <div style="color: blue">{b}</div> |
    | Unexposed Group (e.g., Control) | <div style="color: red">{c}</div> | <div style="color: blue">{d}</div> |
    
    **Odds Ratio = ( <span style="color: red">a / c</span> ) / ( <span style="color: blue">b / d</span> )**
    <br />
    $=$
    <br />
    [ <span style="color: red">{a} / {c}</span> ] /  [ <span style="color: blue">{b} / {d}</span> ] = {odds_ratio:.2f}
    """, unsafe_allow_html=True)
            
        if odds_ratio is not None:
            st.metric("Odds Ratio", f"{odds_ratio:.2f}")
            st.markdown(f"""
                **Interpretation** (*Only in Case Control Study*):
                *   An Odds Ratio of {odds_ratio:.2f} means the **odds of the outcome in the exposed group are {odds_ratio:.2f} times the odds in the unexposed group.**
                *   **OR > 1:** Increased odds. **OR < 1:** Decreased odds. **OR = 1:** No difference.
                """)
        else:
            st.warning("Cannot calculate Odds Ratio (invalid input).")
    with c2:
        st.subheader("Relative Risk Reduction (RRR)")
        with st.expander("Calculation"):
            st.markdown(f"""
                        RRR = 1 - Risk Ratio = <br/> 1 - {risk_ratio:.2f} = {rrr:.2f}
                        """, unsafe_allow_html=True)
        if rrr is not None:
            st.metric("RRR", f"{rrr*100:.2f}%") # Display as percentage
            st.markdown(f"""
                **Interpretation:**
                *   RRR of {rrr*100:.2f}% means the **intervention reduces the risk of the outcome by {rrr*100:.2f}% *relative* to the baseline risk** (risk in the unexposed group).
                *   It's the *proportional* reduction in risk.
                """)
        else:
            st.warning("Cannot calculate RRR (invalid input or no baseline risk in unexposed group).")


    with c3:
        st.subheader("Number Needed to Treat (NNT)")
        with st.expander("Calculation"):
            st.markdown(f"""
                        NNT = 1 / ARR = <br/> 1 / {arr:.2f} = {nnt:.2f}
                        """, unsafe_allow_html=True)
        if nnt is not None:
            if nnt == float('inf'):
                st.metric("NNT", "Infinite") # Indicate no effect
                st.markdown("*No benefit from treatment in terms of risk reduction based on input.*")
            else:
                st.metric("NNT", f"{nnt:.0f}") # NNT is usually an integer
                st.markdown(f"""
                    **Interpretation:**
                    *   NNT of {nnt:.0f} means you need to treat **{nnt:.0f} individuals in the exposed group to prevent one additional outcome** compared to not treating.
                    *   A lower NNT is generally better, indicating a more effective intervention.
                    """)
        else:
            st.warning("Cannot calculate NNT (invalid ARR).")


    with st.expander("Example Scenarios"):
        st.subheader("Scenario 1:  Statin Therapy for Heart Disease Prevention")
        st.markdown("""
            Consider a clinical trial evaluating statin therapy to prevent heart attacks in people with high cholesterol:

            *   **Exposed Group:**  Statin Therapy
            *   **Unexposed Group:** Placebo
            *   **Outcome:** Heart Attack over 5 years

            Let's say the data is:
            """)
        example_data_scenario1 = pd.DataFrame({
            "Outcome Present": [30, 40],
            "Outcome Absent": [970, 960]
        }, index=["Statin Group", "Placebo Group"]) # Outcomes are relatively rare
        st.dataframe(example_data_scenario1)
        st.markdown("Enter these numbers. Notice the ARR, RRR, and NNT. Which measure do you think is most informative for deciding about statin therapy and why?")

        st.subheader("Scenario 2:  Flu Vaccine Effectiveness")
        st.markdown("""
            Imagine studying the effectiveness of a flu vaccine in preventing flu during a flu season:

            *   **Exposed Group:** Received Flu Vaccine
            *   **Unexposed Group:** Did not receive Flu Vaccine
            *   **Outcome:**  Contracting the Flu

            Data example:
            """)
        example_data_scenario2 = pd.DataFrame({
            "Outcome Present": [20, 80],
            "Outcome Absent": [980, 920]
        }, index=["Vaccinated Group", "Unvaccinated Group"])
        st.dataframe(example_data_scenario2)
        st.markdown("Analyze these numbers using all the measures.  How effective is the flu vaccine according to ARR, RRR, and NNT? How do these measures provide different perspectives on effectiveness?")