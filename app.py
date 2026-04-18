import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. PAGE SETUP (Must be the first command)
st.set_page_config(page_title="CircularCycle: Selangor", page_icon="♻️", layout="wide")

# 2. INITIALIZE DATABASE (Session State so data doesn't disappear)
if 'user_db' not in st.session_state:
    # Starting with some fake data so the table isn't empty for your presentation!
    st.session_state.user_db = pd.DataFrame({
        "Business Name": ["Banting Cafe", "Klang Tailor"],
        "Waste Material": ["Coffee Grounds", "Fabric Scraps"],
        "Quantity (kg)": [15, 40],
        "Status": ["Matched", "Pending"]
    })

# 3. KNOWLEDGE GRAPH (The Logic Engine)
waste_logic = {
    "Waste Category": ["Coffee Grounds", "Fabric Scraps", "Used Cooking Oil", "Plastic Bottles", "Cardboard"],
    "Target Industry": ["Mushroom Farms", "Textile Upcycling", "Biodiesel", "3D Printing", "Logistics Hub"],
    "CO2 Saved per kg (kg)": [1.5, 3.2, 2.8, 1.9, 0.5],
    "Value per kg (RM)": [0.50, 1.20, 1.50, 0.80, 0.20]
}
logic_df = pd.DataFrame(waste_logic)

# 4. HEADER
st.title("♻️ CircularCycle: B2B Waste Matchmaker")
st.markdown("### *A Closed-Loop Supply Chain for Kuala Langat (SDG 12)*")
st.divider()

# 5. SIDEBAR (User Input & Upload)
st.sidebar.header("🏢 Add Your Waste")
biz_name = st.sidebar.text_input("Business Name", placeholder="e.g., Warung Pak Ali")
waste_type = st.sidebar.selectbox("Select Material", logic_df["Waste Category"])
quantity_kg = st.sidebar.number_input("Quantity (kg/week)", min_value=1, value=10)

st.sidebar.divider()
st.sidebar.subheader("📸 Proof of Condition")
uploaded_photo = st.sidebar.file_uploader("Upload photo of waste", type=["jpg", "png"])

if st.sidebar.button("Add to Circular Network", type="primary"):
    if biz_name: # Make sure they typed a name
        new_entry = pd.DataFrame({
            "Business Name": [biz_name],
            "Waste Material": [waste_type],
            "Quantity (kg)": [quantity_kg],
            "Status": ["Searching..."]
        })
        st.session_state.user_db = pd.concat([st.session_state.user_db, new_entry], ignore_index=True)
        st.sidebar.success("Added successfully!")
        st.balloons()
    else:
        st.sidebar.error("Please enter a business name first.")

# 6. MAIN CONTENT (Using Tabs for a clean UI)
tab1, tab2, tab3 = st.tabs(["🛒 Marketplace & Database", "🗺️ Selangor Impact Map", "📈 CDO Analytics Dashboard"])

with tab1:
    st.subheader("Live Community Database")
    st.write("Businesses currently looking for circular partners:")
    # Display the live database
    st.dataframe(st.session_state.user_db, use_container_width=True)
    
    st.divider()
    st.subheader("Latest Match Simulation")
    # Simulate a match based on what is currently selected in the sidebar
    match = logic_df[logic_df["Waste Category"] == waste_type].iloc[0]
    total_co2 = match['CO2 Saved per kg (kg)'] * quantity_kg
    total_rm = match['Value per kg (RM)'] * quantity_kg
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ideal Partner Industry", match["Target Industry"])
    col2.metric("CO2 Saved", f"{total_co2:.1f} kg")
    col3.metric("New Revenue", f"RM {total_rm:.2f}")
    
    if uploaded_photo:
        st.image(uploaded_photo, caption=f"Condition of {biz_name}'s {waste_type}", width=300)

with tab2:
    st.subheader("Kuala Langat Logistics Map")
    st.write("Optimizing transport routes to minimize carbon emissions (SDG 13).")
    
    # Create map centered on Banting
    m = folium.Map(location=[2.81, 101.50], zoom_start=12)
    
    # Add fake data points for the presentation
    folium.Marker([2.818, 101.492], popup="Banting Hub", icon=folium.Icon(color="green", icon="recycle")).add_to(m)
    folium.Marker([2.801, 101.520], popup="Mushroom Farm (Buyer)", icon=folium.Icon(color="blue", icon="leaf")).add_to(m)
    folium.Marker([2.830, 101.480], popup="Textile Factory (Waste)", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
    
    # Display map
    st_folium(m, width=800, height=400)

with tab3:
    st.subheader("System Value & Forecasting")
    st.write("Predictive carbon offset tracking for participating businesses.")
    
    # Simple chart data
    chart_data = pd.DataFrame({
        "Material": ["Fabric", "Used Oil", "Plastic", "Coffee", "Cardboard"],
        "Projected CO2 Offset (kg)": [450, 320, 210, 180, 90]
    }).set_index("Material")
    
    st.bar_chart(chart_data, color="#2ecc71")
