import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Lecture 3", layout="wide")
st.title("Modeling Iteration")
st.header("Interactive: Adverse Selection Dynamics")

st.markdown(
    """
    This interactive demo illustrates the *adverse selection* equilibrium in a market where quality is unobservable.

    - Quality $q$ is uniformly distributed on $[v_0, v_1]$.
    - Sellers only offer goods if the market price exceeds quality (their valuation of the good) $p > q$.
    - Buyers value quality at a *mark-up* over quality: $\\text{markup} \\times q$.
    - Buyers know only goods with $q < p$ are offered, so their expected quality equals $E(q|q < p)$.
    - The market moves towards equilibrium where $p = \\text{markup} \\times E(q|q < p)$.
    - If the equilibrium price falls to $v_0$, the market unravels (no trade).
    """
)

st.subheader("Set Model Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    v0 = st.slider("Lowest quality $v_0$", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
with col2:
    v1 = st.slider("Highest quality $v_1$", min_value=1.0, max_value=200.0, value=100.0, step=1.0)
with col3:
    markup = st.slider("Consumer mark-up", min_value=1.01, max_value=2.0, value=1.2, step=0.01)

if v1 <= v0:
    st.error("Highest quality $v_1$ must be greater than lowest quality $v_0$.")
else:
    def expected_q_given_p_uniform(p, a, b):
        # For q ~ Uniform(a, b), and only qualities q < p are offered
        if p < a:
            # Price below support, no goods offered
            return None
        elif p >= b:
            # All qualities are offered, expectation is mean
            return (a + b) / 2
        else:
            # Conditional mean on [a, p]
            return (a + p) / 2

    def update_price_uniform(p, a, b, markup):
        expected_q = expected_q_given_p_uniform(p, a, b)
        if expected_q is None:
            return 0
        return markup * expected_q

    p_history = []
    p = markup * v1  # Start from above the highest possible buyer willingness

    for step in range(50):
        p_history.append(p)
        new_p = update_price_uniform(p, v0, v1, markup)
        if abs(new_p - p) < 1e-6:
            break
        p = new_p

    # Determine if there is trade
    if p <= v0 + 1e-6:
        st.warning(
            f"**Market disappears (death spiral):** Equilibrium price is at the lowest quality (${v0:.2f}$). No trade occurs."
        )
    else:
        st.success(
            f"**Market equilibrium:** Price converges to $p^* = {p:.2f}$ after {step+1} steps."
        )

    # Compute fraction of products traded at each step
    fraction_traded = [(max(0, min(1, (p_i - v0) / (v1 - v0))) if v1 > v0 else 0) for p_i in p_history]
    df_plot = pd.DataFrame({
        "Price": p_history,
        "Fraction traded": fraction_traded
    })

    # --- Stack the two figures in a row using Streamlit columns ---
    col_fig1, col_fig2 = st.columns(2)

    # --- Shared y-axis for both figures, y-axis starts at 0 ---
    y_max = max(max(p_history), v1) * 1.05 if len(p_history) > 0 else v1 * 1.05

    with col_fig1:
        st.write("**Price convergence history and fraction of products traded:**")
        fig, ax1 = plt.subplots()
        color1 = "tab:blue"
        ax1.set_xlabel("Step")
        ax1.set_ylabel("Price", color=color1)
        ax1.plot(df_plot.index, df_plot["Price"], color=color1, label="Price")
        ax1.tick_params(axis="y", labelcolor=color1)
        ax1.set_ylim(0, y_max)

        ax2 = ax1.twinx()
        color2 = "tab:green"
        ax2.set_ylabel("Fraction traded", color=color2)
        ax2.plot(df_plot.index, df_plot["Fraction traded"], color=color2, linestyle="--", label="Fraction traded")
        ax2.tick_params(axis="y", labelcolor=color2)
        ax2.set_ylim(-0.05, 1.05)

        fig.tight_layout()
        st.pyplot(fig)

    with col_fig2:
        st.write("**Equilibrium as intersection of price update and 45-degree line:**")
        q_max_values = np.linspace(v0, v1, 300)
        price_update_curve = []
        for q_max in q_max_values:
            eq = expected_q_given_p_uniform(q_max, v0, v1)
            price_update_curve.append(markup * eq if eq is not None else np.nan)
        fig2, ax = plt.subplots()
        ax.plot(q_max_values, price_update_curve, label=r"$p = \mathrm{markup} \times E(q|q<p)$", color="tab:blue")
        ax.plot(q_max_values, q_max_values, label="45-degree line ($p = q_{max}$)", color="tab:orange", linestyle="--")
        ax.set_xlabel(r"Max quality traded $q_{max}$")
        ax.set_ylabel("Price")
        # Removed the title for better alignment
        ax.set_ylim(0, y_max)
        ax.legend()
        st.pyplot(fig2)

    st.markdown(
        """
        **How to use this demo:**
        - Adjust the sliders for $v_0$, $v_1$, and the mark-up.
        - Observe how the equilibrium price changes.
        - For some parameter values, the market unravels (no trade).
        - For others, trade occurs at a positive equilibrium price.
        - The second figure shows the intersection of the price update curve and the 45-degree line, which is the equilibrium.
        - Because of the markup it is efficient that all qualities are traded (buyer values the good more than the seller)
        - Using the sliders find an efficient equilibrium: which factors are important here?
        - Also find an equilibrium where the market unravels: which factors determine this outcome?
        
        **How does the interation work?**
        - We start with a high price $p_0$
        - We calculate which qualities will be on the market at this price $p_0$
        - Then we derive the expected quality given that $q < p_0$
        - We apply the mark-up to $E(q|q<p_0)$ and see whether this equals $p_0$
          - if it is equal: $p_0$ is the equilibrium price
          - if not: go through the steps above again with $p_1 =  \mathrm{markup} \\times E(q|q<p_0)$
        """
    )
