import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration for better aesthetics
st.set_page_config(
    page_title="SteelInsights: Steel Industry Data Analyzer",
    page_icon="🏭",
    layout="wide"
)

# --- App Title and Description ---
st.title("SteelInsights: Steel Industry Data Analyzer 🏭")
st.markdown("""
Welcome to **SteelInsights**! This application helps you explore and visualize your
steel industry dataset (`Steel_industry_data.csv`).
""")

# --- Data Loading ---
@st.cache_data # Cache the data loading for better performance
def load_data():
    """Loads the steel industry data from a CSV file."""
    try:
        df = pd.read_csv("Steel_industry_data.csv")
        return df
    except FileNotFoundError:
        st.error("Error: 'Steel_industry_data.csv' not found. Please ensure the file is in the same directory as the app.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None

df = load_data()

if df is not None:
    st.success("Data loaded successfully!")

    # --- Display Raw Data ---
    st.header("1. Raw Data Preview")
    st.write(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head())

    # --- Display Basic Statistics ---
    st.header("2. Data Statistics")
    st.write("Here are some descriptive statistics for your numerical columns:")
    st.dataframe(df.describe())

    # --- Data Information (Non-numerical details) ---
    st.header("3. Data Information")
    st.write("Column names and their data types:")
    info_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Unique Values': df.nunique()
    })
    st.dataframe(info_df)

    # --- Data Visualization Section ---
    st.header("4. Data Visualization")
    st.markdown("Select a column to visualize its distribution:")

    # Get all column names for selection
    columns = df.columns.tolist()
    selected_column = st.selectbox("Choose a column to plot:", columns)

    if selected_column:
        st.subheader(f"Distribution of '{selected_column}'")

        # Determine plot type based on column data type
        col_data_type = df[selected_column].dtype

        plt.figure(figsize=(10, 6))
        if pd.api.types.is_numeric_dtype(col_data_type):
            sns.histplot(df[selected_column], kde=True)
            plt.title(f'Histogram of {selected_column}')
            plt.xlabel(selected_column)
            plt.ylabel('Frequency')
        elif pd.api.types.is_string_dtype(col_data_type) or pd.api.types.is_categorical_dtype(col_data_type):
            # For categorical/object columns, show value counts
            value_counts = df[selected_column].value_counts()
            if len(value_counts) > 20: # Limit for readability
                st.warning("Too many unique categories to plot effectively. Showing top 20.")
                value_counts = value_counts.head(20)
            sns.barplot(x=value_counts.index, y=value_counts.values)
            plt.title(f'Bar Plot of {selected_column} (Top {len(value_counts)})')
            plt.xlabel(selected_column)
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right') # Rotate labels for better readability
        else:
            st.info("This column type is not yet supported for direct plotting (e.g., datetime).")

        st.pyplot(plt) # Display the plot in Streamlit
        plt.clf() # Clear the plot to prevent overlapping


    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

