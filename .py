import tkinter as tk
from tkinter import messagebox
import random
import time


# 🎓 Pares de memória por matéria
MEMORIA_PARES = {
    "Matemática": [
        ("2 + 2" , 4"),
        ("3 + 5", "8"),
        ("10 - 7", "3"),
        ("6 / 2", "3"),
    ],
    "Português": [
        ("Cão", "Animal que late"),
        ("Casa", "Lugar onde moramos"),
        ("Livro", "Objeto para ler"),
        ("Amigo", "Pessoa querida"),
    ],
    "Ciências": [
        ("Sol", "Estrela do nosso sistema"),
        ("Água", "Substância essencial à vida"),
        ("Pulmão", "Órgão que usamos para respirar"),
        ("Terra", "Planeta onde vivemos"),
    ],
    "História": [
        ("1500", "Descobrimento do Brasil"),
        ("Dom Pedro II", "Imperador do Brasil"),
        ("Pedro Álvares Cabral", "Descobridor do Brasil"),
        ("Independência", "Ocorreu em 1822"),
    ],
    "Geografia": [
        ("Brasil", "País da América do Sul"),
        ("Amazonas", "Maior rio do Brasil"),
        ("Oceano Atlântico", "Banha o litoral brasileiro"),
        ("África", "Continente ao leste da América do Sul"),
    ]
}




# ============================
# 🌟 Tela de menu inicial
# ============================
class MenuInicial:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória <3")
        self.root.geometry("450x500")
        self.root.config(bg="#f9f9f9")


        tk.Label(root, text="Jogo da Memória da Mente Ativa", font=("Arial", 18, "bold"), bg="#f9f9f9").pack(pady=20)
        tk.Label(root, text="Escolha as matérias para jogar:", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)


        self.materias_vars = {}
        for materia in MEMORIA_PARES.keys():
            var = tk.BooleanVar()
            chk = tk.Checkbutton(root, text=materia, variable=var, bg="#f9f9f9", font=("Arial", 12))
            chk.pack(anchor="w", padx=100)
            self.materias_vars[materia] = var


        # Escolha de dificuldade
        tk.Label(root, text="Selecione o nível de dificuldade:", font=("Arial", 14), bg="#f9f9f9").pack(pady=15)
        self.dificuldade = tk.StringVar(value="Fácil")
        for nivel in ["Fácil", "Médio", "Difícil"]:
            tk.Radiobutton(root, text=nivel, variable=self.dificuldade, value=nivel,
                           bg="#f9f9f9", font=("Arial", 12)).pack(anchor="w", padx=120)


        tk.Button(root, text="Começar Jogo ▶️", font=("Arial", 14, "bold"),
                  bg="#4CAF50", fg="white", command=self.iniciar_jogo).pack(pady=25)


    def iniciar_jogo(self):
        materias_escolhidas = [m for m, v in self.materias_vars.items() if v.get()]
        if not materias_escolhidas:
            messagebox.showwarning("Atenção ⚠️", "Selecione pelo menos uma matéria!")
            return


        pares = []
        for materia in materias_escolhidas:
            pares.extend(MEMORIA_PARES[materia])


        random.shuffle(pares)


        # Ajusta a dificuldade
        nivel = self.dificuldade.get()
        if nivel == "Fácil":
            tempo_limite = 60
            pares = pares[:3]  # menos pares
        elif nivel == "Médio":
            tempo_limite = 40
            pares = pares[:4]
        else:
            tempo_limite = 20
            pares = pares[:5]  # mais pares


        cartas = []
        for p1, p2 in pares:
            cartas.append(p1)
            cartas.append(p2)
        random.shuffle(cartas)


        self.root.destroy()
        abrir_jogo(cartas, tempo_limite)




# ============================
# 🧠 Classe do jogo da memória
# ============================
class JogoMemoria:
    def __init__(self, root, cartas, tempo_limite=60):
        self.root = root
        self.root.title("Jogo da Memória 🧩")
        self.root.geometry("600x600")
        self.root.config(bg="#f9f9f9")


        self.cartas = cartas
        self.botoes = []
        self.selecao = []
        self.pontuacao = 0
        self.tentativas = 0
        self.tempo_limite = tempo_limite
        self.tempo_restante = tempo_limite


        tk.Label(root, text="Encontre os pares correspondentes!", font=("Arial", 18, "bold"), bg="#f9f9f9").pack(pady=10)


        info_frame = tk.Frame(root, bg="#f9f9f9")
        info_frame.pack()


        self.label_pontuacao = tk.Label(info_frame, text="Pontuação: 0", font=("Arial", 14), bg="#f9f9f9")
        self.label_pontuacao.grid(row=0, column=0, padx=30)


        self.label_tempo = tk.Label(info_frame, text=f"Tempo: {self.tempo_restante}s", font=("Arial", 14), bg="#f9f9f9")
        self.label_tempo.grid(row=0, column=1, padx=30)


        self.tabuleiro = tk.Frame(root, bg="#f9f9f9")
        self.tabuleiro.pack(pady=20)


        self.criar_botoes()
        self.atualizar_tempo()


    def criar_botoes(self):
        colunas = int(len(self.cartas) ** 0.5)
        for i, texto in enumerate(self.cartas):
            btn = tk.Button(self.tabuleiro, text="❓", width=18, height=6, font=("Arial", 12, "bold"),
                            bg="#E0E0E0", command=lambda i=i: self.revelar_carta(i))
            btn.grid(row=i // colunas, column=i % colunas, padx=8, pady=8)
            self.botoes.append(btn)


    def atualizar_tempo(self):
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.label_tempo.config(text=f"Tempo: {self.tempo_restante}s")
            self.root.after(1000, self.atualizar_tempo)
        else:
            self.encerrar_tempo()


    def revelar_carta(self, indice):
        if len(self.selecao) == 2 or self.botoes[indice]["state"] == "disabled":
            return
        self.botoes[indice].config(text=self.cartas[indice], bg="#DDEEFF")
        self.selecao.append(indice)
        if len(self.selecao) == 2:
            self.root.after(800, self.verificar_par)


    def verificar_par(self):
        i1, i2 = self.selecao
        c1, c2 = self.cartas[i1], self.cartas[i2]
        self.tentativas += 1


        if self.eh_par(c1, c2):
            self.botoes[i1].config(bg="#A5D6A7", state="disabled")
            self.botoes[i2].config(bg="#A5D6A7", state="disabled")
            self.pontuacao += 1
        else:
            self.botoes[i1].config(text="❓", bg="#E0E0E0")
            self.botoes[i2].config(text="❓", bg="#E0E0E0")


        self.selecao.clear()
        self.label_pontuacao.config(text=f"Pontuação: {self.pontuacao}")


        if self.pontuacao == len(self.cartas) // 2:
            self.finalizar_jogo(True)


    def encerrar_tempo(self):
        for btn in self.botoes:
            btn.config(state="disabled", bg="#F8BBD0")
        self.finalizar_jogo(False)


    def eh_par(self, c1, c2):
        for pares in MEMORIA_PARES.values():
            for p1, p2 in pares:
                if (c1 == p1 and c2 == p2) or (c1 == p2 and c2 == p1):
                    return True
        return False


    def finalizar_jogo(self, venceu):
        if venceu:
            mensagem = f"🎉 Parabéns! Você completou o jogo!\nTentativas: {self.tentativas}"
        else:
            mensagem = f"⏰ Tempo esgotado!\nPontuação final: {self.pontuacao}"
        resposta = messagebox.askyesno("Fim de Jogo", f"{mensagem}\n\nDeseja jogar novamente?")
        self.root.destroy()
        if resposta:
            iniciar_programa()  # reinicia o jogo




# ============================
# 🚀 Função para abrir o jogo
# ============================
def abrir_jogo(cartas, tempo_limite):
    root = tk.Tk()
    JogoMemoria(root, cartas, tempo_limite)
    root.mainloop()




# ============================
# 🏁 Loop principal
# ============================
def iniciar_programa():
    root = tk.Tk()
    MenuInicial(root)
    root.mainloop()




if __name__ == "__main__":
    iniciar_programa()



