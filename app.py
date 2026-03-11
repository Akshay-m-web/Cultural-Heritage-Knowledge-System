import streamlit as st
import engine

st.set_page_config(page_title="Heritage AI", layout="wide")

st.title("🏛️ Cultural Heritage Knowledge System")
st.markdown("---")

try:
    # Get monument list for the dropdown
    _, monuments_data = engine.load_and_query("", "")
    
    if not monuments_data:
        st.error("Error: Please make sure 'data.json' is in the folder.")
    else:
        mon_names = {m['name']: m['id'] for m in monuments_data}

        # Sidebar Search logic
        st.sidebar.header("🔍 Search Filters")
        search_state = st.sidebar.text_input("Find by State", placeholder="e.g. Maharashtra")
        if search_state:
            recs = engine.get_recommendations(search_state)
            if recs:
                st.sidebar.success(f"Sites: {', '.join(recs)}")
            else:
                st.sidebar.warning("No sites found.")

        # Main Layout
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🤖 AI Logic Engine")
            choice = st.selectbox("Choose a Monument", list(mon_names.keys()))
            m_id = mon_names[choice]
            
            query_task = st.radio("Select a Logic Rule to Test:", 
                                 ["Can I take photos?", "Is it a UNESCO site?"])
            
            if st.button("Inference Result"):
                rule_type = "photo" if "photo" in query_task.lower() else "unesco"
                
                # Execute the reasoning engine
                logic_result, _ = engine.load_and_query(m_id, rule_type)
                
                if logic_result:
                    st.success(f"✅ The system inferred: YES for {choice}")
                else:
                    st.error(f"❌ The system inferred: NO for {choice}")

        with col2:
            st.subheader("📂 Knowledge Base (JSON)")
            current_data = next(m for m in monuments_data if m['id'] == m_id)
            st.info("The logic engine reasons over the following structured facts:")
            st.json(current_data)

except Exception as e:
    st.error(f"An error occurred: {e}")