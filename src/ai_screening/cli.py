"""Command line: asks the questions and prints the result."""
from ai_screening.gates import (
    MAX_USE_CASES,
    MIN_USE_CASES,
    PASSED,
    QUESTIONS,
    check_gate,
    is_ready,
)
from ai_screening.library import (
    list_industries,
    load_use_cases,
    parse_numbers,
    use_cases_for,
)


def ask(question, answers):
    """Show the question and what each answer means. Ask until the answer is valid."""
    print(question)
    for key, meaning in answers.items():
        print(f"   {key} = {meaning}")
    while True:
        answer = input("   Your answer: ").strip().lower()
        if answer in answers:
            return answer
        print("   Please answer with one of:", ", ".join(answers))


def pick(prompt, count):
    """Ask for numbers like 1,4,7 until valid. Returns 0-based indexes."""
    while True:
        indexes = parse_numbers(input(prompt), count)
        if indexes is not None:
            return indexes
        print(f"Enter numbers from 1 to {count}, separated by commas, no repeats.")


def screen():
    """Ask the gates in order. The first gate that fails decides the verdict."""
    for key, text, answers in QUESTIONS:
        stop = check_gate(key, ask(text, answers))
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

    rows = load_use_cases()
    industries = list_industries(rows)
    print("\nIndustries:")
    for number, name in enumerate(industries, 1):
        print(f"  {number:2}. {name}")
    industry = industries[pick("Industry number: ", len(industries))[0]]

    options = use_cases_for(rows, industry)
    print(f"\nUse cases for {industry} (plus cross-industry):")
    for number, row in enumerate(options, 1):
        print(f"  {number:2}. [{row['Department']}] {row['Specific use case']}")
    chosen = [options[i] for i in pick(
        f"Choose {MIN_USE_CASES} to {MAX_USE_CASES} (e.g. 1,4,7): ", len(options))]

    if not MIN_USE_CASES <= len(chosen) <= MAX_USE_CASES:
        print(f"\nNote: you chose {len(chosen)} use cases. The method suggests {MIN_USE_CASES} to {MAX_USE_CASES}.")

    results = []
    for row in chosen:
        print(f"\n--- {row['Specific use case']} ({row['Department']}) ---")
        print(f"Signs you should have heard: {row['How to recognize it (signals in the interview)']}")
        print(f"Not suitable when: {row['When NOT to prescribe']}")
        verdict, reason = screen()
        results.append((row["Specific use case"], verdict, reason))

    print(f"\n===== RESULT for {company} ({industry}) =====")
    print(f"Target: {target} | Owner: {owner}\n")
    for name, verdict, reason in results:
        print(f"{verdict:6} | {name:45} | {reason}")