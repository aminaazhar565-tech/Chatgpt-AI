
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

    .stApp {
        background: #f5f7fb;
    }

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

    section[data-testid="stSidebar"] {
        background: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: black;
    }

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

if "api_valid" not in st.session_state:
    st.session_state.api_valid = False

if "tested_api_key" not in st.session_state:
    st.session_state.tested_api_key = ""

if "api_error" not in st.session_state:
    st.session_state.api_error = ""


# --------------------------------------------------
# API KEY VALIDATION FUNCTION
# --------------------------------------------------
def validate_api_key():
    """
    Automatically tests the OpenAI API key when the
    user enters/changes the key.
    """

    key = st.session_state.get("api_key_input", "").strip()

    # Reset if empty
    if not key:
        st.session_state.api_valid = False
        st.session_state.tested_api_key = ""
        st.session_state.api_error = ""
        return

    # Don't test the exact same key repeatedly
    if key == st.session_state.tested_api_key:
        return

    st.session_state.api_valid = False
    st.session_state.api_error = ""

    try:
        test_chat = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=key
        )

        # Small test request
        test_chat.invoke(
            "Reply with exactly: API_KEY_VALID"
        )

        st.session_state.api_valid = True
        st.session_state.tested_api_key = key
        st.session_state.api_error = ""

    except Exception as e:
        st.session_state.api_valid = False
        st.session_state.tested_api_key = key
        st.session_state.api_error = str(e)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown("## 💰 FinanceAI")
    st.caption("Personal Finance Assistant")

    st.divider()

    # --------------------------------------------------
    # API KEY
    # --------------------------------------------------
    st.markdown("### 🔑 OpenAI API Key")

    api_key = st.text_input(
        "Enter your API key",
        type="password",
        placeholder="sk-...",
        key="api_key_input",
        on_change=validate_api_key,
        help="Your API key is tested automatically after you enter it."
    )

    # API STATUS
    if api_key:

        if st.session_state.api_valid:

            st.success("✅ API Key is valid!")

            st.caption(
                "Chat is unlocked. You can now ask FinanceAI questions."
            )

        elif st.session_state.api_error:

            st.error("❌ Invalid API Key")

            st.caption(
                "Please check your API key and enter a valid key."
            )

        else:

            st.info("🔄 Testing API Key...")

    else:

        st.warning(
            "🔒 Enter a valid API Key to unlock the chat."
        )

    st.divider()

    # --------------------------------------------------
    # MODEL
    # --------------------------------------------------
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

    # --------------------------------------------------
    # DOMAIN
    # --------------------------------------------------
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

    # --------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------
    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
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

Your ONLY domain is FINANCE.

Current finance focus:
{domain}

You can help users with:

- Personal finance
- Budgeting
- Income and expenses
- Expense analysis
- Saving money
- Financial goals
- Debt management
- Financial planning
- Investment education
- Financial terminology
- Basic investing concepts
- Money management
- Emergency funds
- Credit and loans
- Banking concepts
- Financial calculations
- Spending analysis
- Saving strategies

STRICT DOMAIN RULE:

You MUST ONLY answer questions related to finance, money,
personal finance, budgeting, saving, investing, expenses,
income, debt, loans, banking, financial planning, or financial education.

If the user asks something unrelated to finance, DO NOT answer that question.

Instead respond exactly:

"Sorry, I am not able to answer this question. I can only help with finance and personal finance topics."

Examples of NON-FINANCE questions:
- Write me a Python program
- Tell me a joke
- Who is the president?
- Help me with chemistry
- Write an essay
- What is the weather?
- Tell me a recipe
- Help me with mathematics unrelated to finance

For unrelated questions, NEVER provide the actual answer.

IMPORTANT FINANCIAL SAFETY RULES:

- Never guarantee investment returns.
- Never claim certainty about future market performance.
- Clearly mention assumptions when necessary.
- Do not present yourself as a licensed financial advisor.
- Encourage users to verify important financial decisions with a qualified professional.
- Give educational information rather than guaranteed financial advice.

RESPONSE STYLE:

- Use simple language.
- Be clear and practical.
- Use headings and bullet points when useful.
- Give examples when helpful.
- If calculations are needed, show the calculation clearly.
"""


# --------------------------------------------------
# CREATE AI MODEL ONLY AFTER VALID API KEY
# --------------------------------------------------
chat = None

if st.session_state.api_valid:

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

    if not st.session_state.api_valid:

        st.info(
            "🔐 Enter a valid OpenAI API key in the left sidebar. "
            "Your API key will be tested automatically before the chat is unlocked."
        )

    else:

        st.success(
            "✅ API Key verified! FinanceAI is ready. "
            "Ask your finance-related question below."
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
    "Ask FinanceAI about budgeting, saving, expenses...",
    disabled=not st.session_state.api_valid
)


# --------------------------------------------------
# PROCESS USER QUESTION
# --------------------------------------------------
if user_prompt:

    if not st.session_state.api_valid:

        st.error(
            "🔒 Please enter a valid OpenAI API key first."
        )

    else:

        # Build conversation
        messages_for_ai = [
            SystemMessage(content=system_message)
        ]

        messages_for_ai.extend(
            st.session_state.messages
        )

        human_message = HumanMessage(
            content=user_prompt
        )

        messages_for_ai.append(
            human_message
        )

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner(
                "FinanceAI is analyzing your request..."
            ):

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
                        AIMessage(
                            content=answer
                        )
                    )

                except Exception as e:

                    st.error(
                        f"❌ Something went wrong:\n\n{str(e)}"
                    )



