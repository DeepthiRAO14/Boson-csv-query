import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import os


os.environ["OPENAI_API_KEY"] = "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"

try:
    from tabulate import tabulate
except ImportError as e:
    st.error(f"Error importing tabulate: {e}. Make sure it is installed.")
    st.stop()

def main():
    # Title and description
    st.title("BOSON Table Query App")
    st.write("Upload a CSV file and enter a query to get an answer.")
    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file is None:
        st.warning("Please upload a CSV file.")
        st.stop()

    data = None

    try:
        # Check if file is not None before attempting to read it
        if file is not None:
            data = pd.read_csv(file)
            st.write("Data Preview:")
            data_html = data.head(10).to_html(index=False)
            
            # Display HTML table
            st.markdown(data_html, unsafe_allow_html=True)

            # Add a fixed image at the top right
        image_path = "your_image_file.png"  # Replace with the actual filename and extension
        image_url = f"data:image/png;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}"
        
        st.markdown(
            f'<style>div.stImage img {{ float: right; }}</style>'
            f'<div style="position: fixed; top: 10px; right: 10px;"><img src="{image_url}" alt="Image" width="100"></div>',
            unsafe_allow_html=True
        )

        else:
            st.warning("File is None. Please upload a CSV file.")
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

    if data is not None:
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), data, verbose=True)

        query = st.text_input("Enter a query:")

        if st.button("Execute"):
            answer = agent.run(query)
            st.write("Answer:")
            st.write(answer)

if __name__ == "__main__":
    main()
