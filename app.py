import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="SWCA APP Master List", layout="wide")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a5f,#2563eb);padding:20px 24px;border-radius:10px;margin-bottom:20px'>
        <p style='color:rgba(255,255,255,0.7);font-size:12px;letter-spacing:2px;margin:0'>SPINE & WELLNESS CENTERS OF AMERICA</p>
        <h1 style='color:white;margin:4px 0 0;font-size:24px'>APP Monthly Master List</h1>
        <p style='color:rgba(255,255,255,0.7);font-size:13px;margin:4px 0 0'>Billing Reconciliation & Compensation Tracker</p>
    </div>
""", unsafe_allow_html=True)

# ── APP Data ──────────────────────────────────────────────────────────────────
apps = [
    ("Rasa Guzeviciene", "FT/Salary"), ("Catalina Galvis", "FT/Salary"),
    ("Beatriz Ojeda", "FT/Salary"), ("Fritz Luma", "Per Diem"),
    ("Andres Alava", "FT/Salary"), ("Jany Vazquez", "FT/Salary"),
    ("Karla Torres", "Per Diem"), ("Jincy Chacko", "FT/Salary"),
    ("Reinaldo Rosales", "FT/Salary"), ("Anam Qureshi", "FT/Salary"),
    ("Showrab Guha", "Per Diem"), ("Chenelle Stanford", "Per Diem"),
    ("Stephanie Landa", "FT/Salary"), ("Bethany Vigroux", "Per Diem"),
    ("Yorka Hernandez", "Per Diem"), ("Virginia Lombardo", "FT/Salary"),
    ("Ernesto Diaz", "Per Diem"), ("Janette Rodriguez", "Per Diem"),
    ("Yesenia Franqui", "FT/Salary"), ("Aida Acuna", "Per Diem"),
    ("Elena Bogatova", "FT/Salary"), ("Lorenza Mattelus", "Per Diem"),
    ("Emma Gustave", "Per Diem"), ("Sandra Segura", "FT/Salary"),
    ("Stephanie Lerner", "PT/Salary"), ("Syddonie Vassell", "FT/Salary"),
    ("Stephanie Chery", "FT/Salary"), ("Orlando Gil", "Per Diem"),
    ("Randi Futterman", "Per Diem"), ("Slavik Shusterman", "Per Diem"),
    ("Beatriz Cruz", "Per Diem"), ("Kalima Ascanio", "Per Diem"),
    ("Rahman Shtomiwa", "Per Diem"), ("James Celestine", "Per Diem"),
    ("Natalie Alanez", "PT/Salary"), ("Dr. Bristow", "FT/Salary"),
    ("Miguel Martinez", "FT/Salary"),
]

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

# ── Sidebar Controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    selected_month = st.selectbox("Select Month", MONTHS, index=0)
    selected_year  = st.selectbox("Select Year", [2025, 2026, 2027], index=1)
    filter_type    = st.selectbox("Filter by Type", ["All", "FT/Salary", "Per Diem", "PT/Salary"])
    search         = st.text_input("Search APP Name")

    st.markdown("---")
    st.markdown("### 🗂 Column Ownership")
    st.markdown("🔵 **Maria / You** — Dates, Facility, Volume, Dropbox")
    st.markdown("🟣 **Carmen** — Compensation Paid")
    st.markdown("🟢 **Ronatta** — Reimbursement & Status")
    st.markdown("🟡 **All** — Notes")

# ── Build Base DataFrame ──────────────────────────────────────────────────────
df = pd.DataFrame(apps, columns=["APP Name", "Employment Type"])

if filter_type != "All":
    df = df[df["Employment Type"] == filter_type]
if search:
    df = df[df["APP Name"].str.contains(search, case=False)]

df = df.sort_values("APP Name").reset_index(drop=True)

# Add editable columns
for col in ["Date(s) of Service", "Facility Name", "Verified Patient Volume", "Dropbox Verified (Y/N)"]:
    df[col] = ""
for col in ["Compensation Paid ($)"]:
    df[col] = ""
for col in ["Reimbursement Received ($)", "Reimbursement Status"]:
    df[col] = ""
df["Notes"] = ""

# ── Summary Metrics ───────────────────────────────────────────────────────────
all_df = pd.DataFrame(apps, columns=["APP Name", "Employment Type"])
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total APPs", len(all_df))
c2.metric("FT/Salary",  len(all_df[all_df["Employment Type"]=="FT/Salary"]))
c3.metric("Per Diem",   len(all_df[all_df["Employment Type"]=="Per Diem"]))
c4.metric("PT/Salary",  len(all_df[all_df["Employment Type"]=="PT/Salary"]))

st.markdown(f"### 📋 {selected_month} {selected_year} — Master List")
st.caption(f"Showing {len(df)} of {len(all_df)} APPs")

# ── Editable Table ────────────────────────────────────────────────────────────
edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "APP Name":                  st.column_config.TextColumn("APP Name", disabled=True, width="medium"),
        "Employment Type":           st.column_config.TextColumn("Employment Type", disabled=True, width="small"),
        "Date(s) of Service":        st.column_config.TextColumn("📅 Date(s) of Service [Maria/You]", width="medium"),
        "Facility Name":             st.column_config.TextColumn("🏥 Facility Name [Maria/You]", width="medium"),
        "Verified Patient Volume":   st.column_config.NumberColumn("👥 Patient Volume [Maria/You]", width="small"),
        "Dropbox Verified (Y/N)":    st.column_config.SelectboxColumn("☁️ Dropbox ✓ [Maria/You]", options=["Y","N","Pending"], width="small"),
        "Compensation Paid ($)":     st.column_config.NumberColumn("💵 Compensation $ [Carmen]", format="$%.2f", width="small"),
        "Reimbursement Received ($)":st.column_config.NumberColumn("💰 Reimbursement $ [Ronatta]", format="$%.2f", width="small"),
        "Reimbursement Status":      st.column_config.SelectboxColumn("📊 Status [Ronatta]", options=["Pending","Partial","Reimbursed","Denied"], width="small"),
        "Notes":                     st.column_config.TextColumn("📝 Notes [All]", width="large"),
    },
    num_rows="fixed",
)

# ── Export to Excel ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### ⬇️ Export")

def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=f"{selected_month} {selected_year}")
    return output.getvalue()

excel_data = to_excel(edited_df)
st.download_button(
    label=f"⬇️ Download {selected_month} {selected_year} Master List (.xlsx)",
    data=excel_data,
    file_name=f"SWCA_MasterList_{selected_month}_{selected_year}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
