import streamlit as st


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
st.write("Proposal:")
st.write("1. Sliding index driven by cumulative ETH staking volume over the past 12mos")
st.write(
    "2. Target cap set to 50bps for total value locked-in at inception. If staking yields deliver > 50bps of referral bonus, no LDO is paid out. If staking yields deliver < 50bps of referral bonus, difference is paid out in LDO at spot price"
)
st.write(
    "3. LDO tokens are streamed via smart contract with a 12mo vesting cliff. Total value of each referral can be multiples in excess of 50bps if LDO appreciates"
)
st.subheader("1: Input desired values for each of the parameters")

eth_price = st.slider("ETH Price in USD", min_value=0.0, max_value=5000.0, value=1300.0)
ldo_price = st.slider(
    "LDO Lock-in Price in USD", min_value=0.0, max_value=20.0, value=1.30
)

eth_staking = st.slider(
    "ETH Staking Yield (%)", min_value=0.0, max_value=10.0, value=5.0
)
idx_take = st.slider("Referral Value Index", min_value=1.0, max_value=2.0, value=1.5)
eth_referred = st.number_input("ETH Referred", min_value=0.0, format="%.2f", value=1.0)
ldo_take = 5.0

led_bps = eth_staking * ldo_take * idx_take
led_usd = led_bps / 10000 * eth_referred * eth_price


st.subheader("2: Input amount of ETH referred")

st.write("Pure cash compensation:")
ans1, ans2 = st.columns(2)
ans1.metric("Referral bonus (bps)", value=f"{led_bps:.1f}")
ans2.metric("Referral bonus (USD)", value=f"{led_usd:.2f}")

st.subheader("3: LDO tokens to reach cap")
led_cap = st.slider(
    "Value cap (bps) at inception", min_value=0.0, max_value=50.0, value=50.0
)

ldo_tokes = max((led_cap - led_bps) / 10000 * eth_referred * eth_price / ldo_price, 0)
ldo_value = ldo_tokes * ldo_price
new_bps = (ldo_value + led_usd) / (eth_referred * eth_price) * 10000
bps_delta = max(new_bps - led_bps, 0)
total_usd = led_usd + ldo_value
delta_usd = total_usd - led_usd

ldo1, ldo2 = st.columns(2)
ldo1.metric("LDO tokens locked (12mos)", value=f"{ldo_tokes:.2f}")
ldo2.metric("LDO value locked (12mos)", value=f"{ldo_value:.2f}")

st.subheader("4: Total referral bonus at inception")
ldo3, ldo4 = st.columns(2)
ldo3.metric(
    "Total referral bonus (bps)", value=f"{new_bps:.1f}", delta=f"{bps_delta:.2f}"
)
ldo4.metric(
    "Total referral bonus (USD)", value=f"{total_usd:.2f}", delta=f"{delta_usd:.2f}"
)

st.subheader("5: Total referral bonus in 12mos")
new_ldo_price = st.slider(
    "LDO Price in 12mos", min_value=0.0, max_value=100.0, value=1.30
)

new_ldo_value = ldo_tokes * new_ldo_price
new_ldo_bps = (new_ldo_value + led_usd) / (eth_referred * eth_price) * 10000
new_ref_value = new_ldo_value + led_usd

delta_new_bps = new_ldo_bps - new_bps
delta_new_value = new_ref_value - total_usd

ldo5 = st.metric("Value of LDO tokens (in 12mos)", value=f"{new_ldo_value:.2f}")

ldo6, ldo7 = st.columns(2)
ldo6.metric(
    "Total referral bonus (bps)",
    value=f"{new_ldo_bps:.2f}",
    delta=f"{delta_new_bps:.2f}",
)
ldo7.metric(
    "Total referral bonus (USD)",
    value=f"{new_ref_value:.2f}",
    delta=f"{delta_new_value:.2f}",
)
