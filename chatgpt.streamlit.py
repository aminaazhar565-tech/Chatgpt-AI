
import streamlit as st
import textwrap
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="FinanceAI | Personal Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# PROFESSIONAL CSS
# ==========================================================
css_code = """
<style>
    /* GLOBAL */
    .stApp {
        background: #f6f8fc;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* HEADER */
    .finance-header {
        background: linear-gradient(135deg, #0f172a 0%, #172554 50%, #1e3a8a 100%);
        padding: 30px 34px;
        border-radius: 22px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.15);
    }

    .finance-header h1 {
        color: white !important;
        margin: 0;
        font-size: 36px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .finance-header p {
        color: #cbd5e1 !important;
        margin: 8px 0 0 0;
        font-size: 15px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
        box-border:black;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #1e293b;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }

    .sidebar-brand {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    .sidebar-brand-title {
        color: white !important;
        font-size: 22px;
        font-weight: 700;
        margin: 0;
    }

    .sidebar-brand-subtitle {
        color: #cbd5e1 !important;
        font-size: 12px;
        margin-top: 4px;
    }

    /* API STATUS CARDS */
    .api-card {
        padding: 14px 15px;
        border-radius: 13px;
        margin-top: 10px;
        font-size: 13px;
        line-height: 1.5;
    }

    .api-card.locked {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412 !important;
    }

    .api-card.valid {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534 !important;
    }

    .api-card.error {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b !important;
    }

    /* INFO CARDS */
    .info-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
        min-height: 145px;
        transition: 0.2s;
    }

    .info-card:hover {
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.09);
    }

    .info-card-icon {
        font-size: 27px;
        margin-bottom: 8px;
    }

    .info-card h3 {
        color: #0f172a !important;
        font-size: 17px;
        margin: 0 0 7px 0;
    }

    .info-card p {
        color: #64748b !important;
        font-size: 13px;
        margin: 0;
        line-height: 1.6;
    }

    /* SECTION TITLE */
    .section-title {
        color: #0f172a;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* CHAT INPUT & MESSAGE */
    div[data-testid="stChatInput"] {
        border-radius: 18px;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 16px !important;
        border: 1px solid #cbd5e1 !important;
        background: white !important;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        margin-bottom: 10px;
    }

    /* DISCLAIMER */
    .disclaimer {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 14px 16px;
        border-radius: 13px;
        color: #64748b !important;
        font-size: 11px;
        line-height: 1.5;
        margin-top: 20px;
    }

    /* STATUS BADGE */
    .ready-badge {
        display: inline-block;
        background: #dcfce7;
        color: #166534 !important;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)


# ==========================================================
# HEADER
# ==========================================================
st.markdown("""<div class="finance-header">
    <h1>💰 FinanceAI</h1>
    <p>Your Personal AI Financial Assistant — Smart insights for better financial decisions.</p>
</div>""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_valid" not in st.session_state:
    st.session_state.api_valid = False

if "tested_api_key" not in st.session_state:
    st.session_state.tested_api_key = ""

if "api_error" not in st.session_state:
    st.session_state.api_error = ""


# ==========================================================
# API KEY VALIDATION
# ==========================================================
def validate_api_key():
    key = st.session_state.get("api_key_input", "").strip()

    if not key:
        st.session_state.api_valid = False
        st.session_state.tested_api_key = ""
        st.session_state.api_error = ""
        return

    if key == st.session_state.tested_api_key:
        return

    st.session_state.api_valid = False
    st.session_state.api_error = ""

    try:
        test_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=key
        )
        test_model.invoke("Reply with exactly: VALID")

        st.session_state.api_valid = True
        st.session_state.tested_api_key = key
        st.session_state.api_error = ""

    except Exception as e:
        st.session_state.api_valid = False
        st.session_state.tested_api_key = key
        st.session_state.api_error = str(e)


# ==========================================================
# SIDEBAR
# ==========================================================
with st.sidebar:

    st.markdown("""<div class="sidebar-brand">
        <div class="sidebar-brand-title">💰 FinanceAI</div>
        <div class="sidebar-brand-subtitle">Personal Finance Assistant</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 🔑 OpenAI API Key")

    st.text_input(
        "Enter your API key",
        type="password",
        placeholder="sk-...",
        key="api_key_input",
        on_change=validate_api_key,
        help="Your API key is tested automatically."
    )

    if not st.session_state.get("api_key_input", ""):
        st.markdown("""<div class="api-card locked">
            🔒 <b>Chat Locked</b><br>
            Enter your API key to activate FinanceAI.
        </div>""", unsafe_allow_html=True)

    elif st.session_state.api_valid:
        st.markdown("""<div class="api-card valid">
            ✅ <b>API Key Verified</b><br>
            FinanceAI is ready to use.
        </div>""", unsafe_allow_html=True)

    elif st.session_state.api_error:
        st.markdown("""<div class="api-card error">
            ❌ <b>API Key Error</b><br>
            The entered key is invalid or unavailable. Please check your key and try again.
        </div>""", unsafe_allow_html=True)

    else:
        st.info("🔄 Testing API key...")

    st.divider()

    st.markdown("### ⚙️ AI Settings")

    model_name = st.selectbox(
        "AI Model",
        ["gpt-4o-mini", "gpt-4o"]
    )

    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1
    )

    st.divider()

    st.markdown("### 🎯 Finance Focus")

    domain = st.selectbox(
        "Assistant Focus",
        [
            "Personal Finance",
            "Budget Planning",
            "Expense Analysis",
            "Saving Strategy",
            "Financial Education"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""<div class="disclaimer">
        ⚠️ <b>Financial Disclaimer</b><br><br>
        FinanceAI provides educational financial information and general guidance. It does not guarantee investment returns or provide professional financial advice.
    </div>""", unsafe_allow_html=True)


# ==========================================================
# SYSTEM PROMPT
# ==========================================================
system_message = f"""
You are FinanceAI, a professional AI Personal Finance Assistant.
Your ONLY purpose is to help users with FINANCE-related topics.

Current finance focus:
{domain}

==========================================================
FINANCE TOPICS YOU CAN ANSWER
==========================================================
• Personal finance & Budget planning
• Income, expenses, and tracking
• Savings, Emergency funds & Financial goals
• Debt, Loans, Credit & Banking
• Investment education & Financial calculations

==========================================================
STRICT FINANCE-ONLY RULE
==========================================================
You MUST ONLY answer questions related to finance.
If the question is NOT related to finance, respond with:
"Sorry, I am not able to answer this question. I can only help with finance and personal finance topics."
"""


# ==========================================================
# CREATE AI MODEL
# ==========================================================
chat = None

if st.session_state.api_valid:
    chat = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=st.session_state.api_key_input
    )


# ==========================================================
# WELCOME SECTION
# ==========================================================
if len(st.session_state.messages) == 0:

    st.markdown('<div class="section-title">👋 Welcome to FinanceAI</div>', unsafe_allow_html=True)

    if st.session_state.api_valid:
        st.markdown('<div class="ready-badge">● FinanceAI is ready</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<div class="info-card">
            <div class="info-card-icon">💳</div>
            <h3>Expense Analysis</h3>
            <p>Understand where your money goes and identify spending patterns.</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="info-card">
            <div class="info-card-icon">🎯</div>
            <h3>Smart Budgeting</h3>
            <p>Create practical monthly budgets and organize your finances.</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class="info-card">
            <div class="info-card-icon">📈</div>
            <h3>Saving Strategy</h3>
            <p>Explore practical ways to save money and reach financial goals.</p>
        </div>""", unsafe_allow_html=True)

    if not st.session_state.api_valid:
        st.info("🔐 Enter your OpenAI API key in the sidebar to unlock the chat.")
    else:
        st.success("✅ API key verified. You can now ask your finance-related question below.")


# ==========================================================
# CHAT HISTORY
# ==========================================================
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


# ==========================================================
# CHAT INPUT & PROCESS
# ==========================================================
user_prompt = st.chat_input(
    "Ask FinanceAI about budgeting, saving, expenses, investing...",
    disabled=not st.session_state.api_valid
)

if user_prompt:
    if not st.session_state.api_valid:
        st.error("🔒 Please enter a valid OpenAI API key first.")
    else:
        messages_for_ai = [SystemMessage(content=system_message)]
        messages_for_ai.extend(st.session_state.messages)

        human_message = HumanMessage(content=user_prompt)
        messages_for_ai.append(human_message)

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("💰 FinanceAI is analyzing..."):
                try:
                    response = chat.invoke(messages_for_ai)
                    answer = response.content
                    st.markdown(answer)

                    st.session_state.messages.append(human_message)
                    st.session_state.messages.append(AIMessage(content=answer))

                except Exception as e:
                    st.error("❌ Something went wrong.")
                    st.caption(str(e))