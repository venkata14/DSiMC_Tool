# DSiMC Tool

Free, interactive web tools for learning evidence-based medicine (EBM) statistics and exploring medical data, built with Python and [Streamlit](https://streamlit.io/) by the Data Science in Medicine Club (DSiMC) at Wayne State University School of Medicine.

**Live app:** https://dsimctool.streamlit.app
**EBM demonstrations:** https://dsimctool.streamlit.app/EBM

No login or installation is needed to use the hosted app.

---

## Hands-On EBM: interactive demonstrations

The EBM page turns core statistics and epidemiology concepts into visualizations that update in real time. Learners change parameters such as sample size, effect size, or a test's decision threshold and immediately see what happens to error rates, confidence intervals, or predictive values.

| Module | What learners can explore |
| --- | --- |
| Type I error, Type II error, and power | How effect size, sample size, and confidence level change α, β, and power |
| Confidence intervals and hypothesis testing | How a confidence interval relates to a hypothesis test's result |
| Confidence interval vs. sample size | How confidence intervals narrow as sample size grows |
| Bias | Selection bias and measurement bias |
| Incidence and prevalence | How disease duration, mortality, vaccination, and treatment change incidence and prevalence |
| Sensitivity, specificity, NPV, and PPV | How moving a test's cutoff shifts false positives and false negatives |
| Interactive 2×2 table | Calculating diagnostic test measures from your own 2×2 table |
| RR, OR, NNT, ARR, and RRR | Calculating treatment-effect measures from a 2×2 table, with clinical scenarios (statin therapy, flu vaccine) |
| RRR vs. ARR | Why a large relative risk reduction can mean a small absolute benefit |
| OR vs. RR | Why the odds ratio drifts away from the risk ratio as a disease becomes more common |

The demonstrations were developed for first-year medical students and are used alongside small-group EBM case worksheets at Wayne State University School of Medicine.

## Data exploration tool

The main page is a point-and-click tool for quick exploratory analysis of tabular data, aimed at students working on research posters and presentations. You can:

- Upload a `.csv` or `.xlsx` file, or try the included sample dataset (`sample_ehr.xlsx`, synthetic data)
- Filter rows
- Create value counts, histograms (optionally layered by a second column), grouped summaries, and scatter plots
- Download charts as images for posters and presentations

Step-by-step instructions are on the app's **Instructions** page (open the sidebar with the `>` button at the top left).

---

## Run locally

Requires Python 3.10 or later.

```bash
git clone https://github.com/venkata14/DSiMC_Tool.git
cd DSiMC_Tool
pip install -r requirements.txt
streamlit run DSiMC_Tool.py
```

The app opens at `http://localhost:8501`. The EBM demonstrations are under the **EBM** page in the sidebar.

## Project structure

```
DSiMC_Tool.py              # Main page: data exploration tool
pages/
  EBM.py                   # Hands-On EBM demonstrations
  Instructions.py          # How to use the data exploration tool
  About DSiMC.py           # About the club
src/
  components/              # Charts, filters, and statistics for the data tool
  components/ebm/          # EBM demonstration modules
  text/instructions.py     # Instructions page text
sample_ehr.xlsx            # Sample dataset
requirements.txt
```

## Adapting this for your institution

Each EBM demonstration is a self-contained function in `src/components/ebm/`. To add or change a module, write a new function and add it to the menu in `pages/EBM.py`. You can deploy your own copy for free on [Streamlit Community Cloud](https://streamlit.io/cloud) by forking this repository and pointing a new app at `DSiMC_Tool.py`.

## Citation

If you use this tool in teaching or research, please cite:

> Patchigolla V, Jhand AS, Lee HJ. DSIMC Tool. Available at: https://dsimctool.streamlit.app/EBM


## Contributors

Developed by **Venkata Patchigolla**, **Amolak Singh Jhand**, and **Hyeok Jun Lee**, Data Science in Medicine Club, Wayne State University School of Medicine.

## License

MIT License. See the attached LICENSE
