import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Lecture 3", layout="wide")
st.title("Modeling Iteration")
st.header("Cournot Reaction Function Dynamics")

st.markdown(
    """
    This interactive demo illustrates the *Cournot duopoly* equilibrium using iterative best-response dynamics.

    - Two firms choose quantities $q_1$ and $q_2$.
    - Market price: $p(q_1, q_2) = 1 - q_1 - q_2$
    - Marginal cost: $c < 1$
    - Firm 1's reaction: $r_1(q_2) = \\frac{1 - q_2 - c}{2}$
    - Firm 2's reaction: $r_2(q_1) = \\frac{1 - q_1 - c}{2}$

    The process:
    1. Start at an initial $q_1$.
    2. Alternate best responses: $q_2=r_2(q_1)$ reacts to $q_1$, then $q_1=r_1(q_2)$ reacts to $q_2$, etc.
    3. Observe the path to equilibrium in $(q_1, q_2)$ space.
    """
)

st.subheader("Set Cournot Model Parameters")
colA, colB, colC = st.columns(3)
with colA:
    c_cournot = st.slider("Marginal cost $c$", min_value=0.0, max_value=0.99, value=0.2, step=0.01)
with colB:
    q1_init = st.slider("Initial $q_1$", min_value=0.0, max_value=0.99, value=0.45, step=0.01)
with colC:
    n_iter = st.slider("Number of iterations", min_value=2, max_value=30, value=14, step=1)

def reaction1(q2, c):
    return (1 - q2 - c) / 2

def reaction2(q1, c):
    return (1 - q1 - c) / 2

q1 = q1_init
points = []
for i in range(n_iter):
    if i % 2 == 0:
        q2 = reaction2(q1, c_cournot)
        points.append((q1, q2))
    else:
        q1 = reaction1(q2, c_cournot)
        points.append((q1, q2))

qs = np.linspace(0, 0.6, 200)
rf1 = [reaction1(q2, c_cournot) for q2 in qs]
rf2 = [reaction2(q1, c_cournot) for q1 in qs]

fig_cournot, ax = plt.subplots(figsize=(5, 5))
ax.plot(qs, rf1, label="Firm 1's reaction ($q_1=r_1(q_2)$)", color='blue')
ax.plot(rf2, qs, label="Firm 2's reaction ($q_2=r_2(q_1)$)", color='red')
points_arr = np.array(points)
ax.plot(points_arr[:,0], points_arr[:,1], 'ko-', label='Iterative path', markersize=7)
# Removed iteration numbering for clarity
ax.set_xlabel('$q_1$')
ax.set_ylabel('$q_2$')
ax.set_title('Nash Equilibrium Path for Cournot via Alternating Best Response')
ax.legend()
ax.grid(True)
ax.set_xlim(0, 0.6)
ax.set_ylim(0, 0.6)
plt.tight_layout()
st.pyplot(fig_cournot)

st.markdown(
    """
    **How to use this demo:**
    - Adjust the marginal cost $c$, initial $q_1$, and number of iterations.
    - The plot shows the reaction functions and the iterative path to equilibrium.
    - The Nash equilibrium $(q_1^*,q_2^*)$ is where the two reaction functions cross:
      - firm 1 plays its optimal reaction to firm 2: $q_1^* = r_1(q_2^*)$
      - and firm 2 plays its optimal reaction to firm 1: $q_2^* = r_2(q_1^*)$.
    """
)
