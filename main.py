import streamlit as st
import pandas as pd
from utils import adjust_all_columns_to_string, convert_df_to_csv, process_csv_data
from schema import required_columns
import time

# Page configuration
st.set_page_config(
    page_title="CSV Editor 🗃️",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for the header
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #4B8BBE;
            text-align: center;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Welcome to the CSV Editor 🗃️</div>', unsafe_allow_html=True)

# Sidebar instructions
st.sidebar.title("📋 Instructions")
st.sidebar.info("""
1. Upload a CSV file.
2. Server will start processing the input CSV to generate output CSV by applying required transformations.
3. Output CSV will be available for review.
4. You can edit the output CSV as well (if any further changes are required).
5. Finally you can download the output CSV.
""")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file containing all the required columns", type=["csv"])

# If a file is uploaded, proceed to check for required columns and process it
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    df = adjust_all_columns_to_string(df)

    # Check if all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        # Display a message showing which columns are missing
        st.error(f"The following required columns are missing from the uploaded CSV: {', '.join(missing_columns)}")
    else:
        # Display the DataFrame in an editable table
        with st.expander("View Output CSV",expanded=True):
            with st.spinner("Processing to generate output CSV"):
                processed_df = process_csv_data(df)
                time.sleep(2)
            edited_df = st.data_editor(processed_df, use_container_width=True)

        # Extract original file name without extension
        original_file_name = uploaded_file.name.split(".")[0]

        # Create updated file name
        updated_file_name = f"updated_{original_file_name}.csv"

        # Convert final DataFrame to CSV
        csv_data = convert_df_to_csv(edited_df)

        # Provide download button for the edited CSV
        st.download_button(
            label="💾 Download Output CSV",
            data=csv_data,
            file_name=updated_file_name,
            mime="text/csv",
        )

# Footer with a helpful message
st.markdown("""
    <style>
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.9rem;
            color: #888;
        }
    </style>
    <div class="footer">Built with ❤️ using Streamlit</div>
""", unsafe_allow_html=True)
