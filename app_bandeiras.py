import streamlit as st
import random

# --- Configuração ---
st.set_page_config(page_title="Quiz Bandeiras", layout="centered")

# Lista expandida com os 48 países (ou mais)
paises_dados = [
    ("Brasil", "br"), ("Argentina", "ar"), ("França", "fr"), ("Japão", "jp"), 
    ("Itália", "it"), ("Alemanha", "de"), ("Espanha", "es"), ("México", "mx"), 
    ("Portugal", "pt"), ("Canadá", "ca"), ("Estados Unidos", "us"), ("Austrália", "au"),
    ("Uruguai", "uy"), ("Paraguai", "py"), ("Chile", "cl"), ("Bolívia", "bo"),
    ("Peru", "pe"), ("Colômbia", "co"), ("Equador", "ec"), ("Venezuela", "ve"),
    ("Reino Unido", "gb"), ("Irlanda", "ie"), ("Bélgica", "be"), ("Holanda", "nl"),
    ("Suíça", "ch"), ("Áustria", "at"), ("Grécia", "gr"), ("Rússia", "ru"),
    ("Ucrânia", "ua"), ("Polônia", "pl"), ("Noruega", "no"), ("Suécia", "se"),
    ("Finlândia", "fi"), ("Dinamarca", "dk"), ("China", "cn"), ("Coreia do Sul", "kr"),
    ("Índia", "in"), ("Israel", "il"), ("Egito", "eg"), ("África do Sul", "za"),
    ("Angola", "ao"), ("Nigéria", "ng"), ("Nova Zelândia", "nz"), ("Tailândia", "th"),
    ("Turquia", "tr"), ("Irã", "ir"), ("Arábia Saudita", "sa"), ("Cuba", "cu")
]

# INICIALIZAÇÃO DO JOGO
if 'lista_sorteada' not in st.session_state:
    # A MÁGICA ESTÁ AQUI: Escolhe 12 países aleatórios da lista de 48
    st.session_state.lista_sorteada = random.sample(paises_dados, 12)
    st.session_state.indice = 0
    st.session_state.pontos = 0
    st.session_state.feedback = None

st.title("🏁 Quiz das Bandeiras do MANUCA BARROS")

# Verifica se ainda temos perguntas (dentro das 12 selecionadas)
if st.session_state.indice < len(st.session_state.lista_sorteada):
    correto, cod = st.session_state.lista_sorteada[st.session_state.indice]
    
    st.write(f"**Pontuação: {st.session_state.pontos}** | Pergunta {st.session_state.indice + 1} de 12")
    st.image(f"https://flagcdn.com/w640/{cod}.png", use_container_width=True)

    if st.session_state.feedback is None:
        # Gera opções de múltipla escolha
        if f'opc_{st.session_state.indice}' not in st.session_state:
            # Pega 3 países errados de toda a base de dados
            outros = [p[0] for p in paises_dados if p[0] != correto]
            opcoes = random.sample(outros, 3)
            opcoes.append(correto)
            random.shuffle(opcoes)
            st.session_state[f'opc_{st.session_state.indice}'] = opcoes

        st.write("### Qual é este país?")
        for opt in st.session_state[f'opc_{st.session_state.indice}']:
            if st.button(opt, key=f"btn_{opt}_{st.session_state.indice}", use_container_width=True):
                if opt == correto:
                    st.session_state.feedback = "✅ ACERTOU!"
                    st.session_state.pontos += 1
                else:
                    st.session_state.feedback = f"❌ ERROU! O correto era {correto}."
                st.rerun()
    else:
        # Tela de feedback antes de passar para a próxima
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
            
        if st.button("PRÓXIMA BANDEIRA ➡️", use_container_width=True):
            st.session_state.feedback = None
            st.session_state.indice += 1
            st.rerun()
else:
    # Fim de jogo após as 12 perguntas
    st.balloons()
    st.write("### 🏆 Fim da Rodada!")
    st.write(f"Você acertou **{st.session_state.pontos}** de 12 bandeiras.")
    
    if st.button("Jogar Novamente (Sortear novos países)"):
        # Limpa tudo para o random.sample rodar de novo no início
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
