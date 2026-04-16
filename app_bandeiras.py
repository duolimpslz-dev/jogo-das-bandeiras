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
    st.session_state.feedback = None # Para saber se mostramos o resultado ou o quiz
    random.shuffle(paises_dados)
    st.session_state.lista = paises_dados

st.title("🏁 Quiz das Bandeiras do MANUCA BARROS")

# Verifica se o jogo ainda não acabou
if st.session_state.indice < len(st.session_state.lista):
    correto, cod = st.session_state.lista[st.session_state.indice]
    
    # Placar
    st.write(f"**Pontuação: {st.session_state.pontos}** | {st.session_state.indice + 1}/{len(st.session_state.lista)}")
    
    # Exibe imagem
    st.image(f"https://flagcdn.com/w640/{cod}.png", use_container_width=True)

    # LÓGICA DE TELAS:
    # Se o usuário ainda não respondeu, mostra os botões de escolha
    if st.session_state.feedback is None:
        if f'opc_{st.session_state.indice}' not in st.session_state:
            outros = [p[0] for p in paises_dados if p[0] != correto]
            opcoes = random.sample(outros, 3)
            opcoes.append(correto)
            random.shuffle(opcoes)
            st.session_state[f'opc_{st.session_state.indice}'] = opcoes

        st.write("### Qual é este país?")
        
        # Cria os botões de opção
        for opt in st.session_state[f'opc_{st.session_state.indice}']:
            if st.button(opt, key=f"btn_{opt}_{st.session_state.indice}", use_container_width=True):
                if opt == correto:
                    st.session_state.feedback = "✅ ACERTOU!"
                    st.session_state.pontos += 1
                else:
                    st.session_state.feedback = f"❌ ERROU! O correto era {correto}."
                st.rerun()

    # Se ele já respondeu, mostra a mensagem e o botão de "Próximo"
    else:
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
            
        if st.button("PRÓXIMA BANDEIRA ➡️", use_container_width=True):
            st.session_state.feedback = None # Reseta o feedback
            st.session_state.indice += 1     # Vai para a próxima
            st.rerun()
            
else:
    st.balloons()
    st.write("### 🏆 Fim de jogo!")
    st.write(f"Sua pontuação final: **{st.session_state.pontos}** pontos.")
    if st.button("Jogar Novamente"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
