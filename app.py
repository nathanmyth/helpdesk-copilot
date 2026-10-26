"""Streamlit demo UI:  streamlit run app.py"""
import streamlit as st

from src.pipeline import Pipeline

st.set_page_config(page_title="HelpDesk Copilot", page_icon="🛠️")
st.title("🛠️ HelpDesk Copilot")
st.caption("Answers IT questions from the company knowledge base. Never paste passwords or MFA codes here.")


@st.cache_resource
def get_pipeline() -> Pipeline:
    return Pipeline()


if "history" not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    st.chat_message(role).markdown(content)

question = st.chat_input("e.g., How do I set up MFA on a new phone?")
if question:
    st.chat_message("user").markdown(question)
    with st.spinner("Searching the knowledge base…"):
        try:
            ans = get_pipeline().ask(question)
            reply = ans.text
        except RuntimeError as err:
            reply, ans = f"⚠️ {err}", None

    with st.chat_message("assistant"):
        st.markdown(reply)
        if ans and ans.hits:
            with st.expander("Retrieved context"):
                for h in ans.hits:
                    st.markdown(f"**{h.chunk.source}** — {h.chunk.section} (score {h.score:.2f})")
        if ans:
            st.caption(f"{ans.latency_s:.2f}s · {ans.input_tokens + ans.output_tokens} tokens")
            c1, c2 = st.columns(8)[:2]
            c1.button("👍", key=f"up{len(st.session_state.history)}")
            c2.button("👎", key=f"down{len(st.session_state.history)}")

    st.session_state.history += [("user", question), ("assistant", reply)]
