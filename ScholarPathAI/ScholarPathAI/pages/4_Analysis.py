import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.analysis import (
    perform_descriptive_statistics,
    perform_correlation_analysis,
    perform_hypothesis_test,
    normalize_data
)

def data_upload():
    st.header("Data Upload")
    
    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type="csv")
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            st.session_state.data = data
            st.success("Data uploaded successfully!")
            return data
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    return None

def descriptive_analysis(data):
    st.header("Descriptive Analysis")
    
    # Select numerical columns
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    if not len(numerical_cols):
        st.warning("No numerical columns found in the dataset.")
        return
    
    selected_cols = st.multiselect(
        "Select columns for analysis",
        options=numerical_cols,
        default=numerical_cols[0] if len(numerical_cols) > 0 else None
    )
    
    if selected_cols:
        stats = perform_descriptive_statistics(data[selected_cols])
        
        st.subheader("Summary Statistics")
        st.write(stats['description'])
        
        st.subheader("Distribution Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Skewness:")
            st.write(stats['skewness'])
        with col2:
            st.write("Kurtosis:")
            st.write(stats['kurtosis'])
        
        # Visualization
        st.subheader("Visualizations")
        plot_type = st.selectbox(
            "Select plot type",
            ["Histogram", "Box Plot", "Violin Plot"]
        )
        
        for col in selected_cols:
            if plot_type == "Histogram":
                fig = px.histogram(data, x=col, title=f"Histogram of {col}")
            elif plot_type == "Box Plot":
                fig = px.box(data, y=col, title=f"Box Plot of {col}")
            else:  # Violin Plot
                fig = px.violin(data, y=col, title=f"Violin Plot of {col}")
            st.plotly_chart(fig)

def correlation_analysis(data):
    st.header("Correlation Analysis")
    
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) < 2:
        st.warning("Need at least 2 numerical columns for correlation analysis.")
        return
    
    selected_cols = st.multiselect(
        "Select columns for correlation analysis",
        options=numerical_cols,
        default=list(numerical_cols)[:2]
    )
    
    if len(selected_cols) >= 2:
        corr_matrix = perform_correlation_analysis(data[selected_cols])
        
        st.subheader("Correlation Matrix")
        fig = px.imshow(
            corr_matrix,
            text=corr_matrix.round(2),
            aspect="auto",
            title="Correlation Heatmap"
        )
        st.plotly_chart(fig)

def hypothesis_testing(data):
    st.header("Hypothesis Testing")
    
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object']).columns
    
    if len(numerical_cols) == 0 or len(categorical_cols) == 0:
        st.warning("Need both numerical and categorical columns for hypothesis testing.")
        return
    
    test_type = st.selectbox(
        "Select test type",
        ["t-test", "mann-whitney"]
    )
    
    dependent_var = st.selectbox("Select dependent variable", numerical_cols)
    grouping_var = st.selectbox("Select grouping variable", categorical_cols)
    
    if st.button("Perform Test"):
        groups = data[grouping_var].unique()
        if len(groups) != 2:
            st.error("Grouping variable must have exactly 2 categories.")
            return
        
        group1_data = data[data[grouping_var] == groups[0]][dependent_var]
        group2_data = data[data[grouping_var] == groups[1]][dependent_var]
        
        results = perform_hypothesis_test(group1_data, group2_data, test_type)
        
        st.subheader("Test Results")
        st.write(f"Test statistic: {results['statistic']:.4f}")
        st.write(f"P-value: {results['p_value']:.4f}")
        st.write("Conclusion:", 
                "Significant difference found" if results['significant'] 
                else "No significant difference found")

def main():
    st.title("📊 Data Analysis")
    
    if 'data' not in st.session_state:
        data = data_upload()
        if data is None:
            return
    else:
        data = st.session_state.data
        if st.button("Upload Different Data"):
            del st.session_state.data
            st.rerun()
    
    tabs = st.tabs(["Descriptive Analysis", "Correlation Analysis", "Hypothesis Testing"])
    
    with tabs[0]:
        descriptive_analysis(data)
    
    with tabs[1]:
        correlation_analysis(data)
    
    with tabs[2]:
        hypothesis_testing(data)

if __name__ == "__main__":
    main()
