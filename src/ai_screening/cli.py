"""Command line: asks the questions and prints the result."""
from ai_screening.gates import (
    MAX_USE_CASES,
    MIN_USE_CASES,
    PASSED,
    QUESTIONS,
    check_gate,
    is_ready,
)


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
    company = input("Company name: ").strip()
    target = input("Target: what improves, by how much, by when? (e.g. invoice processing time from 12 to 8 minutes by 31 Dec 2026): ").strip()
    owner = input("Owner: the ONE person at the company responsible for reaching the target (name): ").strip()

    if not is_ready(target, owner):
        print("\nNOT READY: agree a measurable target and a named owner with the company first.")
        return

    results = []
    while len(results) < MAX_USE_CASES:
        name = input(f"\nUse case {len(results) + 1} (name, or Enter to finish): ").strip()
        if not name:
            break
        verdict, reason = screen()
        results.append((name, verdict, reason))

    if len(results) < MIN_USE_CASES:
        print(f"\nNote: you checked {len(results)} use cases. The method suggests {MIN_USE_CASES} to {MAX_USE_CASES}.")

    print(f"\n===== RESULT for {company} =====")
    print(f"Target: {target} | Owner: {owner}\n")
    for name, verdict, reason in results:
        print(f"{verdict:6} | {name:30} | {reason}")