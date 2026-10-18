def ask(question, options):
    """Ask until the answer is one of the allowed options."""
    while True:
        answer = input(f"{question} {options}: ").strip().lower()
        if answer in options:
            return answer
        print("Please answer with one of:", options)


def screen():
    """Six gates, in order. The first gate that fails decides the verdict."""
    if ask("1. Could a simple fix solve it?", ["y", "n"]) == "y":
        return "NO_AI", "A simpler fix exists"

    if ask("2. Is the data available and in good condition? (u = unknown)", ["y", "n", "u"]) != "y":
        return "LATER", "Data not ready or unknown"

    cost = ask("3. Yearly cost known and big enough? (y = yes, s = known but small, u = unknown)", ["y", "s", "u"])
    if cost == "u":
        return "LATER", "Yearly cost unknown"
    if cost == "s":
        return "PARK", "Cost too small for a project"

    if ask("4. Is a wrong output affordable, OR can a human check it?", ["y", "n"]) == "n":
        return "NO_AI", "Errors unaffordable and cannot be checked"

    if ask("5. Is there a legal/safety blocker that cannot be mitigated?", ["y", "n"]) == "y":
        return "NO_AI", "Unmitigable legal or safety blocker"

    if ask("6. Is there a named owner AND are users willing?", ["y", "n"]) == "n":
        return "LATER", "No owner or users not on board"

    return "DO", "Passed all six gates"


results = []
while True:
    name = input("\nUse case to check (empty line to finish): ").strip()
    if not name:
        break
    verdict, reason = screen()
    results.append((name, verdict, reason))

print("\n===== RESULT =====")
if not results:
    print("No use cases entered.")
for name, verdict, reason in results:
    print(f"{verdict:6} | {name:30} | {reason}")