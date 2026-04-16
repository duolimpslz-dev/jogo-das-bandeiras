import streamlit as st
import random
from urllib.request import urlopen

# --- Configuração da Página ---
st.set_page_config(page_title="Quiz de Bandeiras", page_icon="🏁")

# Estilo para botões grandes e coloridos
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 3.5em;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Banco de Dados Completo ---
@st.cache_data
def carregar_dados():
    return [
        ("Brasil", "br"), ("Argentina", "ar"), ("Uruguai", "uy"), ("Portugal", "pt"),
        ("França", "fr"), ("Japão", "jp"), ("Itália", "it"), ("Alemanha", "de"),
        ("Espanha", "es"), ("Canadá", "ca"), ("Estados Unidos", "us"), ("México", "mx"),
        ("Austrália", "au"), ("China", "cn"), ("Coreia do Sul", "kr"), ("Reino Unido", "gb"),
        ("Grécia", "gr"), ("Rússia", "ru"), ("Egito", "eg"), ("África do Sul", "za")
    ]

paises_lista = carregar_dados()

# --- Inicialização da Memória (Session State) ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.pontos = 0
    st.session_state.game_over = False
    random.shuffle(paises_lista)
    st.session_state.paises_jogo = paises_lista

# --- Lógica para Gerar as Opções ---
def gerar_opcoes(correto, lista_total):
    errados = [p[0] for p in lista_total if p[0] != correto]
    opcoes = random.sample(errados, 3) # Pega 3 nomes errados aleatórios
    opcoes.append(correto) # Adiciona o certo
    random.shuffle(opcoes) # Embaralha as posições
    return opcoes

# --- Interface do Jogo ---
st.title("🏁 Quiz das Bandeiras")

if not st.session_state.game_over:
    if st.session_state.indice < len(st.session_state.paises_jogo):
        pais_atual, codigo_atual = st.session_state.paises_jogo[st.session_state.indice]
        
        st.write(f"### Pontuação: {st.session_state.pontos}")
        
        # Exibe a Bandeira
        url = f"https://flagcdn.com/w640/{codigo_atual}.png"
        st.image(url, use_container_width=True)

        st.write("### Qual é este país?")

        # Se não tivermos as opções da rodada atual guardadas, geramos agora
        if f'opcoes_{st.session_state.indice}' not in st.session_state:
            st.session_state[f'opcoes_{st.session_state.indice}'] = gerar_opcoes(pais_atual, paises_lista)

        opcoes = st.session_state[f'opcoes_{st.session_state.indice}']

        # Criar botões para as opções
        # Usamos colunas para os botões ficarem organizados
        col1, col2 = st.columns(2)
        
        for i, opcao in enumerate(opcoes):
            target_col = col1 if i % 2 == 0 else col2
            if target_col.button(opcao):
                if opcao == pais_atual:
                    st.toast(f"Correto! {pais_atual} ✅", icon="🎉")
                    st.session_state.pontos += 1
                else:
                    st.toast(f"Errado! Era {pais_atual} ❌", icon="💥")
                
                st.session_state.indice += 1
                st.rerun()

    else:
        st.session_state.game_over = True
        st.rerun()
else:
    st.balloons()
    st.success("## 🏆 Fim de Jogo!")
    st.write(f"Você acertou **{st.session_state.pontos}** de **{len(st.session_state.paises_jogo)}** bandeiras!")
    
    if st.button("🔄 Jogar Novamente"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
