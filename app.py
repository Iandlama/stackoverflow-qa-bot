
import streamlit as st
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

st.set_page_config(page_title="Stack Overflow Assistant",
                   page_icon="🐍", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }
    .stButton > button { background: linear-gradient(90deg, #00c6ff, #0072ff); color: white; border: none; border-radius: 30px; padding: 10px 30px; font-weight: bold; width: 100%; }
    .glow-title { text-align: center; font-size: 3em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stTextArea textarea { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #00c6ff; border-radius: 15px; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 3px solid #0072ff; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] label { color: #0055cc !important; }
    [data-testid="stSidebar"] h3 { color: #0088ff !important; }
    .stMarkdown, .stText { color: #ffffff !important; }
    
    /* Слово Answer — белым цветом */
    .stExpander details summary {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    .stExpander details summary::before {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 class="glow-title">
    🐍 Stack Overflow Python Assistant
</h1>
<p style="text-align: center; color: #00ff88;">Your intelligent Python question assistant</p>
""", unsafe_allow_html=True)

# Инициализация
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""
if 'auto_search' not in st.session_state:
    st.session_state.auto_search = False
if 'history' not in st.session_state:
    st.session_state.history = []


@st.cache_resource
def load_model():
    with st.spinner("🚀 Loading AI model..."):
        return SentenceTransformer('all-MiniLM-L6-v2')


@st.cache_data
def load_data():
    with st.spinner("📚 Loading data..."):
        with open('questions_small.pkl', 'rb') as f:
            questions = pickle.load(f)
        with open('question_embeddings.pkl', 'rb') as f:
            embeddings = pickle.load(f)
        with open('filtered_answers.pkl', 'rb') as f:
            answers = pickle.load(f)
        return questions, embeddings, answers


# Боковая панель
with st.sidebar:
    st.markdown("### 🎯 About")
    st.markdown(
        "**Model:** all-MiniLM-L6-v2\n**Database:** 5,000 Python questions")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_k = st.slider("Number of results", 1, 5, 3)
    threshold = st.slider("Relevance threshold", 0.1, 0.8, 0.25, 0.05)
    st.markdown("---")
    st.markdown("### 📜 History")
    for q in st.session_state.history[-5:]:
        st.markdown(f"- {q[:40]}...")

# Загрузка
try:
    model = load_model()
    questions, embeddings, answers = load_data()
    st.success("✅ Ready!")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

# Поиск


def search(question, top_k=3, threshold=0.25):
    q_emb = model.encode([question])
    sim = cosine_similarity(q_emb, embeddings)[0]
    indices = np.argsort(sim)[::-1][:top_k]

    results = []
    for idx in indices:
        if sim[idx] > threshold:
            q_id = questions.iloc[idx]['Id']
            ans = answers.get(q_id, (None, None))
            results.append({
                'relevance': float(sim[idx]),
                'title': questions.iloc[idx]['Title'],
                'body': questions.iloc[idx]['Body'],
                'score': questions.iloc[idx]['Score'],
                'answer': ans[0],
                'ans_score': ans[1]
            })
    return results


# Интерфейс
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask your question")
    user_q = st.text_area("", value=st.session_state.user_question,
                          placeholder="Example: How to merge two dictionaries?",
                          height=100, label_visibility="collapsed")

    if st.button("🔍 Search", use_container_width=True) or st.session_state.get('auto_search', False):
        if st.session_state.get('auto_search', False):
            st.session_state.auto_search = False

        if user_q:
            with st.spinner("🔍 Searching..."):
                results = search(user_q, top_k, threshold)

            if results:
                if user_q not in st.session_state.history:
                    st.session_state.history.insert(0, user_q)
                    st.session_state.history = st.session_state.history[:5]

                st.success(f"Found {len(results)} similar questions!")

                for i, r in enumerate(results, 1):
                    color = "#4CAF50" if r['relevance'] > 0.6 else "#FFC107" if r['relevance'] > 0.4 else "#FF5722"

                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin-bottom: 15px; border-left: 5px solid {color};">
                        <h3 style="color: #fff;">{i}. {r['title']}</h3>
                        <p style="color: {color};">📊 Relevance: {r['relevance']:.1%}</p>
                        <p style="color: #FFD700;">⭐ Score: {r['score']}</p>
                        <p style="color: #fff;"><strong>Question:</strong><br>{r['body']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if r['answer']:
                        with st.expander("💡 Answer"):
                            st.write(r['answer'])
                    else:
                        st.info("No answer found")
                    st.markdown("---")
            else:
                st.warning("No similar questions found.")
        else:
            st.error("Enter a question!")

with col2:
    st.markdown("### 📋 Examples")
    examples = ["How to merge two dictionaries?",
                "Difference between list and tuple", "What is a decorator?"]
    for ex in examples:
        if st.button(f"🔹 {ex}", key=ex, use_container_width=True):
            st.session_state.user_question = ex
            st.session_state.auto_search = True
            st.rerun()

st.markdown("---")
st.markdown("<div style='text-align: center; color: #667;'>🤖 Made with ❤️ for Python</div>",
            unsafe_allow_html=True)
