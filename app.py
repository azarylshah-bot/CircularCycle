import streamlit as st
import pandas as pd
from supabase import create_client, Client
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(page_title="CircularCycle Enterprise", page_icon="♻️", layout="wide")

# 2. SECURE DATABASE CONNECTION (Connects to your Supabase SQL)
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# 3. DATA FETCHING (Pulls real data from your SQL table)
def load_data():
    # This pulls everything from the 'supply' table you built in Supabase
    response = supabase.table("supply").select("*").execute()
    df = pd.DataFrame(response.data)
    return df

# 4. SIDEBAR - DATA ENTRY (Writes to your SQL database)
st.sidebar.header("🏢 Post Industrial Waste")
with st.sidebar.form("waste_form"):
    new_biz = st.text_input("Business Name")
    new_mat = st.selectbox("Material Type", ["Coffee Grounds", "Fabric Scraps", "Used Oil", "Cardboard", "Organic Waste"])
    new_qty = st.number_input("Quantity (kg)", min_value=1, value=50)
    
    submitted = st.form_submit_button("Publish to Network", type="primary")
    if submitted:
        if new_biz:
            # Insert the new data into Supabase
            supabase.table("supply").insert({
                "business_name": new_biz,
                "material_type": new_mat,
                "quantity_kg": new_qty,
                "status": "Available"
            }).execute()
            st.success("Successfully posted to the live network!")
            st.rerun() # Refreshes the page to show new data
        else:
            st.error("Please enter a business name.")

# 5. FETCH LIVE DATA FOR THE APP
df = load_data()

# 6. APP NAVIGATION (The Pro Dashboard Layout)
st.title("♻️ CircularCycle: Kuala Langat Node")
tab1, tab2, tab3 = st.tabs(["🛒 Live Marketplace", "🗺️ Logistics Map", "📈 CDO Analytics"])

# --- TAB 1: THE BEAUTIFUL UI CARDS ---
with tab1:
    st.markdown("**🔍 Filter Live Resources**")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    # Dynamic filters
    all_materials = ["All Materials"] + (df['material_type'].unique().tolist() if not df.empty else [])
    mat_filter = f_col1.selectbox("Material Filter", all_materials)
    
    # Filter the dataframe based on selection
    if mat_filter != "All Materials":
        display_df = df[df["material_type"] == mat_filter]
    else:
        display_df = df

    st.divider()

    # Create the floating cards if data exists
    if not display_df.empty:
        cols = st.columns(3)
        for index, row in display_df.reset_index().iterrows():
            col = cols[index % 3]
            with col:
                with st.container(border=True):
                    st.markdown(f"### {row['material_type']}")
                    st.caption(f"🏢 {row['business_name']}")
                    st.write(f"**⚖️ Quantity:** {row['quantity_kg']} kg")
                    st.write(f"**🌱 CO2 Offset Potential:** {(row['quantity_kg'] * 1.5):.1f} kg")
                    st.write(f"**🕒 Posted:** {str(row['created_at'])[:10]}")
                    
                    st.button("🤝 Claim Resource", key=f"claim_{row['id']}", type="primary", use_container_width=True)
    else:
        st.info("No resources available for this filter yet. Use the sidebar to add some!")

# --- TAB 2: INTERACTIVE GEOSPATIAL MAP ---
with tab2:
    st.subheader("Geospatial Resource Mapping")
    st.write("Visualizing supply hubs to optimize collection routes (SDG 13).")
    
    # Base map of Banting
    m = folium.Map(location=[2.81, 101.50], zoom_start=12)
    
    # In a real app, you would save latitudes in SQL. For now, we simulate map pins based on your database count!
    locations = [[2.818, 101.492], [2.801, 101.520], [2.830, 101.480], [2.790, 101.510], [2.825, 101.495]]
    
    if not df.empty:
        for i, row in df.iterrows():
            # Assign a random Banting location to each real database entry for the prototype
            loc = locations[i % len(locations)]
            folium.Marker(
                loc, 
                popup=f"{row['business_name']}: {row['quantity_kg']}kg of {row['material_type']}", 
                icon=folium.Icon(color="green" if row['status'] == "Available" else "red")
            ).add_to(m)
            
    st_folium(m, width=800, height=400)

# --- TAB 3: POWER BI-STYLE ANALYTICS (Plotly) ---
with tab3:
    st.subheader("District Waste Intelligence")
    
    if not df.empty:
        colA, colB = st.columns(2)
        
        with colA:
            # Group data by material type
            pie_data = df.groupby('material_type')['quantity_kg'].sum().reset_index()
            # Professional Plotly Donut Chart
            fig1 = px.pie(pie_data, values='quantity_kg', names='material_type', hole=0.4, title="Total Supply by Material")
            st.plotly_chart(fig1, use_container_width=True)
            
        with colB:
            # Calculate metrics
            total_kg = df['quantity_kg'].sum()
            total_co2 = total_kg * 1.5 # Simulated CO2 math
            
            with st.container(border=True):
                st.metric("Total Network Volume", f"{total_kg} kg")
            with st.container(border=True):
                st.metric("Projected CO2 Offset", f"{total_co2} kg", delta="SDG 13 Impact")
    else:
        st.warning("Not enough data to generate analytics. Add items in the sidebar.")
