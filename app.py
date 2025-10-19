import pandas as pd
import streamlit as st

# -------------------------------
# Load student data
# -------------------------------
file_path = "student_allocations.csv"  # Update path if needed
students_df = pd.read_csv(file_path)

# -------------------------------
# Streamlit Dashboard Config
# -------------------------------
st.set_page_config(
    page_title="Student Result Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Sidebar for instructions
st.sidebar.header("ℹ️ Instructions")
st.sidebar.markdown("""
1. Enter your **Unique ID** below.  
2. Click **Search** to view your seat allocation details.  
3. Check **Preference, College, Rank, and Caste** information clearly.
""")

# Main Header
st.markdown("<h1 style='text-align: center; color: #4B0082;'>🎓 Student Result Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px;'>Search your Unique ID to view your seat allocation and preferences.</p>", unsafe_allow_html=True)

# -------------------------------
# Input for UniqueID
# -------------------------------
unique_id = st.text_input("🔑 Enter Your Unique ID", value="1115619330")

# -------------------------------
# Search Button
# -------------------------------
if st.button("Search"):
    if unique_id.isdigit():
        unique_id = int(unique_id)
        student = students_df[students_df["UniqueID"] == unique_id]

        if not student.empty:
            # Display summary cards
            st.markdown("### 📝 Student Details")
            cols = st.columns(3)
            cols[0].metric("🎯 Rank", student.iloc[0]["Rank"])
            cols[1].metric("🏫 College Allotted", student.iloc[0]["CollegeID"])
            cols[2].metric("🧬 Caste", student.iloc[0]["Caste"])

            # Display full details in a table
            st.markdown("### 📊 Full Allocation Data")
            st.dataframe(student)  # Simple table, no matplotlib required

        else:
            st.error("❌ Student not found.")
    else:
        st.warning("⚠️ Please enter a valid numeric UniqueID.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("<p style='text-align: center; color: gray; font-size:12px;'>Powered by 🐍 Python & Streamlit</p>", unsafe_allow_html=True)
