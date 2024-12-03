import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Display class and group info at the center of the dashboard
st.markdown(
    """
    <div style="text-align: center; font-size: 20px; font-weight: bold;">
        Kelas 4IFP <br>
        Kelompok 2 <br>
        Imanudin Subagja - 240434002 <br>
        Firmansyah - 240434003
    </div>
    """,
    unsafe_allow_html=True
)

# Load the data
files = {
    "2012": "realisasi-apbn-2012.xlsx",
    "2013": "realisasi-apbn-2013.xlsx",
    "2014": "realisasi-apbn-2014.xlsx",
    "2015": "realisasi-apbn-2015.xlsx",
    "2016": "realisasi-apbn-2016.xlsx"
}

# Combine data
dataframes = []
for year, file in files.items():
    try:
        df = pd.read_excel(file)
        df.columns = df.columns.str.strip()  # Clean column names
        df["Year"] = year
        dataframes.append(df)
    except Exception as e:
        st.error(f"Error loading {file}: {e}")

# Concatenate data
if dataframes:
    data = pd.concat(dataframes)
else:
    st.error("No data loaded. Please check your files.")
    st.stop()

# Optional Debugging Section
if st.sidebar.checkbox("Show Debugging Info (Column Names)", value=False):
    st.subheader("Debugging: Column Names in Dataset")
    st.write(data.columns.tolist())  # Display column names

# Updated column names based on dataset
revenue_col = "Realisasi Keuangan (Rp)"  # Replace with actual revenue column
expenditure_col = "Anggaran (Rp)"  # Replace with actual expenditure column

if revenue_col not in data.columns:
    st.error(f"The expected column '{revenue_col}' is not in the dataset.")
    st.stop()

if expenditure_col not in data.columns:
    st.error(f"The expected column '{expenditure_col}' is not in the dataset.")
    st.stop()

# Sidebar: User inputs
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + list(files.keys()))

# Filter data by selected year
if selected_year != "Semua":
    filtered_data = data[data["Year"] == selected_year]
else:
    filtered_data = data

# Layout
st.title("Dashboard Realisasi APBN")

# 1. Metrics
total_revenue = filtered_data[revenue_col].sum()
total_expenditure = filtered_data[expenditure_col].sum()
st.metric("Total Realisasi Keuangan", f"Rp {total_revenue:,.0f}")
st.metric("Total Anggaran", f"Rp {total_expenditure:,.0f}")

# 2. Line Chart: Revenue Trend
st.subheader("Tren Realisasi Keuangan per Tahun")
trend_data = data.groupby("Year").sum().reset_index()
fig, ax = plt.subplots()
ax.plot(trend_data["Year"], trend_data[revenue_col], marker="o")
ax.set_title("Tren Realisasi Keuangan")
ax.set_xlabel("Tahun")
ax.set_ylabel("Realisasi Keuangan (Rp)")
st.pyplot(fig)

# 3. Bar Chart: Expenditure Comparison
st.subheader("Perbandingan Anggaran Berdasarkan Tahun")
fig, ax = plt.subplots()
ax.bar(trend_data["Year"], trend_data[expenditure_col], color="orange")
ax.set_title("Perbandingan Anggaran")
ax.set_xlabel("Tahun")
ax.set_ylabel("Anggaran (Rp)")
st.pyplot(fig)

# 4. Pie Chart: Composition of Selected Year
if selected_year != "Semua":
    st.subheader(f"Komposisi Realisasi Keuangan dan Anggaran Tahun {selected_year}")
    pie_data = filtered_data[[revenue_col, expenditure_col]].sum()
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=["Realisasi Keuangan", "Anggaran"], autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)
else:
    st.write("Pilih tahun tertentu untuk melihat komposisi.")

# 5. Data Table
st.subheader("Tabel Data")
st.dataframe(filtered_data)

# 6. Original Data Display
if st.sidebar.checkbox("Tampilkan Data Asli"):
    st.write(data)

# 7. Slider for Revenue Filtering
st.sidebar.subheader("Filter Berdasarkan Realisasi Keuangan")
min_revenue = st.sidebar.slider(
    "Batas Minimum Realisasi Keuangan", 0, int(data[revenue_col].max()), 0
)
filtered_data = filtered_data[filtered_data[revenue_col] >= min_revenue]
st.write(f"Data setelah filter: {len(filtered_data)} baris")
st.dataframe(filtered_data)
