import tkinter as tk
from urllib.request import urlopen
import io
import random
import unicodedata
from PIL import Image, ImageTk

class JogoBandeirasSupremo:
    def __init__(self, root):
        self.root = root
        self.root.title("Master Geografia: Desafio das Bandeiras")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c3e50") # Um fundo mais escuro e elegante

        # Base de dados expandida (Nome, Código ISO)
        # O código de acentos permite que você digite "Ira" para "Irã", etc.
        self.todos_paises = [
            ("Brasil", "br"), ("Argentina", "ar"), ("Uruguai", "uy"), ("Paraguai", "py"),
            ("Chile", "cl"), ("Bolivia", "bo"), ("Peru", "pe"), ("Colombia", "co"),
            ("Equador", "ec"), ("Venezuela", "ve"), ("Estados Unidos", "us"), ("Canada", "ca"),
            ("Mexico", "mx"), ("Cuba", "cu"), ("Portugal", "pt"), ("Espanha", "es"),
            ("França", "fr"), ("Italia", "it"), ("Alemanha", "de"), ("Reino Unido", "gb"),
            ("Irlanda", "ie"), ("Belgica", "be"), ("Holanda", "nl"), ("Suíça", "ch"),
            ("Austria", "at"), ("Grecia", "gr"), ("Russia", "ru"), ("Ucrânia", "ua"),
            ("Polonia", "pl"), ("Noruega", "no"), ("Suecia", "se"), ("Finlândia", "fi"),
            ("Dinamarca", "dk"), ("Japao", "jp"), ("China", "cn"), ("Coreia do Sul", "kr"),
            ("India", "in"), ("Israel", "il"), ("Egito", "eg"), ("Africa do Sul", "za"),
            ("Angola", "ao"), ("Nigeria", "ng"), ("Australia", "au"), ("Nova Zelandia", "nz"),
            ("Tailandia", "th"), ("Turquia", "tr"), ("Ira", "ir"), ("Arábia Saudita", "sa")
        ]
        
        random.shuffle(self.todos_paises)
        
        self.indice = 0
        self.pontos = 0

        # --- Elementos Visuais ---
        self.lbl_titulo = tk.Label(root, text="QUE PAÍS É ESTE?", font=("Verdana", 22, "bold"), 
                                   fg="#ecf0f1", bg="#2c3e50")
        self.lbl_titulo.pack(pady=25)

        # Moldura para a bandeira
        self.frame_img = tk.Frame(root, bg="white", bd=5)
        self.frame_img.pack(pady=10)
        
        self.lbl_imagem = tk.Label(self.frame_img, bg="white")
        self.lbl_imagem.pack()

        self.lbl_status = tk.Label(root, text="", font=("Arial", 12), fg="#bdc3c7", bg="#2c3e50")
        self.lbl_status.pack()

        self.entrada = tk.Entry(root, font=("Arial", 20), justify="center", bd=3)
        self.entrada.pack(pady=30)
        self.entrada.bind('<Return>', lambda e: self.verificar())
        self.entrada.focus()

        self.btn_verificar = tk.Button(root, text="CONFERIR RESPOSTA", command=self.verificar, 
                                       font=("Arial", 14, "bold"), bg="#27ae60", fg="white", 
                                       padx=30, pady=10, cursor="hand2")
        self.btn_verificar.pack()

        self.lbl_feedback = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#2c3e50")
        self.lbl_feedback.pack(pady=25)

        self.carregar_proxima()

    def remover_acentos(self, texto):
        """Transforma 'Japão' em 'japao' para facilitar a comparação"""
        return "".join(c for c in unicodedata.normalize('NFD', texto)
                       if unicodedata.category(c) != 'Mn').lower().strip()

    def carregar_proxima(self):
        if self.indice < len(self.todos_paises):
            nome, codigo = self.todos_paises[self.indice]
            try:
                # Busca a imagem da bandeira online
                url = f"https://flagcdn.com/w320/{codigo}.png"
                with urlopen(url) as u:
                    raw_data = u.read()
                
                img_data = Image.open(io.BytesIO(raw_data))
                self.foto = ImageTk.PhotoImage(img_data)
                
                self.lbl_imagem.config(image=self.foto)
                self.lbl_status.config(text=f"Bandeira {self.indice + 1} de {len(self.todos_paises)} | Pontos: {self.pontos}")
                self.entrada.delete(0, tk.END)
            except Exception as e:
                print(f"Erro ao carregar: {e}")
                self.proximo_sem_esperar()
        else:
            self.finalizar()

    def verificar(self):
        # Normaliza tanto a resposta do usuário quanto a resposta correta
        resposta_usuario = self.remover_acentos(self.entrada.get())
        resposta_correta = self.remover_acentos(self.todos_paises[self.indice][0])

        if resposta_usuario == "": return # Evita confirmar vazio

        if resposta_usuario == resposta_correta:
            self.pontos += 1
            self.lbl_feedback.config(text="✅ ACERTOU!", fg="#2ecc71")
        else:
            nome_real = self.todos_paises[self.indice][0]
            self.lbl_feedback.config(text=f"❌ ERRADO! Era {nome_real}", fg="#e74c3c")

        # Bloqueia a entrada enquanto espera o próximo
        self.btn_verificar.config(state="disabled")
        self.root.after(1500, self.proximo_fluxo)

    def proximo_fluxo(self):
        self.btn_verificar.config(state="normal")
        self.lbl_feedback.config(text="")
        self.indice += 1
        self.carregar_proxima()

    def proximo_sem_esperar(self):
        self.indice += 1
        self.carregar_proxima()

    def finalizar(self):
        self.lbl_titulo.config(text="RANKING FINAL")
        self.lbl_imagem.config(image="")
        self.frame_img.pack_forget()
        self.lbl_status.config(text="")
        
        aproveitamento = (self.pontos / len(self.todos_paises)) * 100
        msg = f"Você acertou {self.pontos} de {len(self.todos_paises)}\n({aproveitamento:.1f}%)"
        
        self.lbl_feedback.config(text=msg, fg="#f1c40f")
        self.entrada.pack_forget()
        self.btn_verificar.config(text="SAIR", command=self.root.quit, bg="#c0392b")

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoBandeirasSupremo(root)
    root.mainloop()
