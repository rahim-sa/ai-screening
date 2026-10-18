"""The six gates. Pure rules: no input, no printing."""

# (key, question text, allowed answers), in the order they are checked
QUESTIONS = [
    ("fix", "1. Ask: could a rule, a process change or a feature of software they already own solve this? (e.g. invoices already arrive in a format their accounting software can import). y = yes, a simple fix exists, n = no, u = they don't know", ["y", "n", "u"]),
    ("data", "2. Ask: does the data/text/documents for this exist in digital form, in one place, and is it mostly correct? y = yes, n = no, u = they don't know", ["y", "n", "u"]),
    ("cost", "3. Ask: how many hours or how much money per year does this task cost, and is that number known? y = known and big enough for a project, s = known but small, u = not known", ["y", "s", "u"]),
    ("check", "4. Ask: if the AI gets one output wrong, is the damage small, OR will a person check every output before it is used? y = yes (either one), n = no (big damage and nobody checks), u = they don't know", ["y", "n", "u"]),
    ("blocker", "5. Ask: does a law, contract or safety rule forbid this, with no way around it? (e.g. customer data must not leave the company). y = blocker exists, n = none, u = they don't know", ["y", "n", "u"]),
    ("owner", "6. Ask: is ONE named person responsible for this use case, AND do the future users want it? y = both, n = not both, u = they don't know", ["y", "n", "u"]),
]

# Answers that stop the screening: (gate key, answer) -> (verdict, reason)
#STOPS = {
    ("fix", "y"): ("NO_AI", "A simpler fix exists"),
    ("fix", "u"): ("LATER", "Simple fix unknown: ask the person who does the work, and IT"),
    ("data", "n"): ("LATER", "Data not ready: ask IT what exists and fix its quality"),
    ("data", "u"): ("LATER", "Data availability unknown: ask IT"),
    ("cost", "u"): ("LATER", "Yearly cost unknown: ask the manager or finance"),
    ("cost", "s"): ("PARK", "Cost too small for a project"),
    ("check", "n"): ("NO_AI", "Errors unaffordable and cannot be checked"),
    ("check", "u"): ("LATER", "Cost of errors unknown: ask the process manager"),
    ("blocker", "y"): ("NO_AI", "Unmitigable legal or safety blocker"),
    ("blocker", "u"): ("LATER", "Legal/safety status unknown: ask legal or compliance"),
    ("owner", "n"): ("LATER", "No owner or users not on board: name an owner, involve the users"),
    ("owner", "u"): ("LATER", "Owner/users unknown: ask the executive sponsor"),
}

PASSED = ("DO", "Passed all six gates")


def check_gate(key, answer):
    """Return (verdict, reason) if this answer stops the screening, else None."""
    return STOPS.get((key, answer))

MIN_USE_CASES = 3
MAX_USE_CASES = 8


def is_ready(target, owner):
    """The company is ready only with a measurable target and a named owner."""
    return bool(target.strip()) and bool(owner.strip())