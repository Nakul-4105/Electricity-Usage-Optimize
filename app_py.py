import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Configuration ---
st.set_page_config(
    page_title="India Electricity Usage Optimizer",
    page_icon="⚡",
    layout="wide"
)

# --- App Title and Description ---
st.title('⚡ India Electricity Usage Optimizer')
st.markdown("An interactive tool to analyze and visualize state-wise electricity consumption patterns in India. This project helps in identifying peak usage hours to promote better energy management.")

# --- File Uploader ---
# This allows the app to be self-contained and used with the specific dataset.
uploaded_file = st.file_uploader(
    "Upload the long_data_.csv file to begin",
    type=["csv"]
)

# --- Main Application Logic ---
if uploaded_file is not None:
    # --- Data Loading and Preparation ---
    try:
        df = pd.read_csv(uploaded_file)
        # Convert 'Dates' column to datetime objects, assuming DD/MM/YYYY format
        df['datetime'] = pd.to_datetime(df['Dates'], dayfirst=True)
        df.set_index('datetime', inplace=True)
        # Drop columns that are no longer needed
        df.drop(columns=['Dates', 'latitude', 'longitude'], inplace=True)
        st.success("Dataset loaded and prepared successfully!")

        # --- State Selection Sidebar ---
        st.sidebar.header("Select a State")
        state_list = sorted(df['States'].unique())
        # Default to Maharashtra, given your location in Nashik
        default_index = state_list.index('Maharashtra') if 'Maharashtra' in state_list else 0
        selected_state = st.sidebar.selectbox(
            "State",
            state_list,
            index=default_index
        )

        st.header(f"Consumption Analysis for {selected_state}")

        # --- Filter Data for the Selected State ---
        df_state = df[df['States'] == selected_state].copy()

        # --- Analysis ---
        daily_usage = df_state['Usage'].resample('D').sum()
        df_state['hour'] = df_state.index.hour
        hourly_avg = df_state.groupby('hour')['Usage'].mean()

        # --- Visualization ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Daily Consumption Pattern")
            fig1, ax1 = plt.subplots()
            daily_usage.plot(ax=ax1, color='dodgerblue')
            ax1.set_ylabel("Total Consumption (MW)")
            ax1.set_xlabel("Date")
            plt.tight_layout()
            st.pyplot(fig1)

        with col2:
            st.subheader("Average Hourly Consumption")
            fig2, ax2 = plt.subplots()
            hourly_avg.plot(kind='bar', ax=ax2, color='coral')
            ax2.set_xlabel("Hour of Day")
            ax2.set_ylabel("Average Consumption (MW)")
            plt.xticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig2)

        # --- Optimization Suggestions ---
        st.header("💡 Optimization Suggestions")
        peak_hour = hourly_avg.idxmax()
        st.info(f"**Peak Usage Identified:** In {selected_state}, the highest average consumption occurs around **{peak_hour}:00**.")
        st.warning("**Recommendation:** To improve energy efficiency and potentially reduce costs, consider shifting high-power appliance usage away from this peak hour.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Please ensure you have uploaded the correct 'long_data_.csv' file and that it is not corrupted.")

else:
    st.info("Awaiting for the dataset to be uploaded.")
