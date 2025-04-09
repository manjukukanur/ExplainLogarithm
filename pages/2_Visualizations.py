import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import cm

st.set_page_config(
    page_title="Logarithm Visualizations",
    page_icon="📈",
    layout="wide"
)

st.title("Visualizing Logarithmic Functions")

st.markdown("""
Visualization is a powerful way to understand the behavior of logarithmic functions. 
In this section, we'll explore various visual representations to help you develop intuition about logarithms.
""")

st.markdown("---")

st.subheader("Interactive Logarithm Explorer")

col1, col2 = st.columns([3, 2])

with col1:
    # Create an interactive Plotly figure
    base_options = {"Base 2": 2, "Base e": np.e, "Base 10": 10}
    selected_base = st.selectbox("Select logarithm base:", list(base_options.keys()))
    base = base_options[selected_base]
    
    x_range = st.slider("x-axis range:", 0.1, 100.0, (0.1, 20.0))
    
    # Generate data for the plot
    x = np.linspace(x_range[0], x_range[1], 1000)
    
    if base == 2:
        y = np.log2(x)
        title = "Logarithm Base 2 (log₂(x))"
    elif base == np.e:
        y = np.log(x)
        title = "Natural Logarithm (ln(x))"
    else:
        y = np.log10(x)
        title = "Common Logarithm (log₁₀(x))"
    
    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=title))
    
    # Add vertical line at x=1 and horizontal line at y=0
    fig.add_shape(type="line", x0=1, y0=min(y), x1=1, y1=max(y), 
                  line=dict(color="red", width=2, dash="dash"))
    fig.add_shape(type="line", x0=x_range[0], y0=0, x1=x_range[1], y1=0, 
                  line=dict(color="green", width=2, dash="dash"))
    
    # Label special points
    annotations = []
    if x_range[0] <= 1 <= x_range[1]:
        annotations.append(dict(x=1, y=0, text="(1,0)", showarrow=True, 
                               arrowhead=1, ax=30, ay=-30))
    
    if base <= x_range[1]:
        annotations.append(dict(x=base, y=1, text=f"({base},1)", showarrow=True, 
                               arrowhead=1, ax=30, ay=-30))
    
    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        annotations=annotations,
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    ### Key Observations:
    
    1. **Domain**: The logarithm is only defined for positive values (x > 0).
    
    2. **Special Points**:
       - log(1) = 0 for any base (marked with the vertical red dashed line)
       - log_b(b) = 1 (e.g., log₁₀(10) = 1)
    
    3. **Growth Rate**:
       - The function grows very rapidly for small x values
       - As x increases, the function grows much more slowly
       - This "flattening out" is key to why logarithms are useful for representing large ranges of values
    
    4. **Behavior near zero**:
       - As x approaches 0, the logarithm approaches negative infinity
       - log(x) → -∞ as x → 0⁺
    
    5. **Negative values**:
       - The logarithm is undefined for x ≤ 0
    
    Try adjusting the controls to explore how logarithms with different bases behave!
    """)

st.markdown("---")

st.subheader("Comparing Different Logarithm Bases")

# Generate data for the comparison plot
x = np.linspace(0.1, 20, 1000)
y_log2 = np.log2(x)
y_loge = np.log(x)
y_log10 = np.log10(x)

# Create the Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y_log2, mode='lines', name='log₂(x)', line=dict(color='red')))
fig.add_trace(go.Scatter(x=x, y=y_loge, mode='lines', name='ln(x)', line=dict(color='green')))
fig.add_trace(go.Scatter(x=x, y=y_log10, mode='lines', name='log₁₀(x)', line=dict(color='blue')))

# Add horizontal line at y=0
fig.add_shape(type="line", x0=0.1, y0=0, x1=20, y1=0, 
              line=dict(color="black", width=1, dash="dash"))

# Update layout
fig.update_layout(
    title="Comparison of Different Logarithm Bases",
    xaxis_title="x",
    yaxis_title="log(x)",
    height=500,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    margin=dict(l=0, r=0, t=50, b=0)
)

# Add grid
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Observations from the Comparison:

1. **All logarithms share common properties**:
   - They all pass through the point (1, 0)
   - They all increase as x increases
   - They all approach negative infinity as x approaches 0
   
2. **Growth rates differ**:
   - log₂(x) grows the fastest (since 2 is the smallest base)
   - log₁₀(x) grows the slowest (since 10 is the largest base)
   - ln(x) grows at a rate between the other two (since e ≈ 2.718)
   
3. **When to use each base**:
   - **Base 2**: Used in computer science and information theory
   - **Base e**: Used in calculus and natural sciences
   - **Base 10**: Used in engineering and for human-readable scales
""")

st.markdown("---")

st.subheader("Logarithmic vs. Linear Scale")

col1, col2 = st.columns(2)

with col1:
    # Create data for a linear plot
    x_linear = np.linspace(0, 100, 1000)
    y_linear = x_linear
    
    # Create the linear Plotly figure
    fig_linear = go.Figure()
    fig_linear.add_trace(go.Scatter(x=x_linear, y=y_linear, mode='lines', name='Linear (y = x)'))
    
    # Update layout
    fig_linear.update_layout(
        title="Linear Scale",
        xaxis_title="x",
        yaxis_title="y",
        height=400
    )
    
    # Add grid
    fig_linear.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_linear.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    st.plotly_chart(fig_linear, use_container_width=True)

with col2:
    # Create data for a logarithmic plot
    x_log = np.linspace(0, 100, 1000)
    y_log = x_log
    
    # Create the logarithmic Plotly figure
    fig_log = go.Figure()
    fig_log.add_trace(go.Scatter(x=x_log, y=y_log, mode='lines', name='Linear (y = x)'))
    
    # Update layout with logarithmic y-axis
    fig_log.update_layout(
        title="Logarithmic Scale (y-axis)",
        xaxis_title="x",
        yaxis_title="y",
        yaxis_type="log",
        height=400
    )
    
    # Add grid
    fig_log.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_log.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    st.plotly_chart(fig_log, use_container_width=True)

st.markdown("""
### Understanding Logarithmic Scales:

The plots above show the same linear function (y = x) plotted on:
1. A **linear scale** (left): Equal intervals on the axis represent equal absolute changes
2. A **logarithmic scale** (right): Equal intervals represent equal multiplicative changes

On a logarithmic scale:
- The distance from 1 to 10 is the same as the distance from 10 to 100
- This is useful for visualizing data that spans many orders of magnitude
- It helps identify patterns in exponential growth or decay

Many natural phenomena follow logarithmic patterns, and logarithmic scales help visualize these effectively.
""")

st.markdown("---")

st.subheader("Logarithmic vs. Exponential Growth")

# Generate data
x = np.linspace(0, 5, 100)
y_exp = np.exp(x)
y_linear = x + 1
y_log = np.log(x + 1)

# Create figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y_exp, mode='lines', name='Exponential (e^x)', line=dict(color='red')))
fig.add_trace(go.Scatter(x=x, y=y_linear, mode='lines', name='Linear (x + 1)', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=x, y=y_log, mode='lines', name='Logarithmic (ln(x+1))', line=dict(color='green')))

# Update layout
fig.update_layout(
    title="Comparison of Growth Rates",
    xaxis_title="x",
    yaxis_title="y",
    height=500,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

# Add grid
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Growth Rate Comparison:

This comparison illustrates the dramatic differences in growth rates:

1. **Exponential Growth** (e^x): 
   - Grows extremely rapidly
   - Each equal step in x multiplies the previous value
   - Examples: Unchecked population growth, compound interest, viral spread

2. **Linear Growth** (x + 1):
   - Grows at a constant rate
   - Each equal step in x adds the same amount
   - Examples: Simple interest, constant-speed travel

3. **Logarithmic Growth** (ln(x+1)):
   - Grows extremely slowly
   - Each multiplication of x produces equal steps in y
   - Examples: Human perception, information content, algorithm complexity

The logarithmic function is the inverse of the exponential function. Where one grows quickly, the other grows slowly.
""")

st.markdown("---")

st.subheader("3D Visualization: log(x × y)")

# Create a 3D surface plot of log(x × y) to demonstrate the product rule
x = np.linspace(0.1, 5, 50)
y = np.linspace(0.1, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.log10(X * Y)

# Create figure with subplots
fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])

# Update layout
fig.update_layout(
    title='3D Surface: log₁₀(x × y)',
    scene=dict(
        xaxis_title='x',
        yaxis_title='y',
        zaxis_title='log₁₀(x × y)'
    ),
    width=800,
    height=700,
    margin=dict(l=0, r=0, b=0, t=50)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### The Product Rule in 3D:

This 3D visualization demonstrates the logarithm product rule: log(x × y) = log(x) + log(y)

The surface shows log₁₀(x × y) for different values of x and y. Key observations:

1. The surface forms a smooth gradient increasing with both x and y
2. Doubling either x or y adds the same amount to the result
3. The surface represents the addition of log(x) and log(y) in a single function

This visual demonstrates why logarithms convert multiplication into addition, one of their most useful properties!
""")

st.markdown("---")

st.markdown("### Continue to the next section to explore real-world applications of logarithms!")
