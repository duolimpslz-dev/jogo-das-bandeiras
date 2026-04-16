import streamlit as st
import random

# --- Configuração ---
st.set_page_config(page_title="Quiz Bandeiras", layout="centered")

# Lista de Países (Nome, Código)
paises_dados = [
    ("Brasil", "br"), ("Argentina", "ar"), ("França", "fr"), 
    ("Japão", "jp"), ("Itália", "it"), ("Alemanha", "de"),
    ("Espanha", "es"), ("México", "mx"), ("Portugal", "pt"),
    ("Canadá", "ca"), ("Estados Unidos", "us"), ("Austrália", "au")
]

# Inicializa o estado do jogo
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.pontos = 0
    random.shuffle(paises_dados)
    st.session_state.lista = paises_dados

st.title("🏁 Quiz das Bandeiras")

if st.session_state.indice < len(st.session_state.lista):
    correto, cod = st.session_state.lista[st.session_state.indice]
    
    # Placar e Progresso
    st.write(f"**Pontuação: {st.session_state.pontos}** | Bandeira {st.session_state.indice + 1} de {len(st.session_state.lista)}")
    
    # Exibe imagem
    st.image(f"https://flagcdn.com/w640/{cod}.png", use_container_width=True)
    
    # Gera opções de resposta
    if f'opc_{st.session_state.indice}' not in st.session_state:
        outros = [p[0] for p in paises_dados if p[0] != correto]
        opcoes = random.sample(outros, 3)
        opcoes.append(correto)
        random.shuffle(opcoes)
        st.session_state[f'opc_{st.session_state.indice}'] = opcoes

    st.write("### Qual é este país?")

    # Criando botões
    for opt in st.session_state[f'opc_{st.session_state.indice}']:
        if st.button(opt, key=f"{opt}_{st.session_state.indice}", use_container_width=True):
            if opt == correto:
                st.session_state.pontos += 1
                st.toast(f"Correto! Era {correto} ✅", icon="🎉") # Notificação persistente
            else:
                st.toast(f"Errou! Era {correto} ❌", icon="💥") # Notificação persistente
            
            st.session_state.indice += 1
            st.rerun()
            
else:
    st.balloons()
    st.write("### 🏆 Fim de jogo!")
    st.write(f"Você fez **{st.session_state.pontos}** pontos de um total de {len(st.session_state.lista)}.")
    if st.button("Reiniciar Jogo"):
        # Limpa tudo para recomeçar
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
