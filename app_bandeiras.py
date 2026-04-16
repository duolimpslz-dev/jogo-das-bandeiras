import streamlit as st
import random
import unicodedata
from urllib.request import urlopen
import io
from PIL import Image

# --- Configuração Visual ---
st.set_page_config(page_title="Desafio das Bandeiras do MANUCA BARROS", page_icon="🌍")

# Estilo para deixar o site bonito no celular
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #27ae60; color: white; }
    .main { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

def remover_acentos(texto):
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn').lower().strip()

# --- Lista de Países ---
if 'paises' not in st.session_state:
    lista_base = [
        ("Brasil", "br"), ("Argentina", "ar"), ("Uruguai", "uy"), ("Portugal", "pt"),
        ("França", "fr"), ("Japão", "jp"), ("Itália", "it"), ("Alemanha", "de"),
        ("Espanha", "es"), ("Canadá", "ca"), ("Estados Unidos", "us"), ("México", "mx")
    ]
    random.shuffle(lista_base)
    st.session_state.paises = lista_base
    st.session_state.indice = 0
    st.session_state.pontos = 0

# --- Jogo ---
st.title("🌍 Desafio das Bandeiras do MANUCA BARROS")

if st.session_state.indice < len(st.session_state.paises):
    nome_correto, codigo = st.session_state.paises[st.session_state.indice]
    
    # Placar
    st.subheader(f"Pontos: {st.session_state.pontos} | {st.session_state.indice + 1}/{len(st.session_state.paises)}")
    
    # Imagem da Bandeira
    url = f"https://flagcdn.com/w640/{codigo}.png"
    st.image(url, use_container_width=True)

    # Entrada de texto e Botão
    with st.form(key='jogo_form', clear_on_submit=True):
        resposta = st.text_input("Qual é o país?", placeholder="Digite aqui...")
        submit = st.form_submit_button("Confirmar Resposta")

    if submit:
        if remover_acentos(resposta) == remover_acentos(nome_correto):
            st.success(f"✅ Acertou! É o(a) {nome_correto}!")
            st.session_state.pontos += 1
        else:
            st.error(f"❌ Errou! Era: {nome_correto}")
        
        st.session_state.indice += 1
        st.button("Próxima Bandeira ➡️")

else:
    st.balloons()
    st.header("🏆 Fim de Jogo!")
    st.write(f"Sua pontuação final foi: **{st.session_state.pontos} pontos**.")
    if st.button("Jogar Novamente"):
        del st.session_state.paises
        st.rerun()
