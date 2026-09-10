
import os
import streamlit as st
from dotenv import load_dotenv

from app.pdf_processor import extract_text_from_pdf
from app.rag_engine import (
    create_vectorstore,
    create_vectorstore_from_pages,
    get_relevant_context
)
from app.gemini_client import generate_answer_stream  
from app.report_generator import generate_report

# --------------------------------------------------
# ENVIRONMENT AND CONFIGURATION
# --------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file.")
    st.stop()

st.set_page_config(
    page_title="PharmaGen AI Copilot",
    page_icon="💊",
    layout="wide"
)

# --------------------------------------------------
# 🎨 CUSTOM CSS FOR PHARMA ENTERPRISE THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
        /* ❌ जुना .stApp चा भाग बदलून हा नवीन कोड टाका: */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 50%, #F1F5F9 100%);
        background-attachment: fixed;
    }
    
    /* 📦 सायडबारचा बॅकग्राउंड सुद्धा मॅचिंग करण्यासाठी (Optional पण भारी लुक देईल) */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0;
    }

    
    /* Executive Header Alignment */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        background-color: #FFFFFF;
        border-bottom: 2px solid #E2E8F0;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #0F172A; /* Deep Navy Blue */
        margin: 0;
    }
    .status-badge {
        background-color: #ECFDF5;
        color: #059669; /* Teal/Green Status */
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #A7F3D0;
    }
    .sub-title {
        font-size: 15px;
        color: #64748B;
        margin-top: -15px;
        margin-bottom: 25px;
        padding-left: 5px;
    }
    
    /* Section and Card Layouts */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 20px;
        padding-bottom: 8px;
        border-bottom: 2px solid #0D9488; /* Teal Accent */
    }
    .pharma-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    /* RAG Architectural Flow Chart CSS */
    .flow-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 25px;
        padding: 20px;
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
    .flow-node {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 12px 35px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
        min-width: 250px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .flow-arrow {
        color: #0D9488;
        font-size: 24px;
        font-weight: bold;
        margin: 8px 0;
    }
    .flow-node-active {
        background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
        border: 2px solid #059669;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HEADER CONTAINER WITH STATUS INDICATOR
# --------------------------------------------------
st.markdown(
    """
    <div class="header-container">
        <div class="main-title">💊 PharmaGen AI Copilot</div>
        <div class="status-badge">● Online</div>
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown('<div class="sub-title">Enterprise AI-assisted document intelligence and investigation support for pharmaceutical manufacturing</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE STORAGE
# --------------------------------------------------
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "investigation_history" not in st.session_state:
    st.session_state.investigation_history = []

# --------------------------------------------------
# SIDEBAR NAVIGATION (Professional & Minimalist)
# --------------------------------------------------
st.sidebar.markdown("### 🏢 Industrial Engine")
st.sidebar.info("Quality Assurance & Investigation Support System.")

page = st.sidebar.radio(
    "Navigation System",
    [
        "Dashboard",
        "Documents",
        "AI Copilot",
        "Reports",
    ],
)

# ==================================================
# 📊 DASHBOARD PAGE (Dynamic Dynamic Time Greeting Fix)
# ==================================================
if page == "Dashboard":
    st.markdown('<div class="section-title">📊 Executive Dashboard</div>', unsafe_allow_html=True)
    
    # 🎯 कॉम्प्युटरची सध्याची वेळ मिळवून डायनॅमिक ग्रीटिंग तयार करणे
    from datetime import datetime
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        greeting = "Good Morning 🌅"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon ☀️"
    elif 17 <= current_hour < 21:
        greeting = "Good Evening 🌆"
    else:
        greeting = "Good Night 🌙"
        
    # 🏢 इंजिनिअरला वेळेनुसार अचूक विश दाखवणे
    st.markdown(f"### {greeting}, Engineer 👋")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documents Processed", f"{len(st.session_state.processed_files)}")
    with col2:
        st.metric("RAG Database Status", "Active" if st.session_state.vectorstore else "Inactive")
    with col3:
        st.metric("AI Core (Gemini)", "Ready")

    st.markdown('<div class="pharma-card">', unsafe_allow_html=True)
    st.info(
        "**PharmaGen AI Copilot** is a practical academic prototype tailored for pharmaceutical manufacturing. "
        "It securely retrieves relevant context from engineering logs, deviations, and SOP batch records to assist "
        "investigators in diagnosing process deviations and establishing corrective and preventive actions (CAPA)."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.processed_files:
        st.markdown('<div class="pharma-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Recent Processed Documents")
        for idx, f_name in enumerate(st.session_state.processed_files, 1):
            st.markdown(f"**{idx}.** 📄 `{f_name}`")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# 📄 DOCUMENTS PROCESSING PAGE (With Architectural Flow)
# ==================================================
elif page == "Documents":

    st.markdown(
        '<div class="section-title">📄 Document Management & RAG pipeline</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="pharma-card">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # PDF UPLOADER
    # --------------------------------------------------

    uploaded_files = st.file_uploader(
        "Upload Pharmaceutical PDF Documents (SOPs, Deviation Records, Batch Logs)",
        type=["pdf"],
        accept_multiple_files=True
    )

    # --------------------------------------------------
    # PROCESS DOCUMENTS
    # --------------------------------------------------

    if uploaded_files:

        if st.button("🚀 Process All Documents"):

            with st.spinner(
                "Executing secure extraction and text chunking..."
            ):

                try:

                    all_pages = []
                    processed_names = []

                    # ------------------------------------------
                    # Extract every uploaded PDF page-by-page
                    # ------------------------------------------

                    for uploaded_file in uploaded_files:

                        processed_names.append(
                            uploaded_file.name
                        )

                        from pypdf import PdfReader

                        try:

                            reader = PdfReader(
                                uploaded_file
                            )

                            for page_number, page_data in enumerate(
                                reader.pages,
                                start=1
                            ):

                                text = page_data.extract_text()

                                if text and text.strip():

                                    all_pages.append(
                                        {
                                            "source": uploaded_file.name,
                                            "page": page_number,
                                            "text": text.strip()
                                        }
                                    )

                        except Exception as pdf_err:

                            st.error(
                                f"Error reading {uploaded_file.name}: {pdf_err}"
                            )

                    # ------------------------------------------
                    # Create FAISS Vector Store
                    # ------------------------------------------

                    if all_pages:

                        # Combined text for compatibility
                        combined_text = "\n\n".join(
                            page["text"]
                            for page in all_pages
                        ).strip()

                        st.session_state.document_text = (
                            combined_text
                        )

                        # Page-aware FAISS vector store
                        st.session_state.vectorstore = (
                            create_vectorstore_from_pages(
                                all_pages
                            )
                        )

                        st.session_state.processed_files = (
                            processed_names
                        )

                        st.session_state.documents_processed = (
                            True
                        )

                        st.success(
                            f"✅ {len(processed_names)} document(s) processed successfully!"
                        )

                        st.info(
                            f"📚 {len(all_pages)} PDF page(s) indexed with source and page metadata."
                        )

                    else:

                        st.error(
                            "❌ No readable text was found in the uploaded PDFs."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Document processing failed: {str(e)}"
                    )

    # --------------------------------------------------
    # CLOSE PHARMA CARD
    # --------------------------------------------------

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

     # ==================================================
# 📄 DOCUMENTS PROCESSING PAGE (With Architectural Flow)
# ==================================================
elif page == "Documents":
    st.markdown('<div class="section-title">📄 Document Management & RAG pipeline</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="pharma-card">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload Pharmaceutical PDF Documents (SOPs, Deviation Records, Batch Logs)", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("🚀 Process All Documents"):
            with st.spinner("Executing secure extraction and text chunking..."):
                try:
                    combined_text_list = []
                    processed_names = []
                    
                    for uploaded_file in uploaded_files:
                        processed_names.append(uploaded_file.name)
                        
                        from pypdf import PdfReader
                        try:
                            reader = PdfReader(uploaded_file)
                            for page_data in reader.pages:
                                text = page_data.extract_text()
                                if text:
                                    combined_text_list.append(text)
                        except Exception as pdf_err:
                            st.error(f"Error reading {uploaded_file.name}: {pdf_err}")
                    
                    if combined_text_list:
                        combined_text = "\n\n".join(combined_text_list).strip()
                        st.session_state.document_text = combined_text  
                        
                        st.session_state.vectorstore = create_vectorstore(combined_text)
                        st.session_state.processed_files = processed_names
                        st.session_state.documents_processed = True
                        
                        st.success(f"🎉 Successfully ingested and indexing {len(processed_names)} technical records!")
                    else:
                        st.error("Text extraction yielded empty outputs from the uploaded PDFs.")
                        
                except Exception as e:
                    st.error(f"Data-pipeline disruption: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 🎯 PARTNER'S STRONGEST RECOMMENDATION: VISUAL RAG FLOW CHART
    st.markdown("### ⚙️ Internal RAG Dataflow Process")
    ready_class = "flow-node-active" if st.session_state.vectorstore else ""
    
    flow_html = f"""
    <div class="flow-wrapper">
        <div class="flow-node">📄 1. Upload PDF Records</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-node">🔍 2. Extract Plain Text (pyPDF)</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-node">✂️ 3. Recursive Text Chunking</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-node">🧠 4. Generate Embeddings</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-node">🗄️ 5. Indexing via FAISS VectorStore</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-node {ready_class}">✅ 6. Pipeline Ready for AI Inquiry</div>
    </div>
    """
    st.markdown(flow_html, unsafe_allow_html=True)


# ==================================================
# 🤖 AI COPILOT
# ==================================================

elif page == "AI Copilot":

    st.markdown(
        '<div class="section-title">🤖 AI Investigation Copilot</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Ask technical questions regarding batch records, deviations, and root causes."
    )

    current_lang = "English"

    st.markdown(
        '<div class="pharma-card">',
        unsafe_allow_html=True
    )

    if not st.session_state.vectorstore:

        st.warning(
            "No operational database detected. "
            "Please upload and index documents first."
        )

        current_lang = st.selectbox(
            "🌐 Select Response Language / भाषा निवडा:",
            ["English", "Marathi", "Hindi"],
            key="lang_fallback"
        )

    else:

        source_display = ", ".join(
            st.session_state.processed_files
        )

        st.success(
            f"🔒 Secure Context Database Enabled: {source_display}"
        )

        current_lang = st.selectbox(
            "🌐 Select Response Language / भाषा निवडा:",
            ["English", "Marathi", "Hindi"],
            key="lang_active"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if st.session_state.investigation_history:

        st.markdown(
            '<div class="pharma-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "#### 💬 Investigation Log / चॅट इतिहास"
        )

        for chat in st.session_state.investigation_history:

            with st.chat_message("user"):
                st.write(chat["query"])

            with st.chat_message("assistant"):
                st.markdown(chat["answer"])

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    query = st.chat_input(
        "Enter system audit query or deviation tracking..."
    )

    if query:

        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):

            if not st.session_state.vectorstore:

                st.error(
                    "Operation Denied: Please go to the "
                    "'Documents' page and upload pharmaceutical PDFs first."
                )

                st.session_state.investigation_history.append({
                    "query": query,
                    "answer": "❌ No document database available.",
                    "lang": current_lang,
                    "is_valid": False
                })

            else:

                try:

                    with st.spinner(
                        "Scanning vectorized blocks for compliance data..."
                    ):

                        context = get_relevant_context(
                            st.session_state.vectorstore,
                            query
                        )

                    if not context.strip():

                        clean_text = (
                            "I don't have the answer to this question "
                            "from the uploaded PDF documents."
                        )

                        st.warning(clean_text)
                        is_valid = False

                    else:

                        clean_text = st.write_stream(
                            generate_answer_stream(
                                query,
                                context,
                                current_lang
                            )
                        )

                        if not clean_text:
                            clean_text = (
                                "I don't have the answer to this "
                                "question from the uploaded PDF."
                            )

                        if (
                            "insufficient" in clean_text.lower()
                            or "no relevant" in clean_text.lower()
                        ):

                            clean_text = (
                                "I don't have the answer to this "
                                "question from the uploaded PDF.\n\n"
                                "Please ask your next question."
                            )

                            is_valid = False

                        else:

                            is_valid = True

                    st.session_state.investigation_history.append({
                        "query": query,
                        "answer": clean_text,
                        "lang": current_lang,
                        "is_valid": is_valid
                    })

                    st.rerun()

                except Exception:

                    st.error(
                        "Gemini core connection fault. "
                        "Please verify your API configuration."
                    )

                    st.session_state.investigation_history.append({
                        "query": query,
                        "answer": "❌ System could not complete this request.",
                        "lang": current_lang,
                        "is_valid": False
                    })

                    st.rerun()
# ==================================================
# 📄 REPORTS DYNAMIC DOWNLOAD PAGE
# ==================================================
elif page == "Reports":
    st.markdown('📄 Reports / तपासणी अहवाल', unsafe_allow_html=True)
    
    # फक्त व्हॅलिड (अचूक) प्रश्न गोळा करणे
    valid_history = [
        chat for chat in st.session_state.investigation_history 
        if chat.get('is_valid', True)
    ]
    
    if not valid_history:
        st.warning("⚠️ No valid data to generate a report.")
    else:
        total_questions = len(valid_history)
        st.info(f"📊 Report ready! Recorded: {total_questions}")
        last_chat = valid_history[-1]
        
        is_marathi = last_chat['lang'] == "Marathi"
        is_hindi = last_chat['lang'] == "Hindi"
        
        # 🎯 मांडणी: प्रश्न डार्क बोल्ड निळा आणि उत्तर फिकट राखाडी
        history_html_content = ""
        bundled_answer = ""
        
        for idx, chat in enumerate(valid_history, 1):
            q_text = chat['query']
            a_text = chat['answer'].replace('\n', '<br>')
            
            history_html_content += f"""
            <div style="margin-bottom:20px;border-bottom:1px dashed #ccc;">
                <p style="color:#1E3A8A;font-weight:900;"><b>Q.{idx} {q_text}</b></p>
                <p style="color:#4B5563;font-weight:400;">{a_text}</p>
            </div>
            """
            bundled_answer += f"\n### Q.{idx} {chat['query']}\n{chat['answer']}\n"
            
        # --------------------------------------------------
        # केस १: हिंदी डिजिटल रिपोर्ट
        # --------------------------------------------------
        if is_hindi:
            st.markdown("### 📥 डिजिटल रिपोर्ट डाउनलोड करें")
            st.success(f"✓ भाषा हिंदी। कुल {total_questions} प्रश्न।")
            
            html_template = f"""
            <html><head><meta charset="utf-8">
            <style>
                body {{ font-family:Arial; margin:40px; line-height:1.6; }}
                h1 {{ color:#1E3A8A; text-align:center; }}
                .meta {{ background:#F3F4F6; padding:10px; }}
            </style></head>
            <body>
                <h1>PharmaGen AI Copilot</h1>
                <div class="meta"><p><b>फ़ाइल:</b> {", ".join(st.session_state.processed_files)}</p></div>
                {history_html_content}
            </body></html>
            """
            st.download_button(
                label="📥 डाउनलोड हिंदी डिजिटल रिपोर्ट (.html)",
                data=html_template,
                file_name="PharmaGen_Hindi_Report.html",
                mime="text/html",
                use_container_width=True
            )
            
        # --------------------------------------------------
        # केस २: मराठी डिजिटल अहवाल
        # --------------------------------------------------
        elif is_marathi:
            st.markdown("### 📥 डिजिटल अहवाल डाउनलोड करा")
            st.success(f"✓ भाषा मराठी। एकूण {total_questions} प्रश्न।")
            
            html_template = f"""
            <html><head><meta charset="utf-8">
            <style>
                body {{ font-family:Arial; margin:40px; line-height:1.6; }}
                h1 {{ color:#1E3A8A; text-align:center; }}
                .meta {{ background:#F3F4F6; padding:10px; }}
            </style></head>
            <body>
                <h1>PharmaGen AI Copilot</h1>
                <div class="meta"><p><b>फाईल:</b> {", ".join(st.session_state.processed_files)}</p></div>
                {history_html_content}
            </body></html>
            """
            st.download_button(
                label="📥 डाउनलोड मराठी डिजिटल अहवाल (.html)",
                data=html_template,
                file_name="PharmaGen_Marathi_Report.html",
                mime="text/html",
                use_container_width=True
            )
            
        # --------------------------------------------------
        # केस ३: इंग्रजी Consolidated PDF
        # --------------------------------------------------
        else:
            st.markdown("### 📄 Generate Consolidated PDF Report")
            if st.button("📄 Generate PDF Report", use_container_width=True):
                with st.spinner("Bundling history..."):
                    try:
                        source_display = ", ".join(st.session_state.processed_files)
                        pdf_data = generate_report(source_display, "History Log", bundled_answer)
                        st.download_button(
                            label="📥 Download English PDF",
                            data=bytes(pdf_data),
                            file_name="PharmaGen_English_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Failed: {e}")