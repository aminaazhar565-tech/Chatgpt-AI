
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="FinanceAI | Personal Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f5f7fb;
    }

    /* Header */
    .finance-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 8px 25px rgba(15,23,42,0.15);
    }

    .finance-header h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 700;
    }

    .finance-header p {
        margin-top: 8px;
        color: #cbd5e1;
        font-size: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: black;
    }

    /* Cards */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(15,23,42,0.06);
        margin-bottom: 15px;
    }

    .info-card h3 {
        margin-bottom: 5px;
        color: #0f172a;
    }

    .info-card p {
        color: #64748b;
        font-size: 14px;
    }

    /* Status */
    .status {
        padding: 10px 14px;
        border-radius: 10px;
        background: #14532d;
        color: #dcfce7;
        text-align: center;
        font-size: 13px;
        margin-top: 10px;
    }

    /* Disclaimer */
    .disclaimer {
        font-size: 12px;
        color: #64748b;
        text-align: center;
        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="finance-header">
    <h1>💰 FinanceAI</h1>
    <p>Your Personal AI Financial Assistant — Smart insights for better financial decisions.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown("## 💰 FinanceAI")

    st.caption("Personal Finance Assistant")

    st.divider()

    # API KEY
    st.markdown("### 🔑 OpenAI API Key")

    api_key = st.text_input(
        "Enter your API key",
        type="password",
        placeholder="sk-...",
        help="Your API key is used for this session."
    )

    if api_key:
        st.success("API Key Added ✓")
    else:
        st.warning("Enter API Key to start AI")

    st.divider()

    # MODEL
    st.markdown("### ⚙️ AI Settings")

    model_name = st.selectbox(
        "Select AI Model",
        [
            "gpt-4o-mini",
            "gpt-4o"
        ]
    )

    temperature = st.slider(
        "Response Creativity",
        0.0,
        1.0,
        0.4
    )

    st.divider()

    # DOMAIN
    st.markdown("### 🎯 Finance Domain")

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

    # CLEAR CHAT
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="disclaimer">
        ⚠️ FinanceAI provides educational financial information.
        It does not provide guaranteed returns or professional investment advice.
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------
system_message = f"""
You are FinanceAI, a professional AI Personal Finance Assistant.

Your domain is: {domain}

Your responsibilities:
- Explain financial concepts in simple language.
- Help users understand income and expenses.
- Help create realistic budgets.
- Suggest practical saving strategies.
- Analyze spending patterns when data is provided.
- Help users improve financial organization.
- Explain financial terminology.
- Provide educational information about investing.

Important rules:
- Never guarantee investment returns.
- Never claim certainty about future market performance.
- Clearly mention assumptions.
- Do not present yourself as a licensed financial advisor.
- Encourage users to verify important financial decisions with a qualified professional.

Always give clear, structured and practical answers.
"""

# --------------------------------------------------
# CREATE AI MODEL
# --------------------------------------------------
if api_key:

    chat = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=api_key
    )

# --------------------------------------------------
# WELCOME SECTION
# --------------------------------------------------
if len(st.session_state.messages) == 0:

    st.markdown("### 👋 Welcome to FinanceAI")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
        <h3>💳 Expenses</h3>
        <p>Understand where your money is going and identify spending patterns.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h3>🎯 Budget</h3>
        <p>Create practical budgets and organize your monthly finances.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
        <h3>📈 Savings</h3>
        <p>Explore strategies to improve savings and reach financial goals.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "💡 Enter your OpenAI API key in the left sidebar, "
        "then ask FinanceAI a financial question below."
    )

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(msg.content)

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
user_prompt = st.chat_input(
    "Ask FinanceAI about budgeting, saving, expenses..."
)

if user_prompt:

    if not api_key:

        st.error(
            "🔑 Please enter your OpenAI API Key in the left sidebar first."
        )

    else:

        # Add system message only when needed
        messages_for_ai = [
            SystemMessage(content=system_message)
        ]

        messages_for_ai.extend(st.session_state.messages)

        # Add user message
        human_message = HumanMessage(
            content=user_prompt
        )

        messages_for_ai.append(human_message)

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate response
        with st.chat_message("assistant"):

            with st.spinner("FinanceAI is analyzing your request..."):

                try:

                    response = chat.invoke(
                        messages_for_ai
                    )

                    answer = response.content

                    st.markdown(answer)

                    # Save conversation
                    st.session_state.messages.append(
                        human_message
                    )

                    st.session_state.messages.append(
                        AIMessage(content=answer)
                    )

                except Exception as e:

                    st.error(
                        f"❌ Something went wrong:\n\n{str(e)}"
                    )

