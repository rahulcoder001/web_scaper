import streamlit as st
from scrape import scrape_website
from ai_analysis import analyze_text
from report_generator import generate_report

st.title("🤖 AI Web Scraper Pro")

url = st.text_input("Enter a website URL:")

if st.button("Scrape and Analyze"):
    st.write("🔍 Scraping and analyzing...")

    # Scrape website
    data = scrape_website(url)
    
    # Handle scraping errors
    if 'error' in data:
        st.error(f"❌ Scraping failed: {data['error']}")
        st.stop()
    
    # Prepare text for analysis
    full_text = " ".join(data['paragraphs']).strip() if data['paragraphs'] else ""
    
    # Display extracted content
    with st.expander("📄 Page Information"):
        st.subheader("Title")
        st.write(data['title'] if data.get('title') else "No title found")
        
        if data.get('metadata'):
            st.subheader("Metadata")
            st.json(data['metadata'])
        
        if data.get('accessibility'):
            st.subheader("Accessibility Info")
            st.write(f"Images with alt text: {data['accessibility']['alt_tags']}/{data['accessibility']['total_images']}")
            st.write(f"ARIA roles found: {data['accessibility']['aria_roles']}")

    with st.expander("📑 Content Structure"):
        st.subheader("Headings")
        st.write(data['headings'] if data.get('headings') else "No headings found")
        
        st.subheader("Paragraphs (first 5)")
        st.write(data['paragraphs'][:5] if data.get('paragraphs') else "No paragraphs found")
        
        st.subheader("Tables")
        if data.get('tables'):
            st.write(f"Found {len(data['tables'])} tables")
            for i, table in enumerate(data['tables'][:2], 1):
                st.markdown(f"**Table {i}:**")
                st.markdown(table, unsafe_allow_html=True)
        else:
            st.write("No tables found")
            
        st.subheader("Links (first 5)")
        st.write(data['links'][:5] if data.get('links') else "No links found")

    # AI Analysis
    if full_text:
        analysis = analyze_text(full_text)
    else:
        st.warning("⚠️ No text content found for analysis")
        analysis = {
            "summary": "No content available",
            "sentiment": {"label": "NEUTRAL", "score": 1.0},
            "topics": ["No topics available"],
            "keyword_density": {},
            "classification": {"labels": ["N/A"], "scores": [0.0]}
        }

    # Display AI Analysis
    with st.expander("🧠 AI Analysis"):
        st.subheader("Summary")
        st.write(analysis['summary'])
        
        st.subheader("Sentiment")
        sentiment = analysis['sentiment']
        st.write(f"**Label:** {sentiment['label']}, **Confidence:** {round(sentiment['score'], 2)}")
        
        st.subheader("📊 Keyword Density")
        if analysis['keyword_density']:
            st.bar_chart(analysis['keyword_density'])
        else:
            st.write("No keywords available")
        
        st.subheader("🧩 Detected Topics")
        for topic in analysis['topics']:
            st.write(f"- {topic}")
        
        st.subheader("📌 Content Classification")
        classification = analysis['classification']
        st.write(f"This content is most likely about: {classification['labels'][0]} (Confidence: {classification['scores'][0]:.2f})")

    # PDF Report Generation
    try:
        pdf_report = generate_report(data, analysis, url)
        st.download_button(
            label="📥 Download Full Report",
            data=pdf_report,
            file_name="ai_analysis_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Failed to generate report: {str(e)}")