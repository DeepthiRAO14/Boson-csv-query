import os
import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI



# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"



# Define Streamlit app
def main():
      # Title and description
    st.title("BOSON CSV Query App")
    st.write("Upload a CSV file and enter a query to get an answer.")
    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file is None:
        st.warning("Please upload a CSV file.")
        st.stop()

    st.write(f"File type: {type(file)}, File content: {file}")

    data = None

    try:
        # Check if file is not None before attempting to read it
        if file is not None:
            data = pd.read_csv(file)
            st.write("Data Preview:")
            st.dataframe(data.head())
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







