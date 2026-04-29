import streamlit as st
import json
from classifier import classify_return

st.set_page_config(page_title="Mumzworld Return Classifier", page_icon="🛍️")

st.title("🛍️ Mumzworld Return Request Classifier")
st.markdown("Classify customer return reasons in *English & Arabic*")
st.divider()

reason = st.text_area("Enter return reason (English or Arabic):", height=100, placeholder="e.g. I want my money back, the stroller was broken")

if st.button("Classify", type="primary"):
    if reason.strip():
        with st.spinner("Classifying..."):
            result = classify_return(reason)
        
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            col1, col2 = st.columns(2)
            
            classification = result.get("classification") or "unclear"
            confidence = result.get("confidence", 0)
            
            color = {"refund": "🔴", "exchange": "🔵", "store_credit": "🟢", "escalate": "🟠"}.get(classification, "⚪")
            
            with col1:
                st.metric("Classification", f"{color} {classification.upper()}")
                st.metric("Confidence", f"{int(confidence * 100)}%")
            
            with col2:
                st.success(f"*English:* {result.get('suggested_reply_en', '')}")
                st.info(f"*Arabic:* {result.get('suggested_reply_ar', '')}")
            
            st.divider()
            st.markdown(f"*Reasoning (EN):* {result.get('reasoning_en', '')}")
            st.markdown(f"*Reasoning (AR):* {result.get('reasoning_ar', '')}")
    else:
        st.warning("Please enter a return reason!")

st.divider()
st.caption("Powered by Mumzworld AI | Built with OpenRouter + Nemotron")