import streamlit as st
import pandas as pd

# 1. PAGE SETUP (Makes it look professional and wide)
st.set_page_config(page_title="CircularCycle: Selangor", page_icon="♻️", layout="wide")

# 2. THE "KNOWLEDGE GRAPH" (Our simulated database of waste and partners)
waste_data = {
    "Waste Category": ["Coffee Grounds", "Fabric Scraps", "Used Cooking Oil", "Plastic Bottles", "Cardboard", "Food Scraps"],
    "Target Industry": ["Agriculture (Mushroom Farms)", "Textile Upcycling", "Biodiesel Production", "3D Printing", "Packaging Logistics", "Composting"],
    "Local Partner (Simulated)": ["Sepang Fungi Farm", "Klang Tailor Co.", "Shah Alam Bio-Fuels", "Cyberjaya Makerspace", "Banting Logistics Hub", "KMB Green Club"],
    "CO2 Saved per kg (kg)": [1.5, 3.2, 2.8, 1.9, 0.5, 1.2],
    "Value per kg (RM)": [0.50, 1.20, 1.50, 0.80, 0.20, 0.30]
}
df = pd.DataFrame(waste_data)

# 3. HEADER SECTION
st.title("♻️ CircularCycle: B2B Waste Matchmaker")
st.markdown("### *Turning Waste into Resources in Selangor (SDG 12 & 13)*")
st.write("This engine uses data matching to connect businesses with surplus materials to industries that need them as raw inputs.")
st.divider()

# 4. SIDEBAR (User Input)
st.sidebar.header("🏢 Vendor Registration")
st.sidebar.write("Enter your waste stream details below:")

biz_name = st.sidebar.text_input("Business Name", placeholder="e.g., Warung Pak Ali")
waste_type = st.sidebar.selectbox("Select Waste Material", df["Waste Category"])
quantity_kg = st.sidebar.number_input("Estimated Quantity (kg per week)", min_value=1, value=10, step=5)

# 5. THE MATCHING ENGINE & IMPACT CALCULATOR
if st.sidebar.button("Find Circular Match", type="primary"):
    
    # AI/Data Logic: Find the exact row in our database that matches the user's waste
    match = df[df["Waste Category"] == waste_type].iloc[0]
    
    # Calculate Impact based on user's quantity
    total_co2 = match['CO2 Saved per kg (kg)'] * quantity_kg
    total_value = match['Value per kg (RM)'] * quantity_kg
    
    st.success(f"✅ Match Found for **{biz_name if biz_name else 'your business'}**!")
    
    # Display the results in 3 clean columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Ideal Partner Industry", value=match["Target Industry"])
    with col2:
        st.metric(label="Estimated CO2 Saved/Week", value=f"{total_co2:.1f} kg")
    with col3:
        st.metric(label="Potential Value/Week", value=f"RM {total_value:.2f}")

    st.info(f"📍 **Closest Local Hub Identified:** {match['Local Partner (Simulated)']}")
    st.balloons() # A fun animation for the presentation!

# 6. DATA TRANSPARENCY (Shows the judges you understand Data Frames)
st.divider()
st.subheader("Data Overview: The Circular Ontology")
st.write("The underlying database mapping materials to upcycling pathways and impact metrics.")
st.dataframe(df, use_container_width=True)
