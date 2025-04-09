import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Understanding Logarithms",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("Understanding Logarithms")
st.subheader("An Interactive Educational Experience")

st.markdown("""
### Welcome to the Logarithm Explorer!

This interactive application will help you understand logarithms through:
- **Clear explanations** of logarithmic concepts
- **Visual demonstrations** of logarithmic functions
- **Real-world examples** where logarithms are used
- **Interactive calculators** to try out logarithmic calculations
- **Quizzes** to test your understanding

Navigate through the different sections using the sidebar to explore logarithms in depth.
""")

# Display a sample logarithmic function
st.subheader("Preview: The Logarithmic Function")
col1, col2 = st.columns([3, 2])

with col1:
    # Create a figure for the preview
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate data for the plot
    x = np.linspace(0.1, 10, 1000)
    log_base_10 = np.log10(x)
    log_base_e = np.log(x)  # Natural logarithm
    log_base_2 = np.log2(x)
    
    # Plot the logarithmic functions
    ax.plot(x, log_base_10, label='log₁₀(x)')
    ax.plot(x, log_base_e, label='ln(x)')
    ax.plot(x, log_base_2, label='log₂(x)')
    
    # Add grid, legend, and labels
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('log(x)', fontsize=12)
    ax.set_title('Logarithmic Functions with Different Bases', fontsize=14)
    
    # Display the plot
    st.pyplot(fig)

with col2:
    st.markdown("""
    The graph shows three common logarithmic functions:
    
    - **log₁₀(x)**: Base-10 logarithm (common logarithm)
    - **ln(x)**: Base-e logarithm (natural logarithm)
    - **log₂(x)**: Base-2 logarithm (binary logarithm)
    
    Notice how all logarithmic functions:
    - Cross the x-axis at x = 1 (log(1) = 0)
    - Increase slowly as x increases
    - Are undefined for x ≤ 0
    
    Continue to the Introduction section to learn more about logarithms!
    """)

st.markdown("---")

st.markdown("""
### Ready to start?

Use the sidebar to navigate through the different sections of this application. We recommend following the order:

1. **Introduction**: Learn what logarithms are and their basic properties
2. **Visualizations**: See how logarithmic functions behave
3. **Real-World Applications**: Discover how logarithms are used in different fields
4. **Interactive Calculators**: Try calculating logarithms with different bases
5. **Quiz**: Test your understanding of logarithms
""")
