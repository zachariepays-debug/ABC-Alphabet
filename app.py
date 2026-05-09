import streamlit as st
from gtts import gTTS
import base64
import io

st.set_page_config(page_title="App Bébé", page_icon="👶")

def parler(texte):
    tts = gTTS(text=str(texte), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    audio_b64 = base64.b64encode(fp.getvalue()).decode()
    html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
    st.markdown(html_string, unsafe_allow_html=True)

st.title("👶 Mon App Éducative")

tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    st.subheader("Apprends les lettres")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols = st.columns(6)
    for i, lettre in enumerate(alphabet):
        with cols[i % 6]:
            if st.button(lettre, key=f"btn_{lettre}"):
                parler(lettre)

with tab2:
    st.subheader("Apprends les chiffres")
    chiffres = "0123456789"
    cols_c = st.columns(5)
    for i, chiffre in enumerate(chiffres):
        with cols_c[i % 5]:
            if st.button(chiffre, key=f"btn_{chiffre}"):
                parler(chiffre)