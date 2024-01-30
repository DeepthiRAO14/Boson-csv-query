import os
import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI



# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

try:
    from tabulate import tabulate
except ImportError as e:
    st.error(f"Error importing tabulate: {e}. Make sure it is installed.")
    st.stop()

# Define Streamlit app
def main():
      # Title and description
    st.title("BOSON Table Query App")
    with st.sidebar:
        # Add company logo at the top right
        st.image("C:\Users\Admin\Downloads", width=100,use_column_width=False, output_format='auto')
    st.write("Upload a tabular file and enter a query to get an answer.")
    file = st.file_uploader("Upload tabular file", type=["csv"])

    if file is None:
        st.warning("Please upload a CSV file.")
        st.stop()


    data = None

    try:
        # Check if file is not None before attempting to read it
        if file is not None:
            data = pd.read_csv(file)
            st.write("Data Preview:")
            st.dataframe(data.head(10),index=False)
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







