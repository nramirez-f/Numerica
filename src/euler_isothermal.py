# -*- encoding: utf-8 -*-

import plotly.graph_objects as go
import numpy as np

#
# Euler Isothermal 1D 
#

# Eigenvalues
def eigenvalue1(c, rho, m):
    if np.isscalar(rho):
        if rho == 0:
            out = 0  # only for not break, need to fix
        else:
            out = (m / rho) - c
    else:
        out = np.zeros(len(rho))
        mask = (rho == 0)
        out[mask] = 0 # only for not break, need to fix
        out[~mask] = (m[~mask] / rho[~mask]) - c
    return out

def eigenvalue2(c, rho, m):
    if np.isscalar(rho):
        if rho == 0:
            out = 0  # only for not break, need to fix
        else:
            out = (m / rho) + c
    else:
        out = np.zeros(len(rho))
        mask = (rho == 0)
        out[mask] = 0 # only for not break, need to fix
        out[~mask] = (m[~mask] / rho[~mask]) + c
    return out

# Density parametrization
def rho(rho_f, t):
    """
    Parametrization of density on shock
    """
    return rho_f + t * rho_f

# Momentum parametrization on Shock Curves
def m_1(c, rho_f, m_f, t):
    """
    Paremetrization of momentum on 1-shock
    """
    return m_f + t * (m_f - c * rho_f * np.sqrt(1 + t))

def m_2(c, rho_f, m_f, t):
    """
    Paremetrization of momentum of 2-shock
    """
    return m_f + t * (m_f + c * rho_f * np.sqrt(1 + t))

# Velocity on Curves Shocks
def s1(c, rho_f, m_f,  t):
    """
    Shock velocity of 1-shock
    """
    return (m_f / rho_f) - c * np.sqrt(1 + t)

def s2(c, rho_f, m_f,  t):
    """
    Shock velocity of 2-shock
    """
    return (m_f / rho_f) + c * np.sqrt(1 + t)

# Intersections Between Shock Curves 
def u_m(c, rho_l, m_l, rho_r, m_r):
    """
    """
    disc = pow((m_r / rho_r) - (m_l / rho_l), 2) + 4 * c * ((1 / np.sqrt(rho_r)) + (1 / np.sqrt(rho_l))) * (np.sqrt(rho_r) + np.sqrt(rho_l))

    num = - ((m_r / rho_r) - (m_l / rho_l)) + np.sqrt(disc)

    denom = 2 * c * ((1 / np.sqrt(rho_r)) + (1 / np.sqrt(rho_l)))
    
    z = num / denom

    rho_m = pow(z, 2)

    m_m = ((rho_m * m_r) / rho_r) + c * (rho_m - rho_r) * np.sqrt(rho_m / rho_r)

    state = (float(np.round(rho_m, 2)), float(np.round(m_m, 2)))

    return  state

def u_n(c, rho_l, m_l, rho_r, m_r):
    """
    """
    disc = pow((m_l / rho_l) - (m_r / rho_r), 2) + 4 * c * ((1 / np.sqrt(rho_l)) + (1 / np.sqrt(rho_r))) * (np.sqrt(rho_l) + np.sqrt(rho_r))

    num = - ((m_l / rho_l) - (m_r / rho_r)) + np.sqrt(disc)

    denom = 2 * c * ((1 / np.sqrt(rho_l)) + (1 / np.sqrt(rho_r)))
    
    z = num / denom

    rho_m = pow(z, 2)

    m_m = ((rho_m * m_l) / rho_l) + c * (rho_m - rho_l) * np.sqrt(rho_m / rho_l)

    state = (rho_m, m_m)

    return  state

# Momentum parametrization on Integral Curves
def m_ic1(c, rho_f, m_f, t):
    """
    Parametrization of momentum on the integral curve of r1
    """
    valid = t > -1
    result = np.zeros_like(t)
    result[valid] = (m_f * (1 + t[valid]) + c * rho_f * (1 + t[valid]) * np.log(1 / (1 + t[valid])))
    return result



def m_ic2(c, rho_f, m_f, t):
    """
    Parametrization of momentum on the integral curve of r1
    """
    valid = t > -1

    result = np.zeros_like(t)

    result[valid] = (m_f * (1 + t[valid]) + c * rho_f * (1 + t[valid]) * np.log(1 + t[valid]))
    
    return result



# Hugoniot Locus of a state
def hugoniot_locus(rho_f, m_f, a=1, amplitude=5):
    """
    rho:
    m:
    a: Sound speed
    """
    
    # Layout data
    delta = 0.2 

    # Parameter data
    T = -1
    while max((m_1(a, rho_f, m_f, T), m_2(a, rho_f, m_f, T))) < ((amplitude / 2) + delta) or min((m_1(a, rho_f, m_f, T), m_2(a, rho_f, m_f, T))) > (-(amplitude / 2) - delta):
        T += 0.1

    t_range = np.linspace(-1, T, 1000)

    # Shocks
    rho_values = rho(rho_f, t_range)

    # 1-Shock
    m1_values = m_1(a, rho_f, m_f, t_range)

    speed1_values = s1(a, rho_f, m_f,  t_range)
    shock1_eigenvalue1 = eigenvalue1(a, rho_values, m1_values)
    shock1_eigenvalue2 = eigenvalue2(a, rho_values, m1_values)

    shock1_data = np.array([speed1_values, shock1_eigenvalue1, shock1_eigenvalue2]).T

    split_i = next((i for i, x in enumerate(rho_values) if x > rho_f), None)

    fig = go.Figure()
    # Left
    fig.add_trace(go.Scatter(x=rho_values[:split_i], y=m1_values[:split_i],
                        mode='lines',
                        name=f'1-shock',
                        hovertemplate="ρ: %{x:.2f}<br>m: %{y:.2f}<br>s: %{customdata[0]:.2f}<br>λ1: %{customdata[1]:.2f}<br>λ2: %{customdata[2]:.2f}",
                        customdata = shock1_data[:split_i],
                        line = dict(color='blue', width=2, dash='solid'),
                        showlegend=False))

    # Right
    fig.add_trace(go.Scatter(x=rho_values[split_i:], y=m1_values[split_i:],
                        mode='lines',
                        name=f'1-shock',
                        hovertemplate="ρ: %{x:.2f}<br>m: %{y:.2f}<br>s: %{customdata[0]:.2f}<br>λ1: %{customdata[1]:.2f}<br>λ2: %{customdata[2]:.2f}",
                        customdata = shock1_data[split_i:],
                        line = dict(color='blue', width=2, dash='solid'),
                        showlegend=False))

    # 2-Shock
    m2_values = m_2(a, rho_f, m_f, t_range)

    speed2_values = s1(a, rho_f, m_f,  t_range)
    shock2_eigenvalue1 = eigenvalue1(a, rho_values, m2_values)
    shock2_eigenvalue2 = eigenvalue2(a, rho_values, m2_values)

    shock2_data = np.array([speed2_values, shock2_eigenvalue1, shock2_eigenvalue2]).T

    split_i = next((i for i, x in enumerate(rho_values) if x > rho_f), None)

    # Left
    fig.add_trace(go.Scatter(x=rho_values[:split_i], y=m2_values[:split_i],
                        mode='lines',
                        name='2-shock',
                        hovertemplate="ρ: %{x:.2f}<br>m: %{y:.2f}<br>s: %{customdata[0]:.2f}<br>λ1: %{customdata[1]:.2f}<br>λ2: %{customdata[2]:.2f}",
                        customdata = shock2_data[:split_i],
                        line = dict(color='red', width=2, dash='solid'),
                        showlegend=False))

    # Right
    fig.add_trace(go.Scatter(x=rho_values[split_i:], y=m2_values[split_i:],
                        mode='lines',
                        name='2-shock',
                        hovertemplate="ρ: %{x:.2f}<br>m: %{y:.2f}<br>s: %{customdata[0]:.2f}<br>λ1: %{customdata[1]:.2f}<br>λ2: %{customdata[2]:.2f}",
                        customdata = shock2_data[split_i:],
                        line = dict(color='red', width=2, dash='solid'),
                        showlegend=False))

    # Fix State
    fig.add_trace(go.Scatter(x=[rho_f], y=[m_f],
                        mode='markers',
                        name='',
                        hovertemplate="ρ: %{x:.2f}<br>m: %{y:.2f}<br>λ1: %{customdata[0]:.2f}<br>λ2: %{customdata[1]:.2f}",
                        customdata = [[eigenvalue1(a, rho_f, m_f), eigenvalue2(a, rho_f, m_f)]],
                        line = dict(color='black', width=4, dash='dot'),
                        showlegend=False))
        
    # Personalized Legend
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        name='Entropy S1',
        line=dict(color='blue', dash="solid"),
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        name='Entropy S2',
        line=dict(color='red', dash="solid"),
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        name='Non entropy S1',
        line=dict(color='blue', dash="dash"),
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        name='Non entropy S2',
        line=dict(color='red', dash="dash"),
        showlegend=True
    ))

    # Layout
    fig.update_layout(
            title=dict(text=f'Euler Isothermal Hugoniot Locus of state ({rho_f},{m_f})',
                    font_size=24,
                    x=0.5
            ),
            xaxis=dict(
                title=dict(text='ρ'),
                range=[-delta, amplitude + delta]
            ),
            yaxis=dict(
                title=dict(text='m'),
                range=[-(amplitude / 2) - delta, (amplitude / 2) + delta]
            ),
            legend=dict(y=0.5, font_size=16),
            updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Full Locus",
                        "method": "update",
                        "args": [{"line.dash": ["solid", "solid", "solid", "solid", None, None, None, None, None]}]
                    },
                    {
                        "label": "Shock to Right",
                        "method": "update",
                        "args": [{"line.dash": ["dash", "solid", "solid", "dash", None, None, None, None, None]}]
                    },
                    {
                        "label": "Shock to Left",
                        "method": "update",
                        "args": [{"line.dash": ["solid", "dash", "dash", "solid", None, None, None, None, None]}]
                    }
                ],
                "direction": "down",
                "showactive": True,
                "x": 1.12,
                "y": 1
            }
        ],
            annotations=[
                dict(
                    text=r"$u$",
                    x=rho_f,
                    y=m_f - 0.2,
                    showarrow=False,
                    align="center",
                    font=dict(size=20)
                ),
                dict(
                    text=f"Sound speed: {a}",
                    x=1.12,
                    y=0.8,
                    xref='paper',
                    yref='paper',
                    showarrow=False,
                    align="right",
                    font=dict(size=15)
                )
                    ]
    )

    #fig.write_html("euler_isothermal_hugoniot_locus.html")
    fig.show()