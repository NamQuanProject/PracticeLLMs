from day5 import *

def main():
    """Streamlit Application"""

    # Page Configuration
    st.set_page_config(
        page_title="\U0001F310 Company Brochure Generator",
        page_icon="\U0001F680",
        layout="wide"
    )

    # Custom CSS for extra style
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Google Sans', sans-serif;
    }
    .big-font {
        font-size: 300%;
        font-weight: bold;
        color: #2C3E50;
    }
    .sub-font {
        font-size: 150%;
        color: #34495E;
    }
    </style>
    """, unsafe_allow_html=True)

    # Decorative Header
    st.markdown('<p class="big-font">\U0001F310 Company Brochure Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-font">Transform Websites into Compelling Narratives</p>', unsafe_allow_html=True)

    # Decorative Separator
    st.markdown("---")

    # Input Columns for Better Layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### \U0001F511 API Configuration")
        # Input API Key
        user_provided_key = st.text_input(
            "OpenAI API Key", 
            type="password", 
            placeholder="Enter your OpenAI API Key"
        )

    with col2:
        st.markdown("#### \U0001F3E2 Company Details")
        company_name = st.text_input(
            "Company Name", 
            placeholder="e.g., HuggingFace"
        )
        url = st.text_input(
            "Website URL", 
            placeholder="e.g., huggingface.co"
        )

    # Decorative Separator
    st.markdown("---")

    # Generate Button
    if st.button("\u2728 Generate Magical Brochure \u2728", type="primary"):
        # Validate Inputs
        if not (user_provided_key and company_name and url):
            st.error("\u26A0 Please fill all fields!")
            return

        try:
            # Spinner with Creative Message
            with st.spinner("\u2728 Crafting Your Brochure... (Brewing Innovation)"):
                generator = BrochureGenerator(user_provided_key)
                brochure = generator.create_brochure(company_name, url)

            # Brochure Display
            st.success("\U0001F389 Brochure Generated Successfully!")
            st.markdown("## \U0001F4C4 Your Sparkling Brochure")
            st.markdown(brochure)

            # Download Option
            st.download_button(
                label="\U0001F4BE Download Brochure",
                data=brochure,
                file_name=f"{company_name}_Brochure.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"\U0001F916 Oops! {e}")

    # Fun Footer
    st.markdown("---")
    st.markdown("\U0001F680 **Powered by AI Magic** | Transform Websites into Stories")

if __name__ == "__main__":
    main()
