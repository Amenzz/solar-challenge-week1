import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from app.utils import load_country_data, compute_summary, run_anova

st.set_page_config(layout="wide")
st.title("☀️ Solar Metric Comparison Dashboard")

# Load data
data_dir = "data/cleaned"
country_data = load_country_data(data_dir)

if not country_data:
    st.error("No CSV files found. Please check your 'data/cleaned' folder.")
    st.stop()

# Combine all data
all_data = pd.concat(country_data.values(), ignore_index=True)

# 1. Boxplots for GHI, DNI, DHI
st.header("📦 Boxplots of Solar Metrics")
metrics = ['GHI', 'DNI', 'DHI']
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for i, metric in enumerate(metrics):
    sns.boxplot(data=all_data, x='Country', y=metric, ax=axs[i], palette='viridis')
    axs[i].set_title(f"{metric} by Country")
    axs[i].tick_params(axis='x', rotation=45)
st.pyplot(fig)

# 2. Summary Statistics Table
st.header("📊 Summary Table")
summary_df = compute_summary(all_data)
st.dataframe(summary_df.style.format("{:.2f}"))

# 3. Statistical Testing (ANOVA)
st.header("🧪 Statistical Testing: One-way ANOVA")
f_stat, p_value = run_anova(all_data)
st.write(f"**F-statistic:** {f_stat:.3f}, **p-value:** {p_value:.4f}")
if p_value < 0.05:
    st.success("✅ Significant differences found between countries' GHI values.")
else:
    st.warning("ℹ️ No statistically significant difference in GHI across countries.")

# 4. Key Observations
st.header("📝 Key Observations")
st.markdown("""
- 🇧🇯 **Benin** shows the highest average GHI but also exhibits the greatest variability.
- 🇸🇱 **Sierraleone** has the lowest overall solar radiation values among the three.
- 🇹🇬 **Togo** maintains a balanced GHI profile with moderate variance.
""")

# 5. Bar Chart: Average GHI
st.header("📈 Average GHI by Country")
avg_ghi = all_data.groupby("Country")["GHI"].mean().sort_values(ascending=False)
st.bar_chart(avg_ghi)
