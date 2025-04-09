import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Add utils to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logarithm_utils import log_base, explain_log_calculation, solve_logarithmic_equation

st.set_page_config(
    page_title="Logarithm Calculators",
    page_icon="🧮",
    layout="wide"
)

st.title("Interactive Logarithm Calculators")

st.markdown("""
This section provides interactive calculators to help you work with logarithms. Use these tools to:
- Calculate logarithms with different bases
- Solve logarithmic equations
- Apply logarithms to real-world problems
""")

st.markdown("---")

# Create tabs for different calculators
calculators = st.tabs([
    "Basic Logarithm Calculator", 
    "Equation Solver",
    "Change of Base Calculator",
    "Compound Interest Calculator",
    "Decibel Calculator",
    "pH Calculator"
])

# Tab 1: Basic Logarithm Calculator
with calculators[0]:
    st.header("Basic Logarithm Calculator")
    
    st.markdown("""
    This calculator evaluates logarithms with different bases and provides a step-by-step explanation.
    """)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Create input fields
        x = st.number_input("Enter value (x):", min_value=0.01, value=10.0, step=0.1)
        
        base_options = {"Base 10 (common)": 10, "Base e (natural)": np.e, "Base 2 (binary)": 2, "Custom base": 0}
        base_selection = st.selectbox("Select logarithm base:", list(base_options.keys()))
        
        custom_base = None
        if base_selection == "Custom base":
            custom_base = st.number_input("Enter custom base:", min_value=0.01, value=5.0, step=0.1, 
                                         help="Must be positive and not equal to 1")
        
        # Determine which base to use
        if base_selection == "Custom base":
            base = custom_base
        else:
            base = base_options[base_selection]
        
        # Calculate button
        if st.button("Calculate Logarithm"):
            # Calculate logarithm
            result = log_base(x, base)
            
            if result is not None:
                # Format result based on the base
                if base == 10:
                    st.success(f"log₁₀({x}) = {result:.6f}")
                elif base == np.e:
                    st.success(f"ln({x}) = {result:.6f}")
                elif base == 2:
                    st.success(f"log₂({x}) = {result:.6f}")
                else:
                    st.success(f"log_{base}({x}) = {result:.6f}")
                
                # Explanation
                st.markdown(explain_log_calculation(x, base))
            else:
                st.error("Invalid input: Please check that x > 0 and base > 0, base ≠ 1")
    
    with col2:
        st.markdown("""
        ### How This Works
        
        The logarithm base b of x, written as log_b(x), answers the question:
        
        "To what power must b be raised to get x?"
        
        In mathematical notation:
        
        If log_b(x) = y, then b^y = x
        
        ### Common Bases
        
        - **Base 10** (common logarithm): Written as log₁₀(x) or log(x)
        - **Base e** (natural logarithm): Written as ln(x)
        - **Base 2** (binary logarithm): Written as log₂(x)
        
        ### Examples
        
        - log₁₀(100) = 2 because 10² = 100
        - ln(e) = 1 because e¹ = e
        - log₂(8) = 3 because 2³ = 8
        
        ### Valid Inputs
        
        - The value x must be positive (x > 0)
        - The base must be positive and not equal to 1 (b > 0, b ≠ 1)
        """)
        
        # Create a visualization of the logarithm function
        if x > 0 and base > 0 and base != 1:
            # Create a range of x values around the input
            x_values = np.linspace(max(0.1, x/10), x*2, 1000)
            
            # Calculate logarithm values
            if base == 10:
                y_values = np.log10(x_values)
                title = "Common Logarithm (Base 10)"
                y_label = "log₁₀(x)"
            elif base == np.e:
                y_values = np.log(x_values)
                title = "Natural Logarithm (Base e)"
                y_label = "ln(x)"
            elif base == 2:
                y_values = np.log2(x_values)
                title = "Binary Logarithm (Base 2)"
                y_label = "log₂(x)"
            else:
                y_values = np.log(x_values) / np.log(base)
                title = f"Logarithm Base {base}"
                y_label = f"log_{base}(x)"
            
            # Create plot
            fig = go.Figure()
            
            # Add the logarithm curve
            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines',
                name=y_label,
                line=dict(color='blue', width=2)
            ))
            
            # Add marker for the current value
            log_result = log_base(x, base)
            if log_result is not None:
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[log_result],
                    mode='markers',
                    name=f'({x}, {log_result:.4f})',
                    marker=dict(size=10, color='red')
                ))
            
            # Add x=0 and y=0 lines
            fig.add_shape(
                type="line", x0=0, y0=min(y_values), x1=0, y1=max(y_values),
                line=dict(color="black", width=1, dash="dash")
            )
            fig.add_shape(
                type="line", x0=min(x_values), y0=0, x1=max(x_values), y1=0,
                line=dict(color="black", width=1, dash="dash")
            )
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title="x",
                yaxis_title=y_label,
                height=350,
                margin=dict(l=0, r=0, t=50, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Tab 2: Equation Solver
with calculators[1]:
    st.header("Logarithmic Equation Solver")
    
    st.markdown("""
    This calculator helps you solve different types of logarithmic equations.
    """)
    
    # Create equation type selector
    equation_type = st.selectbox(
        "Select equation type:",
        [
            "Solve log_b(x) = k for x",
            "Solve log_b(k) = x for b",
            "Compound interest: time to reach target amount"
        ]
    )
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Display input fields based on equation type
        if equation_type == "Solve log_b(x) = k for x":
            # Solving log_b(x) = k for x
            
            # Input for base b
            base_options = {"Base 10": 10, "Base e": np.e, "Base 2": 2, "Custom base": 0}
            base_selection = st.selectbox("Select base (b):", list(base_options.keys()))
            
            if base_selection == "Custom base":
                base = st.number_input("Enter custom base:", min_value=0.01, value=5.0, step=0.1, 
                                     help="Must be positive and not equal to 1")
            else:
                base = base_options[base_selection]
            
            # Input for k
            k = st.number_input("Enter value (k):", value=2.0, step=0.1)
            
            parameters = {"base": base, "k": k}
            
            if st.button("Solve Equation"):
                solution, explanation = solve_logarithmic_equation("log_x_equals_k", parameters)
                
                if solution is not None:
                    if base == 10:
                        st.success(f"Solution: For log({solution}) = {k}, x = {solution}")
                    elif base == np.e:
                        st.success(f"Solution: For ln({solution}) = {k}, x = {solution}")
                    elif base == 2:
                        st.success(f"Solution: For log₂({solution}) = {k}, x = {solution}")
                    else:
                        st.success(f"Solution: For log_{base}({solution}) = {k}, x = {solution}")
                    
                    st.markdown(explanation)
                else:
                    st.error("Invalid input: Please check your parameters.")
        
        elif equation_type == "Solve log_b(k) = x for b":
            # Solving log_b(k) = x for b
            
            # Input for k
            k = st.number_input("Enter value inside logarithm (k):", min_value=0.01, value=10.0, step=0.1)
            
            # Input for x
            x = st.number_input("Enter logarithm result (x):", value=1.0, step=0.1)
            
            parameters = {"k": k, "x": x}
            
            if st.button("Solve Equation"):
                solution, explanation = solve_logarithmic_equation("log_k_equals_x", parameters)
                
                if solution is not None:
                    st.success(f"Solution: For log_b({k}) = {x}, b = {solution:.6f}")
                    st.markdown(explanation)
                else:
                    st.error("Invalid input: Please check your parameters.")
        
        elif equation_type == "Compound interest: time to reach target amount":
            # Solving compound interest formula for time
            
            # Input for principal
            principal = st.number_input("Initial investment ($):", min_value=1.0, value=1000.0, step=100.0)
            
            # Input for interest rate
            rate = st.number_input("Annual interest rate (%):", min_value=0.0, value=5.0, step=0.1) / 100
            
            # Input for target amount
            target = st.number_input("Target amount ($):", min_value=1.0, value=2000.0, step=100.0)
            
            parameters = {"principal": principal, "rate": rate, "target": target}
            
            if st.button("Calculate Time"):
                solution, explanation = solve_logarithmic_equation("compound_interest", parameters)
                
                if solution is not None:
                    years = int(solution)
                    months = int((solution - years) * 12)
                    
                    st.success(f"Time required: {years} years and {months} months")
                    st.markdown(explanation)
                else:
                    st.error("Invalid input: Please check your parameters.")
    
    with col2:
        st.markdown("""
        ### How This Works
        
        Logarithmic equations can be solved by applying the fundamental property of logarithms:
        
        If log_b(x) = y, then b^y = x
        
        ### Common Equation Types
        
        1. **Solving for x in log_b(x) = k**
   
           This is solved by applying the exponential function:
           x = b^k
        
        2. **Solving for the base b in log_b(k) = x**
        
           This is solved by rearranging to:
           b^x = k
           b = k^(1/x)
        
        3. **Finding time in compound interest**
        
           Using the formula A = P(1+r)^t, we can solve for t:
           t = log(A/P) / log(1+r)
           
           Where:
           - A is the final amount
           - P is the principal
           - r is the interest rate
           - t is the time
        
        ### Applications
        
        These equations appear in many real-world scenarios:
        - Financial planning
        - Population growth
        - Radioactive decay
        - Sound intensity
        - pH calculations
        """)
        
        # Add visualization based on the equation type
        if equation_type == "Solve log_b(x) = k for x":
            if base > 0 and base != 1:
                # Create visualization of the solution
                x_values = np.linspace(0.1, base**(k+2), 1000)
                
                if base == 10:
                    y_values = np.log10(x_values)
                    title = "Solving log₁₀(x) = k"
                    y_label = "log₁₀(x)"
                elif base == np.e:
                    y_values = np.log(x_values)
                    title = "Solving ln(x) = k"
                    y_label = "ln(x)"
                elif base == 2:
                    y_values = np.log2(x_values)
                    title = "Solving log₂(x) = k"
                    y_label = "log₂(x)"
                else:
                    y_values = np.log(x_values) / np.log(base)
                    title = f"Solving log_{base}(x) = {k}"
                    y_label = f"log_{base}(x)"
                
                # Create plot
                fig = go.Figure()
                
                # Add the logarithm curve
                fig.add_trace(go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines',
                    name=y_label,
                    line=dict(color='blue', width=2)
                ))
                
                # Add horizontal line at y = k
                fig.add_shape(
                    type="line", x0=min(x_values), y0=k, x1=max(x_values), y1=k,
                    line=dict(color="red", width=2, dash="dash")
                )
                
                # Add the solution point
                solution_x = base ** k
                fig.add_trace(go.Scatter(
                    x=[solution_x],
                    y=[k],
                    mode='markers',
                    name=f'Solution: x = {solution_x:.4f}',
                    marker=dict(size=10, color='red')
                ))
                
                # Update layout
                fig.update_layout(
                    title=title,
                    xaxis_title="x",
                    yaxis_title=y_label,
                    height=350,
                    margin=dict(l=0, r=0, t=50, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        elif equation_type == "Solve log_b(k) = x for b":
            if k > 0 and x != 0:
                # Create visualization of the solution
                b_values = np.linspace(1.1, 10, 1000)
                y_values = np.log(k) / np.log(b_values)
                
                # Create plot
                fig = go.Figure()
                
                # Add the function curve
                fig.add_trace(go.Scatter(
                    x=b_values,
                    y=y_values,
                    mode='lines',
                    name=f'log_b({k})',
                    line=dict(color='blue', width=2)
                ))
                
                # Add horizontal line at y = x
                fig.add_shape(
                    type="line", x0=min(b_values), y0=x, x1=max(b_values), y1=x,
                    line=dict(color="red", width=2, dash="dash")
                )
                
                # Add the solution point if within range
                solution_b = k ** (1/x)
                if 1 < solution_b < 10:
                    fig.add_trace(go.Scatter(
                        x=[solution_b],
                        y=[x],
                        mode='markers',
                        name=f'Solution: b = {solution_b:.4f}',
                        marker=dict(size=10, color='red')
                    ))
                
                # Update layout
                fig.update_layout(
                    title=f"Solving log_b({k}) = {x} for b",
                    xaxis_title="Base (b)",
                    yaxis_title=f"log_b({k})",
                    height=350,
                    margin=dict(l=0, r=0, t=50, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        elif equation_type == "Compound interest: time to reach target amount":
            # Create visualization of compound interest growth
            if principal > 0 and target > principal and rate > 0:
                # Calculate time to reach target
                solution, _ = solve_logarithmic_equation("compound_interest", parameters)
                
                if solution is not None:
                    # Create data for growth curve
                    years = np.linspace(0, solution * 1.5, 100)
                    amounts = principal * (1 + rate) ** years
                    
                    # Create plot
                    fig = go.Figure()
                    
                    # Add the growth curve
                    fig.add_trace(go.Scatter(
                        x=years,
                        y=amounts,
                        mode='lines',
                        name='Investment Growth',
                        line=dict(color='green', width=2)
                    ))
                    
                    # Add horizontal line at target amount
                    fig.add_shape(
                        type="line", x0=0, y0=target, x1=max(years), y1=target,
                        line=dict(color="red", width=2, dash="dash")
                    )
                    
                    # Add vertical line at solution time
                    fig.add_shape(
                        type="line", x0=solution, y0=0, x1=solution, y1=target,
                        line=dict(color="blue", width=2, dash="dash")
                    )
                    
                    # Add the solution point
                    fig.add_trace(go.Scatter(
                        x=[solution],
                        y=[target],
                        mode='markers',
                        name=f'Target reached at {solution:.2f} years',
                        marker=dict(size=10, color='red')
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title=f"Investment Growth at {rate*100}% Annual Interest",
                        xaxis_title="Years",
                        yaxis_title="Amount ($)",
                        height=350,
                        margin=dict(l=0, r=0, t=50, b=0)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Change of Base Calculator
with calculators[2]:
    st.header("Change of Base Calculator")
    
    st.markdown("""
    This calculator demonstrates how to compute logarithms in any base using the change of base formula.
    """)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Input for value
        x = st.number_input("Enter value (x):", min_value=0.01, value=10.0, step=0.1, key="change_base_x")
        
        # Input for target base
        target_options = {"Base 10": 10, "Base e": np.e, "Base 2": 2, "Custom base": 0}
        target_selection = st.selectbox("Select target logarithm base:", list(target_options.keys()), key="target_base")
        
        if target_selection == "Custom base":
            target_base = st.number_input("Enter custom target base:", min_value=0.01, value=5.0, step=0.1, 
                                     help="Must be positive and not equal to 1", key="custom_target")
        else:
            target_base = target_options[target_selection]
        
        # Input for computation base
        comp_options = {"Base 10": 10, "Base e": np.e, "Base 2": 2, "Custom base": 0}
        comp_selection = st.selectbox("Select computation base:", list(comp_options.keys()), key="comp_base")
        
        if comp_selection == "Custom base":
            comp_base = st.number_input("Enter custom computation base:", min_value=0.01, value=3.0, step=0.1, 
                                    help="Must be positive and not equal to 1", key="custom_comp")
        else:
            comp_base = comp_options[comp_selection]
        
        if st.button("Calculate"):
            if x > 0 and target_base > 0 and target_base != 1 and comp_base > 0 and comp_base != 1:
                # Calculate logarithm with target base directly
                direct_result = log_base(x, target_base)
                
                # Calculate using change of base formula
                if comp_base == 10:
                    num = np.log10(x)
                    denom = np.log10(target_base)
                    comp_name = "log₁₀"
                elif comp_base == np.e:
                    num = np.log(x)
                    denom = np.log(target_base)
                    comp_name = "ln"
                elif comp_base == 2:
                    num = np.log2(x)
                    denom = np.log2(target_base)
                    comp_name = "log₂"
                else:
                    num = np.log(x) / np.log(comp_base)
                    denom = np.log(target_base) / np.log(comp_base)
                    comp_name = f"log_{comp_base}"
                
                change_result = num / denom
                
                # Display results
                if target_base == 10:
                    target_name = "log₁₀"
                elif target_base == np.e:
                    target_name = "ln"
                elif target_base == 2:
                    target_name = "log₂"
                else:
                    target_name = f"log_{target_base}"
                
                st.success(f"Direct calculation: {target_name}({x}) = {direct_result:.6f}")
                st.success(f"Using change of base: {target_name}({x}) = {change_result:.6f}")
                
                # Step-by-step explanation
                st.markdown(f"""
                ### Step-by-step calculation:
                
                1. We want to calculate {target_name}({x})
                
                2. Using the change of base formula:
                   {target_name}({x}) = {comp_name}({x}) / {comp_name}({target_base})
                
                3. Calculating the numerator:
                   {comp_name}({x}) = {num:.6f}
                
                4. Calculating the denominator:
                   {comp_name}({target_base}) = {denom:.6f}
                
                5. Dividing:
                   {num:.6f} / {denom:.6f} = {change_result:.6f}
                
                6. Therefore, {target_name}({x}) = {change_result:.6f}
                """)
            else:
                st.error("Invalid input: Please check that all values are positive and bases are not equal to 1.")
    
    with col2:
        st.markdown("""
        ### The Change of Base Formula
        
        The change of base formula allows you to calculate a logarithm in any base using logarithms in another base:
        
        $$\log_b(x) = \frac{\log_a(x)}{\log_a(b)}$$
        
        Where:
        - log_b(x) is the logarithm we want to calculate
        - log_a(x) and log_a(b) are logarithms in base a (which we can compute)
        
        ### Why This is Useful
        
        Most calculators and programming languages only provide logarithms in a few bases:
        - Base 10 (common logarithm)
        - Base e (natural logarithm)
        - Base 2 (binary logarithm)
        
        The change of base formula lets us calculate logarithms in any base using these built-in functions.
        
        ### Proof of the Formula
        
        If we let y = log_b(x), then:
        
        b^y = x
        
        Taking the logarithm base a of both sides:
        
        log_a(b^y) = log_a(x)
        
        Using the power property of logarithms:
        
        y × log_a(b) = log_a(x)
        
        Solving for y:
        
        y = log_a(x) / log_a(b)
        
        Since y = log_b(x), we have:
        
        log_b(x) = log_a(x) / log_a(b)
        """)
        
        # Create visualization of the change of base concept
        if x > 0 and target_base > 0 and target_base != 1 and comp_base > 0 and comp_base != 1:
            # Generate data for both logarithm curves
            x_values = np.linspace(0.1, max(x, target_base) * 1.5, 1000)
            
            # Target base logarithm
            if target_base == 10:
                y_target = np.log10(x_values)
                target_label = "log₁₀(x)"
            elif target_base == np.e:
                y_target = np.log(x_values)
                target_label = "ln(x)"
            elif target_base == 2:
                y_target = np.log2(x_values)
                target_label = "log₂(x)"
            else:
                y_target = np.log(x_values) / np.log(target_base)
                target_label = f"log_{target_base}(x)"
            
            # Computation base logarithm
            if comp_base == 10:
                y_comp = np.log10(x_values)
                comp_label = "log₁₀(x)"
            elif comp_base == np.e:
                y_comp = np.log(x_values)
                comp_label = "ln(x)"
            elif comp_base == 2:
                y_comp = np.log2(x_values)
                comp_label = "log₂(x)"
            else:
                y_comp = np.log(x_values) / np.log(comp_base)
                comp_label = f"log_{comp_base}(x)"
            
            # Create plot
            fig = go.Figure()
            
            # Add the logarithm curves
            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_target,
                mode='lines',
                name=target_label,
                line=dict(color='blue', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_comp,
                mode='lines',
                name=comp_label,
                line=dict(color='green', width=2)
            ))
            
            # Add marker for the point of interest
            target_y = log_base(x, target_base)
            comp_y = log_base(x, comp_base)
            
            fig.add_trace(go.Scatter(
                x=[x],
                y=[target_y],
                mode='markers',
                name=f'{target_label} = {target_y:.4f}',
                marker=dict(size=10, color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=[x],
                y=[comp_y],
                mode='markers',
                name=f'{comp_label} = {comp_y:.4f}',
                marker=dict(size=10, color='green')
            ))
            
            # Update layout
            fig.update_layout(
                title="Comparison of Logarithm Bases",
                xaxis_title="x",
                yaxis_title="log(x)",
                height=350,
                margin=dict(l=0, r=0, t=50, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Tab 4: Compound Interest Calculator
with calculators[3]:
    st.header("Compound Interest Calculator")
    
    st.markdown("""
    This calculator demonstrates the application of logarithms in financial calculations.
    """)
    
    st.subheader("Investment Growth Calculator")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Input for investment parameters
        principal = st.number_input("Initial investment ($):", min_value=100, max_value=1000000, value=1000, step=100)
        rate = st.slider("Annual interest rate (%):", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
        years = st.slider("Investment period (years):", min_value=1, max_value=50, value=10, step=1)
        
        # Calculate final amount
        rate_decimal = rate / 100
        final_amount = principal * (1 + rate_decimal) ** years
        
        # Calculate doubling time
        doubling_time = np.log(2) / np.log(1 + rate_decimal)
        
        # Display results
        st.markdown(f"""
        ### Results:
        
        **Initial investment:** ${principal:,.2f}
        
        **Annual interest rate:** {rate}%
        
        **Time period:** {years} years
        
        **Final amount:** ${final_amount:,.2f}
        
        **Time to double investment:** {doubling_time:.2f} years
        
        **Rule of 72 approximation:** {72/rate:.2f} years
        """)
    
    with col2:
        st.markdown("""
        ### Logarithms in Compound Interest
        
        Compound interest calculations rely on logarithms, particularly when solving for time.
        
        #### The Compound Interest Formula
        
        The basic formula is:
        
        A = P(1 + r)^t
        
        Where:
        - A is the final amount
        - P is the principal (initial investment)
        - r is the interest rate (as a decimal)
        - t is the time in years
        
        #### Solving for Time
        
        To find how long it takes to reach a target amount:
        
        1. Start with A = P(1 + r)^t
        2. Divide both sides by P: A/P = (1 + r)^t
        3. Take the logarithm of both sides: log(A/P) = t × log(1 + r)
        4. Solve for t: t = log(A/P) / log(1 + r)
        
        #### The Doubling Time Formula
        
        To find how long it takes for an investment to double:
        
        t = log(2) / log(1 + r)
        
        #### Rule of 72
        
        A quick approximation for doubling time:
        
        t ≈ 72 / (r × 100)
        
        This works because ln(2) ≈ 0.693, and 0.693 × 100 ≈ 72.
        """)
        
        # Create visualization of investment growth
        # Generate time points
        time = np.linspace(0, years, 100)
        amount = principal * (1 + rate_decimal) ** time
        
        # Create doubling time markers
        double_markers = []
        double_times = []
        double_amounts = []
        
        current_amount = principal
        current_time = 0
        
        while current_time < years:
            double_markers.append(current_amount)
            double_times.append(current_time)
            double_amounts.append(current_amount)
            
            current_amount *= 2
            current_time += doubling_time
        
        # Create plot
        fig = go.Figure()
        
        # Add the growth curve
        fig.add_trace(go.Scatter(
            x=time,
            y=amount,
            mode='lines',
            name='Investment Growth',
            line=dict(color='green', width=2)
        ))
        
        # Add doubling markers
        fig.add_trace(go.Scatter(
            x=double_times,
            y=double_amounts,
            mode='markers',
            name='Doubling Points',
            marker=dict(size=8, color='red')
        ))
        
        # Update layout
        fig.update_layout(
            title=f"Investment Growth at {rate}% Annual Interest",
            xaxis_title="Years",
            yaxis_title="Amount ($)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Investment Goal Calculator")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Input for goal parameters
        goal_principal = st.number_input("Initial investment ($):", min_value=100, max_value=1000000, value=1000, step=100, key="goal_principal")
        goal_rate = st.slider("Annual interest rate (%):", min_value=0.1, max_value=20.0, value=5.0, step=0.1, key="goal_rate")
        target_amount = st.number_input("Target amount ($):", min_value=200, max_value=10000000, value=2000, step=100)
        
        # Calculate time to reach goal
        goal_rate_decimal = goal_rate / 100
        
        # Check if target is greater than principal
        if target_amount > goal_principal and goal_rate_decimal > 0:
            goal_time = np.log(target_amount / goal_principal) / np.log(1 + goal_rate_decimal)
            
            years = int(goal_time)
            months = int((goal_time - years) * 12)
            days = int(((goal_time - years) * 12 - months) * 30)
            
            # Display results
            st.markdown(f"""
            ### Results:
            
            **Initial investment:** ${goal_principal:,.2f}
            
            **Annual interest rate:** {goal_rate}%
            
            **Target amount:** ${target_amount:,.2f}
            
            **Time to reach target:** {years} years, {months} months, and {days} days
            
            **Time in decimal years:** {goal_time:.2f} years
            """)
        else:
            if target_amount <= goal_principal:
                st.error("Target amount must be greater than the initial investment.")
            elif goal_rate_decimal <= 0:
                st.error("Interest rate must be greater than 0%.")
    
    with col2:
        st.markdown("""
        ### Calculating Time to Reach a Goal
        
        One of the most useful applications of logarithms in finance is determining how long it will take to reach a specific investment goal.
        
        #### The Process
        
        1. Set your financial goal (target amount)
        2. Determine your starting point (principal)
        3. Estimate your interest rate or investment return
        4. Use logarithms to solve for the time required
        
        #### The Formula
        
        t = log(A/P) / log(1 + r)
        
        Where:
        - t is the time needed
        - A is the target amount
        - P is the principal
        - r is the interest rate
        - log is the logarithm function
        
        #### Why Logarithms Are Needed
        
        Logarithms are essential because we need to "undo" the exponent in the compound interest formula:
        
        A = P(1 + r)^t
        
        Since t is in the exponent, we need logarithms to isolate it.
        """)
        
        # Create visualization of time to goal
        if target_amount > goal_principal and goal_rate_decimal > 0:
            # Generate data for growth curve
            max_time = min(goal_time * 1.5, 50)  # Limit to 50 years maximum
            time_points = np.linspace(0, max_time, 100)
            growth_curve = goal_principal * (1 + goal_rate_decimal) ** time_points
            
            # Create plot
            fig = go.Figure()
            
            # Add the growth curve
            fig.add_trace(go.Scatter(
                x=time_points,
                y=growth_curve,
                mode='lines',
                name='Investment Growth',
                line=dict(color='blue', width=2)
            ))
            
            # Add horizontal line at target amount
            fig.add_shape(
                type="line", x0=0, y0=target_amount, x1=max_time, y1=target_amount,
                line=dict(color="red", width=2, dash="dash")
            )
            
            # Add vertical line at goal time
            fig.add_shape(
                type="line", x0=goal_time, y0=0, x1=goal_time, y1=target_amount,
                line=dict(color="green", width=2, dash="dash")
            )
            
            # Add target point
            fig.add_trace(go.Scatter(
                x=[goal_time],
                y=[target_amount],
                mode='markers',
                name=f'Target Reached: {goal_time:.2f} years',
                marker=dict(size=10, color='green')
            ))
            
            # Update layout
            fig.update_layout(
                title=f"Time to Reach ${target_amount:,.2f} at {goal_rate}% Annual Interest",
                xaxis_title="Years",
                yaxis_title="Amount ($)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Tab 5: Decibel Calculator
with calculators[4]:
    st.header("Decibel Calculator")
    
    st.markdown("""
    This calculator demonstrates the logarithmic nature of sound intensity and the decibel scale.
    """)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Create two option tabs
        db_options = st.radio(
            "Select calculation type:",
            ["Convert intensity to decibels", "Compare two sound levels"]
        )
        
        if db_options == "Convert intensity to decibels":
            # Input for sound intensity
            intensity = st.number_input(
                "Sound intensity (W/m²):",
                min_value=1e-12,
                max_value=1e3,
                value=1e-6,
                format="%.2e"
            )
            
            # Calculate decibels
            reference = 1e-12  # Reference intensity (threshold of hearing)
            decibels = 10 * np.log10(intensity / reference)
            
            # Display result
            st.markdown(f"""
            ### Results:
            
            **Sound intensity:** {intensity:.2e} W/m²
            
            **Sound level:** {decibels:.1f} dB
            """)
            
            # Provide context
            common_sounds = {
                "Threshold of hearing": 0,
                "Rustling leaves": 10,
                "Whisper": 20,
                "Quiet library": 30,
                "Normal conversation": 60,
                "Busy traffic": 70,
                "Vacuum cleaner": 75,
                "Lawn mower": 90,
                "Rock concert": 110,
                "Jet engine at 100m": 140
            }
            
            # Find the closest common sounds
            db_array = np.array(list(common_sounds.values()))
            closest_idx = np.abs(db_array - decibels).argmin()
            closest_sound = list(common_sounds.keys())[closest_idx]
            
            st.markdown(f"""
            **Comparison:** This is approximately the sound level of {closest_sound} ({db_array[closest_idx]} dB).
            """)
        
        else:  # Compare two sound levels
            # Input for two sound levels
            level1 = st.slider("First sound level (dB):", min_value=0, max_value=150, value=70, step=5)
            level2 = st.slider("Second sound level (dB):", min_value=0, max_value=150, value=90, step=5)
            
            # Calculate intensity ratio
            intensity_ratio = 10 ** ((level2 - level1) / 10)
            
            # Calculate perceived loudness ratio (approximately)
            loudness_ratio = 2 ** ((level2 - level1) / 10)
            
            # Display results
            st.markdown(f"""
            ### Results:
            
            **Sound level difference:** {abs(level2 - level1)} dB
            
            **Intensity ratio:** {intensity_ratio:.1f}× {("greater" if level2 > level1 else "less")}
            
            **Perceived loudness ratio:** Approximately {loudness_ratio:.1f}× {("louder" if level2 > level1 else "quieter")}
            """)
    
    with col2:
        st.markdown("""
        ### Decibels and Logarithms
        
        The decibel (dB) scale uses logarithms to express sound intensity in a more manageable range.
        
        #### The Decibel Formula
        
        Sound level in decibels is calculated as:
        
        dB = 10 × log₁₀(I/I₀)
        
        Where:
        - I is the sound intensity being measured (in W/m²)
        - I₀ is the reference intensity (10⁻¹² W/m², the threshold of human hearing)
        
        #### Why Use a Logarithmic Scale?
        
        Human hearing spans an enormous range of intensities:
        
        - The quietest audible sound (threshold of hearing): 10⁻¹² W/m²
        - Painfully loud sounds: 10 W/m²
        - That's a ratio of 10¹³ (10 trillion)!
        
        #### Key Properties of the Decibel Scale
        
        - **+3 dB**: Doubles the sound intensity
        - **+10 dB**: 10× the sound intensity, perceived as about twice as loud
        - **+20 dB**: 100× the sound intensity
        - **+30 dB**: 1,000× the sound intensity
        
        #### Hearing Damage Risk
        
        - **85 dB**: Hearing damage possible with prolonged exposure
        - **120 dB**: Pain threshold, immediate risk
        - **140+ dB**: Immediate damage risk even with brief exposure
        """)
        
        # Create a visualization of the decibel scale
        # Define common sounds and their dB levels
        sounds = {
            "Threshold of hearing": 0,
            "Rustling leaves": 10,
            "Whisper": 20,
            "Quiet library": 30,
            "Refrigerator hum": 40,
            "Quiet office": 50,
            "Normal conversation": 60,
            "Busy traffic": 70,
            "Vacuum cleaner": 75,
            "Alarm clock": 80,
            "Lawn mower": 90,
            "Motorcycle": 100,
            "Rock concert": 110,
            "Thunder": 120,
            "Jet engine at 100m": 140
        }
        
        # Create DataFrame
        df_sounds = pd.DataFrame({
            'Sound': list(sounds.keys()),
            'Decibels': list(sounds.values())
        })
        
        # Create horizontal bar chart
        fig = px.bar(
            df_sounds,
            x='Decibels',
            y='Sound',
            orientation='h',
            color='Decibels',
            color_continuous_scale=['green', 'yellow', 'orange', 'red'],
            title="Common Sounds on the Decibel Scale"
        )
        
        # Add annotations for danger thresholds
        fig.add_vline(x=85, line_dash="dash", line_color="orange",
                     annotation_text="Prolonged exposure risk (85 dB)",
                     annotation_position="top")
        
        fig.add_vline(x=120, line_dash="dash", line_color="red",
                     annotation_text="Pain threshold (120 dB)",
                     annotation_position="top")
        
        # Update layout
        fig.update_layout(
            height=500,
            xaxis_title="Sound Level (dB)",
            yaxis_title=""
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 6: pH Calculator
with calculators[5]:
    st.header("pH Calculator")
    
    st.markdown("""
    This calculator demonstrates the logarithmic relationship between pH and hydrogen ion concentration.
    """)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Create two option tabs
        ph_options = st.radio(
            "Select calculation type:",
            ["Calculate pH from [H⁺]", "Calculate [H⁺] from pH"]
        )
        
        if ph_options == "Calculate pH from [H⁺]":
            # Input for hydrogen ion concentration
            h_concentration = st.number_input(
                "Hydrogen ion concentration [H⁺] (mol/L):",
                min_value=1e-14,
                max_value=10.0,
                value=1e-7,
                format="%.2e"
            )
            
            # Calculate pH
            ph = -np.log10(h_concentration)
            
            # Display result
            st.markdown(f"""
            ### Results:
            
            **Hydrogen ion concentration [H⁺]:** {h_concentration:.2e} mol/L
            
            **pH:** {ph:.2f}
            
            **Classification:** {'Acidic' if ph < 7 else 'Neutral' if ph == 7 else 'Basic'}
            """)
            
            # Calculate comparison to neutral
            if ph < 7:
                times_acidic = 10 ** (7 - ph)
                st.markdown(f"This solution is {times_acidic:.1e} times more acidic than pure water.")
            elif ph > 7:
                times_basic = 10 ** (ph - 7)
                st.markdown(f"This solution is {times_basic:.1e} times more basic than pure water.")
        
        else:  # Calculate [H⁺] from pH
            # Input for pH
            ph = st.slider("pH:", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
            
            # Calculate hydrogen ion concentration
            h_concentration = 10 ** (-ph)
            
            # Display result
            st.markdown(f"""
            ### Results:
            
            **pH:** {ph:.1f}
            
            **Hydrogen ion concentration [H⁺]:** {h_concentration:.2e} mol/L
            
            **Classification:** {'Acidic' if ph < 7 else 'Neutral' if ph == 7 else 'Basic'}
            """)
            
            # Calculate comparison to neutral
            if ph < 7:
                times_acidic = 10 ** (7 - ph)
                st.markdown(f"This solution is {times_acidic:.1e} times more acidic than pure water.")
            elif ph > 7:
                times_basic = 10 ** (ph - 7)
                st.markdown(f"This solution is {times_basic:.1e} times more basic than pure water.")
    
    with col2:
        st.markdown("""
        ### pH and Logarithms
        
        The pH scale uses logarithms to express hydrogen ion concentration in a more manageable range.
        
        #### The pH Formula
        
        pH is calculated as:
        
        pH = -log₁₀([H⁺])
        
        Where:
        - [H⁺] is the hydrogen ion concentration in moles per liter (mol/L)
        
        #### Why Use a Logarithmic Scale?
        
        Hydrogen ion concentrations in solutions vary by many orders of magnitude:
        
        - Strong acids: [H⁺] ≈ 1 mol/L (pH ≈ 0)
        - Pure water: [H⁺] = 10⁻⁷ mol/L (pH = 7)
        - Strong bases: [H⁺] ≈ 10⁻¹⁴ mol/L (pH ≈ 14)
        
        #### Key Properties of the pH Scale
        
        - **pH < 7**: Acidic solutions
        - **pH = 7**: Neutral (pure water at 25°C)
        - **pH > 7**: Basic (alkaline) solutions
        
        - Each 1-unit decrease in pH represents a 10× increase in acidity
        - Each 1-unit increase in pH represents a 10× increase in alkalinity
        
        #### Applications of pH
        
        - **Medicine**: Blood pH must be maintained between 7.35-7.45
        - **Agriculture**: Soil pH affects nutrient availability
        - **Food industry**: pH affects taste, preservation, and safety
        - **Water treatment**: pH monitoring ensures water quality
        - **Manufacturing**: pH control is critical in many industrial processes
        """)
        
        # Create a visualization of the pH scale
        # Define common substances and their pH levels
        substances = {
            "Battery acid": 0.5,
            "Stomach acid": 1.5,
            "Lemon juice": 2.5,
            "Vinegar": 3,
            "Orange juice": 3.5,
            "Tomato juice": 4.5,
            "Coffee": 5,
            "Tea": 5.5,
            "Milk": 6.5,
            "Pure water": 7,
            "Blood": 7.4,
            "Sea water": 8,
            "Baking soda": 8.5,
            "Toothpaste": 9.5,
            "Milk of magnesia": 10.5,
            "Ammonia": 11,
            "Soapy water": 12,
            "Bleach": 12.5,
            "Lye (NaOH)": 13.5
        }
        
        # Create DataFrame
        df_ph = pd.DataFrame({
            'Substance': list(substances.keys()),
            'pH': list(substances.values())
        })
        
        # Create horizontal bar chart
        fig = px.bar(
            df_ph,
            x='pH',
            y='Substance',
            orientation='h',
            color='pH',
            color_continuous_scale=['red', 'orange', 'green', 'cyan', 'blue', 'purple'],
            title="Common Substances on the pH Scale",
            range_color=[0, 14]
        )
        
        # Add vertical line at pH 7 (neutral)
        fig.add_vline(x=7, line_dash="dash", line_color="green",
                     annotation_text="Neutral (pH 7)",
                     annotation_position="top")
        
        # Update layout
        fig.update_layout(
            height=500,
            xaxis_title="pH Value",
            yaxis_title="",
            xaxis=dict(tickmode='linear', dtick=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("""
### Logarithms in Daily Life

As you've seen through these calculators, logarithms play a crucial role in many aspects of our lives:

- **Financial planning**: Calculating compound interest and investment growth
- **Sound engineering**: Measuring sound levels and designing audio equipment
- **Chemistry**: Measuring acidity and alkalinity
- **Engineering**: Solving complex equations and modeling natural phenomena
- **Computer science**: Analyzing algorithm efficiency and data compression

The logarithmic relationship allows us to work with values that span many orders of magnitude in a more intuitive way. This is why logarithmic scales are so prevalent in science and engineering.

Continue to the Quiz section to test your understanding of logarithms!
""")
