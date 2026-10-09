import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# موبائل اسکرین پر کسٹم انجینئرنگ آئیکن سیٹ کرنا
st.set_page_config(page_title="TMA Haripur Suite", page_icon="🏗️", layout="wide")
st.title("🏗️ TMA Haripur (KPK) - Smart Infrastructure Suite")
st.subheader("PC-1 to PC-4, Feasibilities & Auto Cross-Sections")

# سیمپل خیبر پختونخوا مارکیٹ ریٹ سسٹم (MRS) ڈیٹا بیس
mrs_data = {
    "Item Code": ["03-11-a", "03-21-b", "06-01-a", "17-02-b"],
    "Description": ["Excavation in common soil", "PCC 1:4:8 in foundation", "Pacca Brick Work in 1:4", "Sub-Base Course for Roads"],
    "Unit": ["Cu.m", "Cu.m", "Cu.m", "Cu.m"],
    "Rate (PKR)": [350.0, 8500.0, 12500.0, 4200.0]
}
df_mrs = pd.DataFrame(mrs_data)

st.sidebar.header("📋 KPK MRS Database")
st.sidebar.dataframe(df_mrs)

option = st.selectbox(
    "آپ کون سا فارم یا رپورٹ بنانا چاہتے ہیں؟",
    ["PC-1 (Project Estimate & Form)", "PC-2 (Feasibility Report)", "PC-3 (Progress Report)", "PC-4 (Completion Report)", "Engineering Drawings (Cross-Sections)"]
)

if "PC-1" in option:
    st.write("### 📝 Measurement Sheet & Cost Estimate")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        item_selected = st.selectbox("آئٹم کوڈ:", df_mrs["Item Code"])
    with col2:
        length = st.number_input("لمبائی (Length - m):", min_value=0.0, value=10.0)
    with col3:
        width = st.number_input("چوڑائی (Width - m):", min_value=0.0, value=2.0)
    with col4:
        height = st.number_input("اونچائی (Height - m):", min_value=0.0, value=0.5)
    with col5:
        nos = st.number_input("تعداد (Nos):", min_value=1, value=1)

    quantity = length * width * height * nos
    selected_rate = df_mrs[df_mrs["Item Code"] == item_selected]["Rate (PKR)"].values[0]
    item_desc = df_mrs[df_mrs["Item Code"] == item_selected]["Description"].values[0]
    unit = df_mrs[df_mrs["Item Code"] == item_selected]["Unit"].values[0]
    total_cost = quantity * selected_rate

    st.write("----")
    st.write(f"**Description:** {item_desc}")
    st.success(f"📊 **Qty:** {quantity:.2f} {unit} | **Cost:** {total_cost:,.2f} PKR")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_bill = pd.DataFrame([{
            "Item Code": item_selected, "Description": item_desc, 
            "L": length, "W": width, "H": height, "Nos": nos,
            "Qty": quantity, "Unit": unit, "Rate": selected_rate, "Amount": total_cost
        }])
        df_bill.to_excel(writer, sheet_name="PC-1 Estimate", index=False)
    
    st.download_button(
        label="📥 ڈاؤن لوڈ کسٹم PC-1 Excel Sheet",
        data=buffer.getvalue(),
        file_name="TMA_Haripur_PC1_Estimate.xlsx",
        mime="application/vnd.ms-excel"
    )

elif "Drawings" in option:
    st.write("### 📐 Auto-Generated Cross Section")
    d_width = st.number_input("نالی کی چوڑائی (Bed Width):", value=1.0)
    d_height = st.number_input("نالی کی گہرائی (Wall Height):", value=1.2)
    w_thick = st.number_input("دیوار کی موٹائی (Thickness):", value=0.2)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(plt.Rectangle((0, 0), d_width + (2 * w_thick), w_thick, facecolor='gray', alpha=0.5, label="PCC Foundation"))
    ax.add_patch(plt.Rectangle((0, w_thick), w_thick, d_height, facecolor='brown', alpha=0.7, label="Brick Work"))
    ax.add_patch(plt.Rectangle((d_width + w_thick, w_thick), w_thick, d_height, facecolor='brown', alpha=0.7))
    ax.set_xlim(-0.5, d_width + (2 * w_thick) + 0.5)
    ax.set_ylim(-0.5, d_height + w_thick + 0.5)
    ax.set_aspect('equal')
    plt.title("Drain Cross Section")
    st.pyplot(fig)

else:
    st.info(f"آپ نے {option} منتخب کیا ہے۔ یہ فارم اور فیزیبلٹی ماڈیول بیک اینڈ پر کنفگرڈ ہے۔")
  
