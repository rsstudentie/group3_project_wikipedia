# main.py
import streamlit as st
import pandas as pd
from main import print_hi, init_projecct  # Import the function from the different module

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

    if st.sidebar.button("Line Chart"):
        st.title("Line Chart")
        # Add your line chart code here

    if st.sidebar.button("Bar Chart"):
        st.title("Bar Chart")
        # Add your bar chart code here

    st.sidebar.title("File Upload")

    if st.sidebar.button("Upload File"):
        st.title("Upload File")
        st.write("Drag and drop a CSV file here, or use the browse files button below.")

        # Display custom CSS for drag and drop
        st.markdown(custom_css, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)

        st.write("Or")

        # Display sample file structure
        st.subheader("Sample File Structure:")
        sample_df = create_sample_df()
        st.table(sample_df.head())

        # Button to download sample file
        if st.button("Download Sample CSV"):
            sample_csv = sample_df.to_csv(index=False)
            st.download_button(
                label="Download Sample CSV",
                data=sample_csv,
                file_name='sample_data.csv',
                mime='text/csv'
            )

    # If a DataFrame is displayed, offer to download it
    if 'df' in locals():
        if st.button("Download Displayed CSV"):
            displayed_csv = df.to_csv(index=False)
            st.download_button(
                label="Download Displayed CSV",
                data=displayed_csv,
                file_name='displayed_data.csv',
                mime='text/csv'
            )

    # Button to call function from different module
    if st.button("Call Function from Other Module"):
        print_hi("ashdvahsvd")  # Call the function from the different module


if __name__ == "__main__":
    init_projecct()
    main()
