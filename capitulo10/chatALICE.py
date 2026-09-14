import aiml
import os

# Cria uma instância do kernel AIML
alice = aiml.Kernel()

# Verifica se existe um arquivo de aprendizado salvo
if os.path.isfile("std_brain.brn"):
    alice.bootstrap(brainFile="std_brain.brn")

else:
    # Carrega os arquivos AIML
    alice.learn("base.aiml")
    # Salva o “cérebro” compilado para uso futuro
    alice.saveBrain("std_brain.brn")

print("ALICE: Olá! Eu sou a ALICE, sua assistente virtual. Digite 'sair' para encerrar.\n")

# Loop de conversa
while True:
    user_input = input("Você: ").upper()
    if user_input in ["SAIR", "TCHAU"]:
        print("ALICE: Até mais! :)")
        break
    resposta = alice.respond(user_input)
    print(f"ALICE: {resposta}")
