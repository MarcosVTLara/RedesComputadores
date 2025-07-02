# tui_exemplo.py
import questionary

nome = questionary.text("Qual é seu nome?").ask()
linguagem = questionary.select(
    "Qual linguagem você prefere?",
    choices=["Python", "JavaScript", "C++", "Outro"]
).ask()

print(f"\nOlá, {nome}! Você escolheu: {linguagem}")
