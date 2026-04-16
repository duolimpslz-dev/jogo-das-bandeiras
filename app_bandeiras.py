import streamlit as st
import random

# --- Configuração da Página ---
st.set_page_config(page_title="Mestre das Bandeiras 96", layout="centered")

# --- Banco de Dados com 96 Países ---
# Organizado para cobrir todos os continentes
paises_dados = [
    # AMÉRICAS (20)
    ("Brasil", "br"), ("Argentina", "ar"), ("Uruguai", "uy"), ("Paraguai", "py"),
    ("Chile", "cl"), ("Bolívia", "bo"), ("Peru", "pe"), ("Colômbia", "co"),
    ("Equador", "ec"), ("Venezuela", "ve"), ("Estados Unidos", "us"), ("Canadá", "ca"),
    ("México", "mx"), ("Cuba", "cu"), ("Panamá", "pa"), ("Costa Rica", "cr"),
    ("Jamaica", "jm"), ("Haiti", "ht"), ("República Dominicana", "do"), ("Guatemala", "gt"),
    
    # EUROPA (25)
    ("Portugal", "pt"), ("Espanha", "es"), ("França", "fr"), ("Itália", "it"),
    ("Alemanha", "de"), ("Reino Unido", "gb"), ("Irlanda", "ie"), ("Bélgica", "be"),
    ("Holanda", "nl"), ("Suíça", "ch"), ("Áustria", "at"), ("Grécia", "gr"),
    ("Rússia", "ru"), ("Ucrânia", "ua"), ("Polônia", "pl"), ("Noruega", "no"),
    ("Suécia", "se"), ("Finlândia", "fi"), ("Dinamarca", "dk"), ("Islândia", "is"),
    ("Croácia", "hr"), ("Sérvia", "rs"), ("República Tcheca", "cz"), ("Hungria", "hu"), ("Romênia", "ro"),
    
    # ÁSIA (25)
    ("Japão", "jp"), ("China", "cn"), ("Coreia do Sul", "kr"), ("Índia", "in"),
    ("Tailândia", "th"), ("Vietnã", "vn"), ("Indonésia", "id"), ("Malásia", "my"),
    ("Filipinas", "ph"), ("Cazaquistão", "kz"), ("Israel", "il"), ("Arábia Saudita", "sa"),
    ("Irã", "ir"), ("Iraque", "iq"), ("Turquia", "tr"), ("Paquistão", "pk"),
    ("Catar", "qa"), ("Emirados Árabes Unidos", "ae"), ("Cingapura", "sg"), ("Líbano", "lb"),
    ("Jordânia", "jo"), ("Camboja", "kh"), ("Coreia do Norte", "kp"), ("Mongólia", "mn"), ("Nepal", "np"),

    # ÁFRICA (20)
    ("Egito", "eg"), ("África do Sul", "za"), ("Angola", "ao"), ("Nigéria", "ng"),
    ("Marrocos", "ma"), ("Argélia", "dz"), ("Tunísia", "tn"), ("Líbia", "ly"),
    ("Gana", "gh"), ("Senegal", "sn"), ("Camarões", "cm"), ("Costa do Marfim", "ci"),
    ("Quênia", "ke"), ("Etiópia", "et"), ("Tanzânia", "tz"), ("Uganda", "ug"),
    ("Moçambique", "mz"), ("Madagascar", "mg"), ("Cabo Verde", "cv"), ("Guiné-Bissau", "gw"),

    # OCEANIA (6)
    ("Austrália", "au"), ("Nova Zelândia", "nz"), ("Fiji", "fj"), ("Papua Nova Guiné", "pg"),
    ("Samoa", "ws"), ("Palau", "pw")
]

# --- Inicialização do Jogo ---
if 'lista_sorteada' not in st.session_state:
    # Sorteia 12 países diferentes do total de 96
    st.session_state.lista_sorteada = random.sample(paises_dados, 12)
    st.session_state.indice = 0
    st.session_state.pontos = 0
    st.session_state.feedback = None

st.title("🌍 Quiz: Desafio dos Países do MANUCA BARROS")
st.write("Cada partida sorteia **12 bandeiras** diferentes da nossa base de dados.")

# --- Lógica das Rodadas ---
if st.session_state.indice < len(st.session_state.lista_sorteada):
    correto, cod = st.session_state.lista_sorteada[st.session_state.indice]
    
    st.write(f"### Pontuação: {st.session_state.pontos} | Pergunta {st.session_state.indice + 1} de 12")
    
    # Imagem da bandeira (FlagCDN)
    st.image(f"https://flagcdn.com/w640/{cod}.png", use_container_width=True)

    if st.session_state.feedback is None:
        # Gera 4 opções (1 correta + 3 erradas sorteadas dos 96)
        if f'opc_{st.session_state.indice}' not in st.session_state:
            errados = [p[0] for p in paises_dados if p[0] != correto]
            opcoes = random.sample(errados, 3)
            opcoes.append(correto)
            random.shuffle(opcoes)
            st.session_state[f'opc_{st.session_state.indice}'] = opcoes

        st.write("### Qual é este país?")
        # Botões de múltipla escolha
        for opt in st.session_state[f'opc_{st.session_state.indice}']:
            if st.button(opt, key=f"btn_{opt}_{st.session_state.indice}", use_container_width=True):
                if opt == correto:
                    st.session_state.feedback = "✅ EXCELENTE! Você acertou."
                    st.session_state.pontos += 1
                else:
                    st.session_state.feedback = f"❌ QUASE! O correto era {correto}."
                st.rerun()
    else:
        # Tela de Feedback
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
            
        if st.button("PRÓXIMA BANDEIRA ➡️", use_container_width=True):
            st.session_state.feedback = None
            st.session_state.indice += 1
            st.rerun()
else:
    # Tela Final
    st.balloons()
    st.header("🏆 Fim da Jornada!")
    st.write(f"Você acertou **{st.session_state.pontos}** de 12 bandeiras.")
    
    if st.button("🔄 Jogar Novamente (Sortear novos países)"):
        # Limpa o estado para recomeçar do zero com novos sorteios
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
