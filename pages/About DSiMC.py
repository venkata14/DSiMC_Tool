import streamlit as st

st.set_page_config(
    page_title="About DSiMC",
    page_icon="👋",
    layout="wide"
)

# Header
st.title("Welcome to the Data Science in Medicine Club!")
st.write("Empowering medical students with the knowledge and skills to conduct data-driven analysis in medical contexts.")

# Mission Statement
st.header("Our Mission")
st.write("""
At the Data Science Club, we strive to:
- Foster a community of medicine & data enthusiasts
- Provide hands-on learning experiences
- Promote student research

The mission of the Data Science in Medicine Club (DSiMC) at Wayne SOM is to empower our fellow medical students with the knowledge and skills to conduct data-driven analysis in medical contexts. To this end, we host introductory Python programming workshops for our peers, work with the EBM team at WSUSOM and developed a data analysis tool for rapid data analysis. 

Please reach out to any of us for data analysis needs!
""")
st.markdown("---")

# Club Activities
st.header("What We Do")
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height = 170):
        st.subheader("_Python Workshop Series_")
        st.write("Our Python Workshops provide an opportunity for medical students with minimal computer science background to learn the basics of programming.")

url_tool = "https://dsimctool.streamlit.app/"
with col2:
    with st.container(border=True, height = 170):
        st.subheader("_DSiMC Tool_")
        st.write("The [DSiMC Tool](%s) is a simple, easy-to-use online application created by our members for exploratory analysis, statistical analysis, and visualization of tabulated medical data." % url_tool)

another_col1, another_col2 = st.columns(2)

url_ebm = "https://dsimctool.streamlit.app/EBM"
with another_col1:
    with st.container(border=True, height = 170):
        st.subheader("_Evidence Based Medicine Demonstrations_")
        st.write("Our interactive [EBM demonstrations](%s) aim to educate medical students on important EBM and statistical topics they may come across during their studies and provide an engaging learning experience." % url_ebm)

# Team Members Part 1
st.header("Meet Our Team")
col1, col2, col3 = st.columns(3)

team_members = [
    {"name": "Venkata Patchigolla", "role": "President", },
    {"name": "Amolak Singh Jhand", "role": "Vice President", },
    {"name": "Hyeok Jun Lee", "role": "Treasurer", },
]

for i, member in enumerate(team_members):
    with [col1, col2, col3][i]:
        st.write(f"*{member['role']}*")
        st.write(f"{member['name']}")

# Team Members Part 2
col1, col2, col3 = st.columns(3)

team_members = [
    {"name": "Henry Li", "role": "Secretary", },
    {"name": "Dhwani Krishnan", "role": "Event Coordinator", },
    {"name": "Madeleine Evans", "role": "Event Coordinator", },
]

for i, member in enumerate(team_members):
    with [col1, col2, col3][i]:
        st.write(f"*{member['role']}*")
        st.write(f"{member['name']}")


# Join Us Section
st.header("Join Us!")
st.write("""
Interested in joining our club? We welcome students of all backgrounds and skill levels! Please email us at data_science_in_medicine@med.wayne.edu to get started.
""")
st.markdown("---")
