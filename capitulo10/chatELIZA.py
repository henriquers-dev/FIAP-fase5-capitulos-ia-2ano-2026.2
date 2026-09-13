import re
import random

# Regras de substituição: palavra-chave -> respostas possíveis
regras = {
    r"eu preciso de (.*)": [
        "Por que você precisa de {0}?",
        "Você realmente acha que precisa de {0}?",
        "Ter {0} ajudaria você de alguma forma?"
    ],
    r"eu sinto (.*)": [
        "Com que frequência você sente {0}?",
        "Por que você sente {0}?",
        "Você costuma se sentir {0} há muito tempo?"
    ],
    r"estou (.*)": [
        "Por que você está {0}?",
        "Você acredita que estar {0} é algo bom?",
        "Há algo que o faz se sentir {0}?"
    ],
    r"olá|oi": [
        "Olá! Como você está se sentindo hoje?",
        "Oi! Em que posso ajudar você?"
    ],
    r".*": [  # resposta padrão
        "Conte-me mais sobre isso.",
        "Por favor, continue.",
        "Você pode explicar melhor?"
    ]
}

def eliza_responder(frase):
    frase = frase.lower()
    for padrao, respostas in regras.items():
        match = re.match(padrao, frase)
        if match:
            resposta = random.choice(respostas)
            # Substitui grupos capturados na resposta
            return resposta.format(*match.groups())
    return "Interessante... fale mais sobre isso."

# Simulação de conversa
print("ELIZA: Olá! Eu sou a ELIZA. Como você está se sentindo hoje?")

while True:
    entrada = input("Você: ")
    if entrada.lower() in ["sair", "tchau"]:
        print("ELIZA: Até mais! Cuide-se.")
        break
    resposta = eliza_responder(entrada)
    print(f"ELIZA: {resposta}")
