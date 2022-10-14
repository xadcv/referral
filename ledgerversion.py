import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


LIDO = 5.0


def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:,.2f}".format(num).rstrip("0").rstrip("."),
        ["", "k", "m", "bn", "tn"][magnitude],
    )


st.title("Referral Simulation")
st.subheader("Partnership parameters:")
st.write(
    "1. Guaranteed minimum payout: Hard floor on 25bps in today's terms, LDO token payout is calculated at spot"
)
st.write(
    "2. Long-term incentive baked in: If partnership is a success, even if yields compress, LDO could magnify referral bps if token appreciates"
)
st.write(
    "3. Fully exposed to upside: If yields skyrocket, Ledger doesn't leave money on the table as ETH holders flock to deposit"
)

ref_cap = 25.0
idx_take = 1.5

eth_price = st.slider("ETH Price in USD", min_value=0.0, max_value=5000.0, value=1300.0)

ldo_price = st.slider(
    "LDO Lock-in Price in (USD)", min_value=0.0, max_value=100.0, value=1.30
)
new_ldo_price = st.slider(
    "LDO price in 12mos (USD)", min_value=0.0, max_value=100.0, value=10.0
)

eth_ref = st.number_input("Number of ETH Referred", min_value=0.0, value=1.0)


data = pd.DataFrame({"yield_pcg": np.arange(0.0, 10.0, step=0.1)})
data.set_index("yield_pcg")
data["lido_take_bps"] = data["yield_pcg"] / 100 * LIDO / 100 * 10000
data["cash_bonus_bps"] = data["lido_take_bps"] * idx_take
data["ldo_bonus_bps"] = np.maximum(ref_cap - data["cash_bonus_bps"], 0)
data["tot_cash"] = data["cash_bonus_bps"] * eth_ref * eth_price / 10000
data["tot_bps"] = data["ldo_bonus_bps"] + data["cash_bonus_bps"]
data["ldo_payback"] = data["tot_bps"] / data["lido_take_bps"]
data["tot_ldo"] = data["ldo_bonus_bps"] * eth_ref * eth_price / (ldo_price * 10000)
data["tot_ldo_usd"] = data["tot_ldo"] * ldo_price
data["tot_usd"] = data["tot_ldo_usd"] + data["tot_cash"]

data["tot_ldo_usd12"] = data["tot_ldo"] * new_ldo_price
data["tot_usd12"] = data["tot_ldo_usd12"] + data["tot_cash"]
data["tot_usd12_bps"] = data["tot_usd12"] / (eth_ref * eth_price) * 10000

fig1 = go.Figure()
fig1.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["cash_bonus_bps"],
        name="Cash Rewards (bps)",
        line_color="rgb(3,163,255)",
    )
)
fig1.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["ldo_bonus_bps"],
        name="LDO Rewards (bps)",
        line_color="rgb(255,127,115)",
    )
)
fig1.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_bps"],
        name="Total Rewards (bps)",
        line_color="rgb(86,203,167)",
    )
)
fig1.update_layout(
    title="Rewards (bps)",
    xaxis_title="ETH Yield (%)",
    yaxis_title="bps",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_bps"],
        name="Total Rewards (bps)",
        line_color="rgb(86,203,167)",
    )
)
fig2.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_usd12_bps"],
        name="Total Rewards in 12mos (bps)",
        line_color="rgb(255,227,53)",
    )
)
fig2.update_layout(
    title="Rewards Today vs 12mos (bps)",
    xaxis_title="ETH Yield (%)",
    yaxis_title="bps",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.subheader("Rewards (bps)")

st.plotly_chart(fig1)
st.plotly_chart(fig2)


st.subheader("Rewards (abs)")

fig3 = go.Figure()
fig3.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_cash"],
        name="Cash Rewards (bps)",
        line_color="rgb(3,163,255)",
    )
)
fig3.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_ldo_usd12"],
        name="LDO Rewards (bps)",
        line_color="rgb(255,127,115)",
    )
)
fig3.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_usd"],
        name="Total Rewards (bps)",
        line_color="rgb(86,203,167)",
    )
)
fig3.add_trace(
    go.Scatter(
        x=data["yield_pcg"],
        y=data["tot_usd12"],
        name="Total Rewards in 12mos (bps)",
        line_color="rgb(255,227,53)",
    )
)
fig3.update_layout(
    title="Rewards Today vs 12mos (Cash)",
    xaxis_title="ETH Yield (%)",
    yaxis_title="USD",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig3)

with st.expander("Data Table"):
    st.table(data)
