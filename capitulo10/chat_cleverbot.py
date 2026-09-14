import json
import difflib
import os
import random

# ==============================
# ----------- Cleverbot---------
# ==============================
class Cleverbot:
    def __init__(self, brain_file="clever_brain.json"):
        self.brain_file = brain_file
        self.memory = {}
        self._load_brain()

    def _load_brain(self):
        # Carrega os dados salvos, se existirem
        if os.path.exists(self.brain_file):
            with open(self.brain_file, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = {}

    def _save_brain(self):
        # Salva os dados em disco
        with open(self.brain_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def find_best_match(self, user_input):
        # Encontra a frase mais semelhante já vista
        if not self.memory:
            return None
        matches = difflib.get_close_matches(user_input, self.memory.keys(), n=1, cutoff=0.6)
        return matches[0] if matches else None

    def respond(self, user_input):
        # Gera uma resposta com base na memória existente
        match = self.find_best_match(user_input)
        if match:
            responses = self.memory[match]
            return random.choice(responses)
        else:
            return None

    def learn(self, user_input, response):
        # Aprende uma nova associação de entrada e resposta
        if user_input not in self.memory:
            self.memory[user_input] = []
        self.memory[user_input].append(response)
        self._save_brain()

# ==============================
# --------- Interface ----------
# ==============================
if __name__ == "__main__":
    bot = Cleverbot()
    print("CLEVERBOT: Olá! Eu sou o Cleverbot. Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ").strip().lower()
        if user_input in ["sair", "tchau", "adeus"]:
            print("CLEVERBOT: Até mais! Foi bom conversar com você.")
            break

        response = bot.respond(user_input)

        if response:
            print(f"CLEVERBOT: {response}")
        else:
            print("CLEVERBOT: Não sei como responder a isso. O que eu deveria dizer?")
            new_response = input("Você: ").strip()
            bot.learn(user_input, new_response)
            print("CLEVERBOT: Entendido! Vou lembrar disso.")
