# main.py
import streamlit as st
import pandas as pd
from main import print_hi, init_projecct  # Import the function from the different module
from wikipedia.src.visualization.data_visualization import plot_median_views_per_day

# Custom CSS for drag and drop
custom_css = """
<style>
#upload-file {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
}
</style>
"""


# Function to create sample DataFrame
def create_sample_df():
    data = {
        'Column1': ['value1', 'value2', 'value3'],
        'Column2': [10, 20, 30],
        'Column3': [True, False, True]
    }
    return pd.DataFrame(data)


def main():
    st.sidebar.title("Navigation")

    if st.sidebar.button("Time Series"):
        st.title("Line Chart")
        # Add your line chart code here
        plot_median_views_per_day()

    if st.sidebar.button("Bar Chart"):
        st.title("Bar Chart")
        # Add your bar chart code here


    # Button to call function from different module
    if st.button("Call Function from Other Module"):
        print_hi("ashdvahsvd")  # Call the function from the different module


if __name__ == "__main__":
    init_projecct()
    main()
