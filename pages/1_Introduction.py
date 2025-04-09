import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Introduction to Logarithms",
    page_icon="📚",
    layout="wide"
)

st.title("Introduction to Logarithms")

st.markdown("""
### What is a Logarithm?

A logarithm is the inverse operation to exponentiation. This means that a logarithm answers the question:

> "**To what power** must a given base be raised to produce a given number?"

For example, if we want to find the logarithm base 10 of 100, we're asking:
"To what power must 10 be raised to get 100?"
Since 10² = 100, the logarithm base 10 of 100 is 2.

We write this as: log₁₀(100) = 2
""")

st.markdown("---")

st.subheader("Basic Definition")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    Mathematically, if:
    
    $$y = \log_b(x)$$
    
    This is equivalent to:
    
    $$b^y = x$$
    
    Where:
    - **b** is the base of the logarithm
    - **x** is the number we're taking the logarithm of (input)
    - **y** is the result of the logarithm (output)
    
    ### Common Bases
    
    The most commonly used logarithm bases are:
    
    - **Base 10** (Common logarithm): Written as log₁₀(x) or often just log(x)
    - **Base e ≈ 2.71828** (Natural logarithm): Written as log_e(x) or ln(x)
    - **Base 2** (Binary logarithm): Written as log₂(x)
    
    Each base has specific applications in different fields, which we'll explore later.
    """)

with col2:
    # Create an interactive example
    st.markdown("### Try it yourself:")
    
    base = st.selectbox("Select a base:", [2, "e (≈2.71828)", 10], index=2)
    
    if base == "e (≈2.71828)":
        base_value = np.e
        base_display = "e"
    else:
        base_value = base
        base_display = str(base)
    
    number = st.slider("Select a number (x):", 0.1, 100.0, 10.0)
    
    if base_value == 10:
        log_result = np.log10(number)
        log_notation = f"log₁₀({number}) ≈ {log_result:.4f}"
    elif base_value == np.e:
        log_result = np.log(number)
        log_notation = f"ln({number}) ≈ {log_result:.4f}"
    else:
        log_result = np.log2(number)
        log_notation = f"log₂({number}) ≈ {log_result:.4f}"
    
    st.markdown(f"**Result:** {log_notation}")
    st.markdown(f"This means: {base_display}^{log_result:.4f} ≈ {number}")

st.markdown("---")

st.subheader("Properties of Logarithms")

st.markdown("""
Logarithms have several important properties that make them useful in various calculations:

1. **Product Rule**: $\log_b(x \cdot y) = \log_b(x) + \log_b(y)$
   - The logarithm of a product equals the sum of the logarithms

2. **Quotient Rule**: $\log_b(x / y) = \log_b(x) - \log_b(y)$
   - The logarithm of a quotient equals the difference of the logarithms

3. **Power Rule**: $\log_b(x^n) = n \cdot \log_b(x)$
   - The logarithm of a power equals the exponent times the logarithm

4. **Base Switch Formula**: $\log_b(x) = \frac{\log_a(x)}{\log_a(b)}$
   - This allows conversion between different logarithm bases

5. **Special Values**:
   - $\log_b(1) = 0$ (since $b^0 = 1$ for any base $b$)
   - $\log_b(b) = 1$ (since $b^1 = b$ for any base $b$)
""")

st.markdown("---")

st.subheader("The Relationship Between Logarithmic and Exponential Functions")

col1, col2 = st.columns([3, 2])

with col1:
    # Create a figure for the relationship
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate data for the plot
    x = np.linspace(-2, 4, 1000)
    y_exp = np.power(10, x)
    
    x_log = np.linspace(0.01, 10, 1000)
    y_log = np.log10(x_log)
    
    # Plot the exponential and logarithmic functions
    ax.plot(x, y_exp, label='10^x (exponential)', color='blue')
    ax.plot(x_log, y_log, label='log₁₀(x) (logarithmic)', color='red')
    
    # Plot the line y = x
    ax.plot([-2, 4], [-2, 4], label='y = x', linestyle='--', color='green')
    
    # Set axis limits
    ax.set_xlim(-2, 4)
    ax.set_ylim(-2, 4)
    
    # Add grid, legend, and labels
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Logarithmic and Exponential Functions', fontsize=14)
    
    # Display the plot
    st.pyplot(fig)

with col2:
    st.markdown("""
    **Key Relationship:**
    
    Logarithmic and exponential functions are inverses of each other.
    
    If $y = \log_b(x)$, then $x = b^y$
    
    This means:
    - The logarithmic function reflects the exponential function across the line y = x
    - Where one grows quickly, the other grows slowly
    - When we apply one function followed by its inverse, we get back to our starting point
    
    This inverse relationship is extremely useful in solving equations and modeling natural phenomena.
    """)

st.markdown("---")

st.subheader("History of Logarithms")

st.markdown("""
Logarithms were invented as a computational tool in the early 17th century:

- **John Napier** (1550-1617): Scottish mathematician who published the first tables of logarithms in 1614.
- **Henry Briggs** (1561-1630): English mathematician who introduced base-10 logarithms.

Before electronic calculators, logarithm tables were essential tools for astronomers, navigators, and scientists to perform complex calculations.

Initially, logarithms were created as a computational aid to convert multiplication into addition. In the days before calculators, this significantly simplified calculations.

Today, logarithms are widely used in science, engineering, computer science, and many other fields, which we'll explore in the "Real-World Applications" section.
""")

st.markdown("---")

st.markdown("### Continue to the next section to explore visualizations of logarithmic functions!")
