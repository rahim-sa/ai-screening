"""Command line: asks the questions and prints the result."""
from ai_screening.gates import PASSED, QUESTIONS, check_gate


def ask(question, options):
    """Ask until the answer is one of the allowed options."""
    while True:
        answer = input(f"{question} {options}: ").strip().lower()
        if answer in options:
            return answer
        print("Please answer with one of:", options)


def screen():
    """Ask the gates in order. The first gate that fails decides the verdict."""
    for key, text, options in QUESTIONS:
        stop = check_gate(key, ask(text, options))
        if stop:
            return stop
    return PASSED


def main():
    results = []
    while True:
        name = input("\nName of the use case (e.g. Invoice entry), or Enter to finish: ").strip()
        if not name:
            break
        verdict, reason = screen()
        results.append((name, verdict, reason))

    print("\n===== RESULT =====")
    if not results:
        print("No use cases entered.")
    for name, verdict, reason in results:
        print(f"{verdict:6} | {name:30} | {reason}")