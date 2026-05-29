import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Lecture 3", layout="wide")
st.title("Modeling Iteration")
st.header("Labour Market Dynamics")

st.markdown(
    r"""
    This interactive demo simulates a labor market with three states:
    - Unemployed ($u$)
    - Low wage job ($l$)
    - High wage job ($h$)

    **Transitions:**
    - $\mu$: probability an unemployed finds a low wage job
    - $\lambda$: probability a low wage worker becomes high wage
    - $\delta_l$: probability a low wage worker loses job
    - $\delta_h$: probability a high wage worker loses job

    The model uses difference equations to update the shares in each state over time.

    **Transition equations:**
    $$
    \begin{align*}
    u_{t+1} &= u_t + \delta_l l_t + \delta_h h_t - \mu u_t \\
    l_{t+1} &= l_t + \mu u_t - \lambda l_t - \delta_l l_t \\
    h_{t+1} &= h_t + \lambda l_t - \delta_h h_t
    \end{align*}
    $$

    **Matrix notation:**
    $$
    \begin{bmatrix}
    u_{t+1} \\
    l_{t+1} \\
    h_{t+1}
    \end{bmatrix}
    =
    \begin{bmatrix}
    1 - \mu & \delta_l & \delta_h \\
    \mu & 1 - \lambda - \delta_l & 0 \\
    0 & \lambda & 1 - \delta_h
    \end{bmatrix}
    \begin{bmatrix}
    u_t \\
    l_t \\
    h_t
    \end{bmatrix}
    $$
    """
)

st.subheader("Set Labour Market Parameters")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    mu = st.slider(r"Job finding rate $\mu$", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
with col2:
    lambda_ = st.slider(r"Learning rate $\lambda$", min_value=0.01, max_value=0.5, value=0.15, step=0.01)
with col3:
    delta_l = st.slider(r"Low wage sep. $\delta_l$", min_value=0.01, max_value=0.5, value=0.05, step=0.01)
with col4:
    delta_h = st.slider(r"High wage sep. $\delta_h$", min_value=0.01, max_value=0.5, value=0.02, step=0.01)
with col5:
    u0 = st.slider(r"Initial unemployment $u_0$", min_value=0.0, max_value=1.0, value=1.0, step=0.01)

T = 60
u_hist, l_hist, h_hist = [], [], []
u, l, h = u0, 1-u0, 0.0

for t in range(T):
    u_hist.append(u)
    l_hist.append(l)
    h_hist.append(h)
    new_l = mu * u
    l_to_h = lambda_ * l
    l_to_u = delta_l * l
    h_to_u = delta_h * h

    next_u = u + l_to_u + h_to_u - new_l
    next_l = l + new_l - l_to_h - l_to_u
    next_h = h + l_to_h - h_to_u

    total = next_u + next_l + next_h
    next_u, next_l, next_h = next_u/total, next_l/total, next_h/total

    u, l, h = next_u, next_l, next_h

fig_labour, ax = plt.subplots(figsize=(7, 4))
ax.plot(u_hist, label="Unemployed $u$")
ax.plot(l_hist, label="Low wage $l$")
ax.plot(h_hist, label="High wage $h$")
ax.axhline(y=u_hist[-1], color='gray', linestyle='--', label="Steady state $u^*$")
ax.set_title("Labor Market Markov Process Dynamics")
ax.set_xlabel("Time step")
ax.set_ylabel("Share of workers")
ax.legend()
ax.grid(True)
plt.tight_layout()
st.pyplot(fig_labour)

st.markdown(
    r"""
    **How to use this demo:**
    - Adjust the transition rates and initial unemployment.
    - The plot shows the evolution of unemployment, low wage, and high wage shares.
    - The dashed line shows the steady state unemployment.
    - Which slider(s) affect the evolution but not the steady state level of unemployment?
    - Does an increase in $\lambda$ lead to lower unemployment?
    """
)
