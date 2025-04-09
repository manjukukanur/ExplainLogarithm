import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Real-World Applications of Logarithms",
    page_icon="🌍",
    layout="wide"
)

st.title("Real-World Applications of Logarithms")

st.markdown("""
Logarithms aren't just mathematical concepts - they're widely used in many fields to model real-world phenomena
and solve practical problems. This section explores several important applications of logarithms.
""")

st.markdown("---")

# Create tabs for different application areas
tabs = st.tabs([
    "Finance & Economics", 
    "Computer Science",
    "Earth Science", 
    "Sound & Music",
    "Human Perception",
    "Information Theory"
])

# Finance & Economics Tab
with tabs[0]:
    st.header("Finance & Economics")
    
    st.subheader("Compound Interest")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create interactive compound interest calculator
        st.markdown("### Compound Interest Calculator")
        
        principal = st.number_input("Initial investment ($):", min_value=100, max_value=100000, value=1000, step=100)
        rate = st.slider("Annual interest rate (%):", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
        years = st.slider("Time period (years):", min_value=1, max_value=50, value=20, step=1)
        
        # Calculate final amount
        rate_decimal = rate / 100
        final_amount = principal * (1 + rate_decimal) ** years
        
        # Calculate doubling time using logarithm
        doubling_time = np.log(2) / np.log(1 + rate_decimal)
        
        # Generate data for graph
        time = np.linspace(0, years, 100)
        amount = principal * (1 + rate_decimal) ** time
        
        # Create plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=amount, mode='lines', name='Investment Growth'))
        
        # Update layout
        fig.update_layout(
            title="Investment Growth Over Time",
            xaxis_title="Years",
            yaxis_title="Amount ($)",
            height=400
        )
        
        # Add doubling time line if within range
        if doubling_time <= years:
            fig.add_shape(type="line", x0=doubling_time, y0=0, x1=doubling_time, y1=principal*2, 
                          line=dict(color="red", width=2, dash="dash"))
            fig.add_annotation(x=doubling_time, y=principal*2/2, 
                               text=f"Doubling Time: {doubling_time:.2f} years", 
                               showarrow=True, arrowhead=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        **Results:**
        - Initial investment: ${principal:,.2f}
        - Annual interest rate: {rate}%
        - Time period: {years} years
        - Final amount: ${final_amount:,.2f}
        - Doubling time: {doubling_time:.2f} years
        """)
    
    with col2:
        st.markdown("""
        ### Logarithms in Finance
        
        Logarithms are essential in financial calculations, particularly for:
        
        #### 1. Finding doubling time
        
        The time it takes for an investment to double can be calculated using logarithms:
        
        $T_{doubling} = \frac{\log(2)}{\log(1+r)}$
        
        Where:
        - r is the interest rate (as a decimal)
        - T is the time in years
        
        This formula comes from solving:
        
        $P(1+r)^T = 2P$
        
        for T.
        
        #### 2. Rule of 72
        
        A simplified approximation of doubling time:
        
        $T_{doubling} ≈ \frac{72}{r\%}$
        
        This quick estimation works because ln(2) ≈ 0.693, and 0.693 × 100 ≈ 72.
        
        #### 3. Calculating interest rates and time periods
        
        Logarithms help solve for unknown variables in compound interest formula:
        
        $A = P(1+r)^T$
        
        Solving for T:
        
        $T = \frac{\log(A/P)}{\log(1+r)}$
        """)
    
    st.markdown("---")
    
    st.subheader("Economic Growth and Logarithmic Scales")
    
    st.markdown("""
    ### GDP Growth on Linear vs. Logarithmic Scales
    
    Economic data often spans many orders of magnitude and grows exponentially over time.
    Logarithmic scales help visualize this data more effectively:
    
    - They show percentage changes as equal distances
    - They make exponential growth appear linear (which helps identify changes in growth rates)
    - They accommodate wide ranges of values
    """)
    
    # Sample GDP data
    years = list(range(1960, 2021, 5))
    
    # Exponential growth with some variation
    np.random.seed(42)  # For reproducibility
    base_gdp = 500  # Billion USD
    growth_rates = 1.03 + np.random.normal(0, 0.01, len(years))
    gdp_values = [base_gdp]
    
    for i in range(1, len(years)):
        gdp_values.append(gdp_values[i-1] * growth_rates[i])
    
    # Create a DataFrame
    df = pd.DataFrame({'Year': years, 'GDP (Billions $)': gdp_values})
    
    # Create subplots
    col1, col2 = st.columns(2)
    
    with col1:
        # Linear scale plot
        fig1 = px.line(df, x='Year', y='GDP (Billions $)', title='GDP Growth (Linear Scale)')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Log scale plot
        fig2 = px.line(df, x='Year', y='GDP (Billions $)', title='GDP Growth (Logarithmic Scale)', log_y=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    **Observations:**
    
    - **Linear scale** (left): Recent growth dominates the visual, earlier periods appear flat
    - **Logarithmic scale** (right): Growth rate (slope) is more consistent across time periods
    
    Economists use log scales to:
    - Compare growth rates across different time periods
    - Identify when growth is accelerating or decelerating
    - Compare economies of vastly different sizes
    """)

# Computer Science Tab
with tabs[1]:
    st.header("Computer Science")
    
    st.subheader("Algorithm Complexity")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Generate data for different algorithm complexities
        n = np.linspace(1, 100, 1000)
        constant = np.ones_like(n)
        logarithmic = np.log2(n)
        linear = n
        linearithmic = n * np.log2(n)
        quadratic = n**2
        cubic = n**3
        exponential = 2**n
        
        # Create range slider for x-axis
        max_n = st.slider("Maximum input size (n):", min_value=10, max_value=100, value=50, step=5)
        
        # Create range slider for y-axis
        log_scale = st.checkbox("Use logarithmic scale for y-axis", value=False)
        
        # Filter data based on slider
        mask = n <= max_n
        
        # Create plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=n[mask], y=constant[mask], mode='lines', name='O(1) - Constant'))
        fig.add_trace(go.Scatter(x=n[mask], y=logarithmic[mask], mode='lines', name='O(log n) - Logarithmic'))
        fig.add_trace(go.Scatter(x=n[mask], y=linear[mask], mode='lines', name='O(n) - Linear'))
        fig.add_trace(go.Scatter(x=n[mask], y=linearithmic[mask], mode='lines', name='O(n log n) - Linearithmic'))
        fig.add_trace(go.Scatter(x=n[mask], y=quadratic[mask], mode='lines', name='O(n²) - Quadratic'))
        
        # Only show cubic and exponential if the range is small enough
        if max_n <= 30:
            fig.add_trace(go.Scatter(x=n[mask], y=cubic[mask], mode='lines', name='O(n³) - Cubic'))
        if max_n <= 20:
            # Filter exponential to avoid overflow
            exp_mask = (n <= max_n) & (n <= 20)
            fig.add_trace(go.Scatter(x=n[exp_mask], y=exponential[exp_mask], mode='lines', name='O(2ⁿ) - Exponential'))
        
        # Update layout
        fig.update_layout(
            title="Algorithm Time Complexity",
            xaxis_title="Input Size (n)",
            yaxis_title="Operations",
            height=500
        )
        
        # Set logarithmic scale if selected
        if log_scale:
            fig.update_layout(yaxis_type="log")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### Logarithms in Algorithm Analysis
        
        Logarithms are fundamental in analyzing and describing algorithm efficiency:
        
        #### Common Complexity Classes
        
        - **O(1)** - Constant time: execution time doesn't depend on input size
        - **O(log n)** - Logarithmic time: execution time grows logarithmically with input
        - **O(n)** - Linear time: execution time grows linearly with input
        - **O(n log n)** - Linearithmic time: slightly worse than linear
        - **O(n²)** - Quadratic time: execution time grows with square of input
        - **O(n³)** - Cubic time: execution time grows with cube of input
        - **O(2ⁿ)** - Exponential time: execution time doubles with each additional input
        
        #### Why Logarithmic Algorithms Are Efficient
        
        Logarithmic algorithms (O(log n)) are highly efficient because they:
        
        - Reduce the problem size by a constant factor in each step
        - Can handle enormous inputs with reasonable resources
        - Grow very slowly as input size increases
        
        #### Examples of Logarithmic Algorithms
        
        - **Binary search**: O(log n)
        - **Balanced binary tree operations**: O(log n)
        - **Certain divide-and-conquer algorithms**: O(log n)
        
        These are critical for large-scale data processing and real-time systems.
        """)
    
    st.markdown("---")
    
    st.subheader("Binary Search Example")
    
    st.markdown("""
    ### Binary Search: A Logarithmic Algorithm
    
    Binary search is a classic example of a logarithmic algorithm. It works by repeatedly dividing the search space in half.
    
    Try the interactive example below. Enter a number between 1 and 100, and watch the algorithm find it in O(log n) time.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        target = st.number_input("Enter a number for the algorithm to find (1-100):", min_value=1, max_value=100, value=42)
        
        if st.button("Run Binary Search"):
            # Set up the search range
            low, high = 1, 100
            numbers = list(range(low, high + 1))
            steps = []
            found = False
            
            # Perform binary search
            iteration = 1
            while low <= high:
                mid = (low + high) // 2
                steps.append({
                    "iteration": iteration,
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "range_size": high - low + 1
                })
                
                if numbers[mid - 1] == target:
                    found = True
                    steps[-1]["result"] = "Found!"
                    break
                elif numbers[mid - 1] < target:
                    low = mid + 1
                    steps[-1]["result"] = "Target is higher"
                else:
                    high = mid - 1
                    steps[-1]["result"] = "Target is lower"
                
                iteration += 1
            
            # Display steps in a table
            df_steps = pd.DataFrame(steps)
            st.table(df_steps)
            
            # Show the logarithmic relationship
            total_steps = len(steps)
            theoretical_steps = np.ceil(np.log2(100)).astype(int)
            
            st.markdown(f"""
            **Search Results:**
            - Target number: {target}
            - Steps required: {total_steps}
            - Theoretical maximum steps (log₂(100)): {theoretical_steps}
            
            This demonstrates the logarithmic efficiency of binary search!
            """)
    
    with col2:
        st.markdown("""
        ### How Binary Search Works
        
        1. Start with a sorted array of elements
        2. Compare the target value to the middle element
        3. If they match, return the middle index
        4. If the target is less than the middle, search the left half
        5. If the target is greater than the middle, search the right half
        6. Repeat until the element is found or the search space is empty
        
        ### Logarithmic Complexity Analysis
        
        For an array of size n:
        
        - First comparison: n elements
        - Second comparison: n/2 elements
        - Third comparison: n/4 elements
        - ...and so on
        
        After k steps, we're examining n/2ᵏ elements.
        
        When n/2ᵏ = 1, we've narrowed to a single element, so:
        
        n = 2ᵏ
        
        Taking the logarithm:
        
        k = log₂(n)
        
        This is why binary search has O(log n) complexity.
        """)
    
    st.markdown("---")
    
    st.subheader("Data Compression and Information Theory")
    
    st.markdown("""
    ### Logarithms in Data Compression
    
    Logarithms are fundamental to information theory and data compression. They help measure information content
    and optimize storage requirements.
    
    #### Information Entropy
    
    The entropy of a source is measured in bits and uses logarithms:
    
    $H(X) = -\sum_{i=1}^{n} p(x_i) \log_2 p(x_i)$
    
    Where:
    - p(xᵢ) is the probability of event xᵢ
    - H(X) is the average information content in bits
    
    #### Huffman Coding Example
    
    Huffman coding is a method for lossless data compression that uses entropy and logarithms:
    
    - Frequently occurring symbols get shorter codes
    - Rarely occurring symbols get longer codes
    - The optimal code length for a symbol with probability p is approximately -log₂(p) bits
    """)
    
    # Create sample data for Huffman coding
    characters = ['A', 'B', 'C', 'D', 'E']
    frequencies = [0.4, 0.2, 0.2, 0.1, 0.1]
    
    # Calculate optimal code lengths
    optimal_lengths = [-np.log2(freq) for freq in frequencies]
    actual_lengths = [1, 2, 2, 3, 3]  # Example Huffman code lengths
    
    # Create DataFrame
    df_huffman = pd.DataFrame({
        'Character': characters,
        'Frequency': frequencies,
        'Optimal Length (-log₂(p))': [f"{length:.2f}" for length in optimal_lengths],
        'Huffman Code Length': actual_lengths
    })
    
    st.table(df_huffman)
    
    st.markdown("""
    This table shows how logarithms help determine optimal code lengths in data compression.
    Huffman coding approximates these logarithmic values with integer-length codes,
    resulting in efficient compression.
    
    **Application Areas:**
    - ZIP and other file compression formats
    - Image formats like PNG and JPEG
    - Video compression algorithms
    - Network data transmission
    """)

# Earth Science Tab
with tabs[2]:
    st.header("Earth Science")
    
    st.subheader("The Richter Scale (Earthquake Magnitude)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create an interactive Richter scale visualization
        magnitude = st.slider("Earthquake Magnitude (Richter scale):", min_value=1.0, max_value=9.5, value=5.0, step=0.1)
        
        # Calculate amplitude and energy
        amplitude_factor = 10 ** magnitude
        energy_factor = 10 ** (1.5 * magnitude)
        
        # Reference magnitude (for comparison)
        reference_magnitude = 4.0
        reference_amplitude = 10 ** reference_magnitude
        reference_energy = 10 ** (1.5 * reference_magnitude)
        
        # Calculate relative values
        amplitude_ratio = amplitude_factor / reference_amplitude
        energy_ratio = energy_factor / reference_energy
        
        # Create amplitude comparison chart
        magnitudes = np.array([reference_magnitude, magnitude])
        amplitudes = 10 ** magnitudes
        
        fig1 = px.bar(
            x=['Reference (4.0)', f'Selected ({magnitude})'],
            y=amplitudes,
            labels={'x': 'Earthquake', 'y': 'Ground Amplitude (log scale)'},
            title='Ground Amplitude Comparison',
            log_y=True
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Create energy comparison chart
        energies = 10 ** (1.5 * magnitudes)
        
        fig2 = px.bar(
            x=['Reference (4.0)', f'Selected ({magnitude})'],
            y=energies,
            labels={'x': 'Earthquake', 'y': 'Energy Released (log scale)'},
            title='Energy Comparison',
            log_y=True
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### The Richter Scale and Logarithms
        
        The Richter scale measures earthquake magnitude using logarithms:
        
        $M = \log_{10}(A) - \log_{10}(A_0)$
        
        Where:
        - M is the magnitude
        - A is the maximum amplitude measured
        - A₀ is a standard reference amplitude
        
        #### Why Use a Logarithmic Scale?
        
        Earthquakes vary enormously in strength:
        
        - A magnitude 1 earthquake is barely detectable
        - A magnitude 9 earthquake can devastate entire regions
        
        **Key Properties:**
        
        1. **Amplitude Relationship:**
           - Each 1-point increase means 10× greater amplitude
           - A magnitude 6 quake has 100× the amplitude of a magnitude 4 quake
        
        2. **Energy Relationship:**
           - Each 1-point increase means approximately 32× more energy (10^1.5)
           - A magnitude 6 quake releases about 1,000× the energy of a magnitude 4 quake
        
        #### Notable Earthquakes
        
        - **1906 San Francisco:** ~7.9
        - **1964 Alaska:** 9.2
        - **2004 Indian Ocean:** 9.1-9.3
        - **2011 Japan:** 9.0-9.1
        
        The logarithmic scale allows scientists to compare earthquakes of vastly different magnitudes using a single, manageable scale.
        """)
        
        st.markdown(f"""
        ### Current Example:
        
        **Comparing magnitude {reference_magnitude} to magnitude {magnitude}:**
        
        - **Amplitude difference:** {amplitude_ratio:.1f}× larger
        - **Energy difference:** {energy_ratio:.1f}× more energy released
        
        This demonstrates the exponential relationship between earthquake magnitudes.
        """)
    
    st.markdown("---")
    
    st.subheader("pH Scale (Acidity)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create an interactive pH scale visualization
        ph_value = st.slider("Select pH value:", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        
        # Calculate H+ concentration
        h_concentration = 10 ** (-ph_value)
        
        # Create a more comprehensive pH scale visualization
        ph_ranges = {
            "Battery Acid (0-1)": (0, 1, "red"),
            "Stomach Acid (1-3)": (1, 3, "red"),
            "Lemon Juice (2-3)": (2, 3, "red"),
            "Vinegar (2-3)": (2, 3, "red"),
            "Orange Juice (3-4)": (3, 4, "orange"),
            "Tomato Juice (4-5)": (4, 5, "orange"),
            "Coffee (5)": (5, 5.5, "orange"),
            "Milk (6.5-6.8)": (6.5, 6.8, "yellow"),
            "Pure Water (7)": (7, 7, "green"),
            "Blood (7.35-7.45)": (7.35, 7.45, "blue"),
            "Sea Water (7.5-8.4)": (7.5, 8.4, "blue"),
            "Baking Soda (8-9)": (8, 9, "blue"),
            "Antacids (9-10)": (9, 10, "purple"),
            "Ammonia (11-12)": (11, 12, "purple"),
            "Bleach (12-13)": (12, 13, "purple"),
            "Lye (13-14)": (13, 14, "purple")
        }
        
        # Create a pH scale figure
        fig = go.Figure()
        
        # Add rectangles for each pH range
        for label, (min_val, max_val, color) in ph_ranges.items():
            fig.add_trace(go.Scatter(
                x=[min_val, max_val, max_val, min_val, min_val],
                y=[0, 0, 1, 1, 0],
                fill="toself",
                fillcolor=color,
                line=dict(color="black", width=1),
                name=label,
                hoverinfo="name",
                mode="lines"
            ))
        
        # Add marker for selected pH
        fig.add_trace(go.Scatter(
            x=[ph_value],
            y=[0.5],
            mode="markers",
            marker=dict(size=20, color="black", symbol="triangle-down"),
            name=f"Selected pH: {ph_value}",
            hoverinfo="name"
        ))
        
        # Update layout
        fig.update_layout(
            title="pH Scale with Common Substances",
            xaxis=dict(title="pH Value", range=[0, 14], dtick=1),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add H+ concentration comparison
        neutral_concentration = 10 ** (-7)
        concentration_ratio = h_concentration / neutral_concentration
        
        if ph_value < 7:
            comparison_text = f"**{concentration_ratio:.1e}× more** acidic than pure water"
        elif ph_value > 7:
            comparison_text = f"**{1/concentration_ratio:.1e}× less** acidic than pure water"
        else:
            comparison_text = "Same acidity as pure water (neutral)"
        
        st.markdown(f"""
        **H⁺ ion concentration:** {h_concentration:.2e} mol/L
        
        {comparison_text}
        """)
        
        # Display comparative concentrations
        ph_values = [0, 3, 7, 10, 14]
        h_concentrations = [10 ** (-ph) for ph in ph_values]
        
        df_ph = pd.DataFrame({
            'pH': ph_values,
            'H⁺ Concentration (mol/L)': [f"{conc:.2e}" for conc in h_concentrations],
            'Compared to Neutral': [f"{(conc/neutral_concentration):.1e}×" if ph < 7 else 
                                    "1×" if ph == 7 else 
                                    f"{1/(conc/neutral_concentration):.1e}×" 
                                    for ph, conc in zip(ph_values, h_concentrations)]
        })
        
        st.table(df_ph)
    
    with col2:
        st.markdown("""
        ### The pH Scale and Logarithms
        
        The pH scale measures the acidity or alkalinity of a solution using logarithms:
        
        $pH = -\log_{10}[H^+]$
        
        Where [H⁺] is the concentration of hydrogen ions in moles per liter.
        
        #### Why Use a Logarithmic Scale?
        
        Hydrogen ion concentrations in natural and man-made substances vary by many orders of magnitude:
        
        - Strong acids have [H⁺] concentrations around 1.0 mol/L
        - Pure water has [H⁺] concentration of 10⁻⁷ mol/L
        - Strong bases have [H⁺] concentrations around 10⁻¹⁴ mol/L
        
        **Key Properties:**
        
        1. **Logarithmic Nature:**
           - Each 1-unit decrease in pH represents a 10× increase in acidity
           - pH 4 is 10× more acidic than pH 5 and 100× more acidic than pH 6
        
        2. **Neutral Point:**
           - pH 7 is neutral (neither acidic nor basic)
           - Below 7 is acidic
           - Above 7 is basic (alkaline)
        
        #### Applications of pH
        
        - **Agriculture:** Soil pH affects nutrient availability
        - **Medicine:** Blood pH must be tightly regulated (7.35-7.45)
        - **Industry:** pH control is critical in manufacturing
        - **Environment:** Monitoring water quality and acid rain
        - **Food production:** pH affects taste and preservation
        
        The logarithmic scale allows scientists to express a wide range of concentrations in a compact, manageable scale.
        """)

# Sound & Music Tab
with tabs[3]:
    st.header("Sound & Music")
    
    st.subheader("Decibel Scale (Sound Intensity)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create an interactive decibel scale visualization
        decibel_level = st.slider("Sound level (dB):", min_value=0, max_value=180, value=70, step=5)
        
        # Create reference points for common sounds
        sound_references = {
            "Threshold of hearing": 0,
            "Whisper": 20,
            "Normal conversation": 60,
            "City traffic": 80,
            "Power lawn mower": 90,
            "Rock concert": 110,
            "Jet engine at 100m": 140,
            "Rocket launch": 180
        }
        
        # Calculate intensity ratio compared to threshold of hearing
        intensity_ratio = 10 ** (decibel_level / 10)
        
        # Create visualization
        fig = go.Figure()
        
        # Add bars for reference sounds
        y_positions = list(range(len(sound_references)))
        reference_names = list(sound_references.keys())
        reference_levels = list(sound_references.values())
        
        fig.add_trace(go.Bar(
            x=reference_levels,
            y=reference_names,
            orientation='h',
            marker_color='lightblue',
            name='Reference Sounds'
        ))
        
        # Add marker for selected level
        if decibel_level in reference_levels:
            marker_y = reference_names[reference_levels.index(decibel_level)]
        else:
            marker_y = reference_names[0]  # Default position
            
        fig.add_trace(go.Scatter(
            x=[decibel_level],
            y=[marker_y],
            mode='markers',
            marker=dict(size=15, color='red', symbol='triangle-right'),
            name=f'Selected: {decibel_level} dB'
        ))
        
        # Update layout
        fig.update_layout(
            title="Common Sound Levels (dB)",
            xaxis=dict(title="Decibel Level (dB)", range=[0, 180]),
            height=400,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display intensity information
        st.markdown(f"""
        **Selected sound level: {decibel_level} dB**
        
        This is **{intensity_ratio:.2e}× more intense** than the threshold of human hearing (0 dB).
        
        **Intensity doubling:** Each +3 dB increase represents approximately a doubling of sound intensity.
        
        **Perceived loudness doubling:** Each +10 dB increase is perceived as approximately twice as loud.
        """)
        
        # Display comparative table
        db_values = [0, 10, 20, 40, 60, 80, 100, 120]
        intensity_ratios = [10 ** (db / 10) for db in db_values]
        
        df_db = pd.DataFrame({
            'Decibel Level (dB)': db_values,
            'Intensity Ratio': [f"{ratio:.1e}×" for ratio in intensity_ratios],
            'Perceived Loudness': [f"{2**(db/10):.1f}×" for db in db_values]
        })
        
        st.table(df_db)
    
    with col2:
        st.markdown("""
        ### The Decibel Scale and Logarithms
        
        The decibel (dB) scale measures sound intensity using logarithms:
        
        $dB = 10 \cdot \log_{10}\left(\frac{I}{I_0}\right)$
        
        Where:
        - I is the sound intensity being measured
        - I₀ is the reference intensity (threshold of hearing)
        
        #### Why Use a Logarithmic Scale?
        
        Human hearing spans an enormous range of intensities:
        
        - The quietest audible sound (threshold of hearing): 10⁻¹² W/m²
        - Painfully loud sounds: 10 W/m²
        - That's a ratio of 10¹³ (10 trillion)!
        
        **Key Properties:**
        
        1. **Logarithmic Nature:**
           - Each +10 dB represents 10× the sound intensity
           - Each +20 dB represents 100× the sound intensity
           - Each +30 dB represents 1,000× the sound intensity
        
        2. **Human Perception:**
           - +10 dB is perceived as approximately twice as loud
           - Our ears naturally respond logarithmically to sound intensity
        
        #### Hearing Damage Risk
        
        - **85 dB:** Hearing damage possible with prolonged exposure
        - **120 dB:** Pain threshold, immediate risk
        - **140+ dB:** Immediate damage risk even with brief exposure
        
        The logarithmic scale allows us to express this enormous range of intensities in a more manageable scale of 0-180 dB.
        """)
    
    st.markdown("---")
    
    st.subheader("Musical Scales and Frequencies")
    
    st.markdown("""
    ### Logarithms in Music: Pitch and Frequency
    
    Musical notes and intervals are based on frequency ratios, and logarithms help us understand these relationships.
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Generate frequency data for an octave
        base_note = st.selectbox("Select base note:", ["A", "B", "C", "D", "E", "F", "G"], index=0)
        
        # Base frequencies (A4 = 440 Hz)
        base_frequencies = {
            "C": 261.63,
            "D": 293.66,
            "E": 329.63,
            "F": 349.23,
            "G": 392.00,
            "A": 440.00,
            "B": 493.88
        }
        
        base_freq = base_frequencies[base_note]
        
        # Create a table of notes in an octave
        notes = []
        frequencies = []
        ratios = []
        semitones = []
        
        for i in range(13):  # 12 semitones in an octave + the octave note
            freq = base_freq * (2 ** (i / 12))
            ratio = freq / base_freq
            
            if i == 0:
                note = f"{base_note}4"
            elif i == 12:
                note = f"{base_note}5"
            else:
                # Simplistic naming - not accounting for sharps/flats properly
                steps = ["", "#", "", "#", "", "", "#", "", "#", "", "#", ""]
                note_names = ["C", "C", "D", "D", "E", "F", "F", "G", "G", "A", "A", "B"]
                
                # Calculate the position in the chromatic scale
                base_position = ["C", "D", "E", "F", "G", "A", "B"].index(base_note)
                current_position = (base_position + i) % 7
                note = f"{note_names[(base_position + i) % 12]}{steps[(base_position + i) % 12]}4"
            
            notes.append(note)
            frequencies.append(round(freq, 2))
            ratios.append(round(ratio, 3))
            semitones.append(i)
        
        # Create DataFrame
        df_notes = pd.DataFrame({
            'Note': notes,
            'Frequency (Hz)': frequencies,
            'Ratio to Base': ratios,
            'Semitones': semitones
        })
        
        st.table(df_notes)
        
        # Create a visualization of the frequency relationships
        fig = go.Figure()
        
        # Add bars for frequency
        fig.add_trace(go.Bar(
            x=notes,
            y=frequencies,
            name='Frequency (Hz)',
            marker_color='lightblue'
        ))
        
        # Add line for exponential growth
        fig.add_trace(go.Scatter(
            x=notes,
            y=frequencies,
            mode='lines+markers',
            name='Exponential growth',
            line=dict(color='red', width=2)
        ))
        
        # Update layout
        fig.update_layout(
            title=f"Frequencies of Notes (Starting from {base_note}4)",
            xaxis_title="Note",
            yaxis_title="Frequency (Hz)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### Equal Temperament and Logarithms
        
        Modern musical scales use equal temperament, which divides an octave into 12 equal semitones using logarithms.
        
        #### Mathematical Foundations
        
        The frequency of any note is related to a reference note by:
        
        $f = f_{ref} \cdot 2^{n/12}$
        
        Where:
        - f is the frequency of the note
        - f_ref is the reference frequency
        - n is the number of semitones from the reference
        
        #### Why Logarithms?
        
        1. **Octaves and Frequency Doubling:**
           - An octave higher = 2× the frequency
           - An octave lower = 1/2× the frequency
           - Each additional octave multiplies frequency by 2 again
        
        2. **Equal Temperament:**
           - Each semitone = frequency ratio of 2^(1/12) ≈ 1.059463
           - 12 semitones = 2^(12/12) = 2 (one octave)
           - The exponential relationship is most naturally described using logarithms
        
        3. **Pitch Perception:**
           - Our perception of musical intervals is based on frequency ratios, not absolute differences
           - This is inherently logarithmic
        
        #### Important Intervals
        
        - **Octave:** Ratio of 2:1 (12 semitones)
        - **Perfect fifth:** Ratio of 3:2 (7 semitones)
        - **Perfect fourth:** Ratio of 4:3 (5 semitones)
        - **Major third:** Ratio of 5:4 (4 semitones)
        
        Logarithms help create evenly spaced notes that sound harmonious across all keys.
        """)

# Human Perception Tab
with tabs[4]:
    st.header("Human Perception")
    
    st.subheader("Weber-Fechner Law (Sensation and Perception)")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create interactive Weber-Fechner demonstration
        stimulus_type = st.selectbox(
            "Choose a stimulus type:",
            ["Light intensity", "Sound intensity", "Weight perception"]
        )
        
        # Create sliders for different stimulus ranges
        if stimulus_type == "Light intensity":
            min_val, max_val = 1, 1000
            unit = "candela"
            perception_factor = 0.1  # Arbitrary factor for demonstration
        elif stimulus_type == "Sound intensity":
            min_val, max_val = 1, 1000
            unit = "dB"
            perception_factor = 0.33  # Arbitrary factor for demonstration
        else:  # Weight
            min_val, max_val = 1, 100
            unit = "kg"
            perception_factor = 0.15  # Arbitrary factor for demonstration
        
        # Use log scale for slider
        log_min, log_max = np.log10(min_val), np.log10(max_val)
        log_value = st.slider(
            f"Set {stimulus_type} (log scale):",
            min_value=log_min,
            max_value=log_max,
            value=(log_min + log_max) / 2,
            step=0.1
        )
        
        # Convert back to linear scale
        stimulus = 10 ** log_value
        
        # Calculate perceived intensity (simplified Weber-Fechner)
        perceived = perception_factor * np.log10(stimulus / min_val)
        
        # Create a chart comparing physical and perceived intensity
        # Generate data for curve
        x_range = np.logspace(log_min, log_max, 100)
        y_physical = x_range
        y_perceived = perception_factor * np.log10(x_range / min_val)
        
        # Normalize for visualization
        max_physical = max(y_physical)
        y_physical_norm = y_physical / max_physical
        y_perceived_norm = y_perceived / max(y_perceived)
        
        # Create the plot
        fig = go.Figure()
        
        # Add physical intensity line (linear)
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_physical_norm,
            mode='lines',
            name='Physical Intensity',
            line=dict(color='blue', width=2)
        ))
        
        # Add perceived intensity curve (logarithmic)
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_perceived_norm,
            mode='lines',
            name='Perceived Intensity',
            line=dict(color='red', width=2)
        ))
        
        # Add marker for current value
        fig.add_trace(go.Scatter(
            x=[stimulus],
            y=[perceived / max(y_perceived)],
            mode='markers',
            marker=dict(size=12, color='green'),
            name=f'Current: {stimulus:.1f} {unit}'
        ))
        
        # Update layout
        fig.update_layout(
            title=f"Weber-Fechner Law: {stimulus_type}",
            xaxis=dict(title=f"Physical Intensity ({unit})", type='log'),
            yaxis=dict(title="Normalized Intensity", range=[0, 1.1]),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show doubling example
        double_stimulus = stimulus * 2
        double_perceived = perception_factor * np.log10(double_stimulus / min_val)
        perceived_increase = (double_perceived - perceived) / perceived * 100
        
        st.markdown(f"""
        **Current stimulus:** {stimulus:.1f} {unit}
        
        **Perceived intensity:** {perceived:.2f} (normalized)
        
        **If the stimulus doubles to {double_stimulus:.1f} {unit}:**
        - The perceived intensity increases to {double_perceived:.2f}
        - That's only a {perceived_increase:.1f}% increase in perceived intensity
        - This demonstrates the logarithmic nature of perception!
        """)
    
    with col2:
        st.markdown("""
        ### The Weber-Fechner Law and Logarithmic Perception
        
        The Weber-Fechner Law describes how human perception relates to physical stimuli using logarithmic relationships:
        
        $S = k \cdot \log(I/I_0)$
        
        Where:
        - S is the perceived sensation
        - I is the stimulus intensity
        - I₀ is the threshold intensity
        - k is a constant that depends on the type of stimulus
        
        #### Why Perception is Logarithmic
        
        Our sensory systems evolved to respond logarithmically to stimuli because:
        
        1. **Efficiency:** It allows us to perceive a wide range of intensities
        2. **Sensitivity:** We can detect small changes at low intensities
        3. **Protection:** We're not overwhelmed by high intensities
        
        #### Examples in Everyday Life
        
        **1. Brightness Perception:**
        - A candle seems bright in a dark room
        - The same candle is barely noticeable in daylight
        - The actual difference in light intensity is enormous
        
        **2. Sound Perception:**
        - We can hear both a whisper and a rock concert
        - The sound intensity difference is over 1 trillion times
        - Our auditory system compresses this range logarithmically
        
        **3. Weight Perception:**
        - You can easily tell the difference between 100g and 105g
        - But cannot distinguish between 5kg and 5.05kg
        - The same absolute difference feels different
        
        #### Just Noticeable Difference (JND)
        
        The minimum change in stimulus that can be detected is proportional to the stimulus intensity:
        
        $\Delta I / I = k$
        
        This is Weber's Law, which leads to the logarithmic relationship in the Weber-Fechner Law.
        
        **Practical applications:**
        - User interface design
        - Audio equipment calibration
        - Lighting design
        - Food flavor intensity
        """)
    
    st.markdown("---")
    
    st.subheader("The Psychological Scales")
    
    st.markdown("""
    ### Other Logarithmic Psychological Scales
    
    Many psychological and perceptual scales use logarithmic relationships, including:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Star Magnitude (Astronomy)
        
        The apparent brightness of stars is measured on a logarithmic scale:
        
        $m_2 - m_1 = -2.5 \log_{10}(I_2/I_1)$
        
        - Each 5 magnitudes difference = factor of 100 in brightness
        - Lower magnitudes are brighter
        - The brightest stars have negative magnitudes
        - The dimmest visible stars have magnitude +6
        """)
        
        # Create a small example table
        star_data = {
            "Star": ["Sun", "Full Moon", "Venus (max)", "Sirius", "Polaris", "Faintest visible"],
            "Apparent Magnitude": [-26.7, -12.7, -4.6, -1.5, 2.0, 6.0],
            "Relative Brightness (× Polaris)": ["10^11.5", "10^6", "10^2.6", "10^1.4", "1", "0.02"]
        }
        
        df_stars = pd.DataFrame(star_data)
        st.table(df_stars)
    
    with col2:
        st.markdown("""
        #### Perceived Value (Economics)
        
        The subjective value of money follows a logarithmic curve:
        
        $V = k \cdot \log(M)$
        
        Where:
        - V is the perceived value
        - M is the monetary amount
        - k is a constant
        
        This explains why:
        - The perceived difference between $10 and $20 feels larger than between $1010 and $1020
        - Pay raises are often discussed in percentage terms rather than absolute amounts
        - Luxury goods must increase in price exponentially to maintain their exclusive perceived value
        """)
        
        # Create a simple example
        st.markdown("""
        **Example: Income increases**
        
        | Income Increase | Perceived Value Increase |
        |-----------------|--------------------------|
        | $30K → $60K     | Very significant         |
        | $60K → $90K     | Significant              |
        | $90K → $120K    | Moderate                 |
        | $1M → $1.03M    | Barely noticeable        |
        
        Despite each being a $30K increase, the perceived value differs dramatically.
        """)

# Information Theory Tab
with tabs[5]:
    st.header("Information Theory")
    
    st.subheader("Information Content and Entropy")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### Interactive Information Content Calculator
        
        The information content of an event is measured in bits and is related to its probability.
        """)
        
        # Create an interactive probability slider
        probability = st.slider(
            "Event probability:",
            min_value=0.01,
            max_value=1.0,
            value=0.5,
            step=0.01
        )
        
        # Calculate information content
        information_content = -np.log2(probability)
        
        # Display result
        st.markdown(f"""
        **Event probability:** {probability}
        
        **Information content:** {information_content:.2f} bits
        
        This means that learning this event has occurred provides {information_content:.2f} bits of information.
        """)
        
        # Generate data for information content curve
        probs = np.linspace(0.01, 1.0, 100)
        info_content = -np.log2(probs)
        
        # Create plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=probs,
            y=info_content,
            mode='lines',
            line=dict(color='blue', width=2),
            name='Information Content'
        ))
        
        # Add marker for current value
        fig.add_trace(go.Scatter(
            x=[probability],
            y=[information_content],
            mode='markers',
            marker=dict(size=12, color='red'),
            name=f'p = {probability}'
        ))
        
        # Update layout
        fig.update_layout(
            title="Information Content vs. Probability",
            xaxis=dict(title="Probability", range=[0, 1]),
            yaxis=dict(title="Information Content (bits)"),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Information entropy example
        st.subheader("Entropy Example: Coin Flips")
        
        # Create slider for coin bias
        coin_bias = st.slider(
            "Probability of Heads:",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01
        )
        
        # Calculate entropy
        p_heads = coin_bias
        p_tails = 1 - coin_bias
        
        # Handle edge cases to avoid log(0)
        if p_heads == 0:
            entropy_heads = 0
        else:
            entropy_heads = -p_heads * np.log2(p_heads)
            
        if p_tails == 0:
            entropy_tails = 0
        else:
            entropy_tails = -p_tails * np.log2(p_tails)
            
        entropy = entropy_heads + entropy_tails
        
        # Display result
        st.markdown(f"""
        **Coin bias:** P(Heads) = {p_heads}, P(Tails) = {p_tails}
        
        **Entropy:** {entropy:.4f} bits per flip
        
        This represents the average information content (uncertainty) per coin flip.
        """)
        
        # Generate entropy curve for different biases
        biases = np.linspace(0.01, 0.99, 99)
        entropies = [-p * np.log2(p) - (1-p) * np.log2(1-p) for p in biases]
        
        # Create entropy plot
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=biases,
            y=entropies,
            mode='lines',
            line=dict(color='green', width=2),
            name='Entropy'
        ))
        
        # Add marker for current value
        fig2.add_trace(go.Scatter(
            x=[coin_bias],
            y=[entropy],
            mode='markers',
            marker=dict(size=12, color='red'),
            name=f'p = {coin_bias}'
        ))
        
        # Update layout
        fig2.update_layout(
            title="Entropy of a Biased Coin",
            xaxis=dict(title="Probability of Heads", range=[0, 1]),
            yaxis=dict(title="Entropy (bits per flip)"),
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### Information Theory and Logarithms
        
        Information theory uses logarithms to quantify information content and uncertainty.
        
        #### Information Content
        
        The information content of an event with probability p is:
        
        $I(p) = -\log_2(p)$ bits
        
        **Key properties:**
        
        1. **Rare events contain more information**
           - An unlikely event (small p) has high information content
           - A certain event (p = 1) has zero information content
        
        2. **Units are in bits**
           - 1 bit = the information from a fair coin flip
           - Using log base 2 gives units in bits
           - Using log base e gives units in nats
        
        3. **Additivity for independent events**
           - If events A and B are independent, then:
           - I(A and B) = I(A) + I(B)
        
        #### Entropy
        
        Entropy measures the average information content:
        
        $H(X) = -\sum_{i} p_i \log_2(p_i)$ bits
        
        Where p_i are the probabilities of each possible outcome.
        
        **Examples:**
        
        1. **Fair coin (p = 0.5)**
           - Information of H or T: -log₂(0.5) = 1 bit
           - Entropy: 1 bit per flip
        
        2. **Biased coin (p = 0.9)**
           - Information of H: -log₂(0.9) ≈ 0.15 bits
           - Information of T: -log₂(0.1) ≈ 3.32 bits
           - Entropy: 0.9(0.15) + 0.1(3.32) ≈ 0.47 bits per flip
        
        #### Applications
        
        - **Data compression:** Optimal coding lengths
        - **Machine learning:** Feature selection, decision trees
        - **Cryptography:** Key generation, security analysis
        - **Communication:** Channel capacity, error correction
        - **Quantum computing:** Quantum information theory
        
        Information theory provides the mathematical foundation for modern computing and communication systems.
        """)

st.markdown("---")

st.markdown("""
## Summary and Key Takeaways

Logarithms are present in many aspects of our world:

1. **Finance**: Compound interest calculations and growth rates
2. **Computer Science**: Algorithm efficiency and information theory
3. **Earth Science**: Earthquake magnitudes and acidity measurements
4. **Sound and Music**: Audio levels and musical intervals
5. **Human Perception**: How we perceive stimuli follows logarithmic patterns
6. **Information Theory**: Measuring information content and entropy

The logarithmic relationship allows us to:
- Represent vast ranges of values on manageable scales
- Convert multiplicative relationships to additive ones
- Model natural phenomena that follow exponential growth or decay
- Match the way humans perceive changes in stimuli

Understanding logarithms helps us make sense of many natural and human-made systems!
""")

st.markdown("---")

st.markdown("""
#### Continue to the Interactive Calculators section to practice working with logarithms!
""")
