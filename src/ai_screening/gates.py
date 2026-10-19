"""The six gates. Pure rules: no input, no printing."""

# (key, question text, allowed answers), in the order they are checked
QUESTIONS = [
    ("fix", "1. Is there a simple fix that does not need AI? A rule, a process change, or a feature of software they already own (e.g. invoices already arrive in a format their accounting software can import).",
     {"y": "yes, a simple fix exists", "n": "no, nothing simple would work", "u": "don't know yet"}),
    ("data", "2. Does the data this needs (text, documents, records) exist in digital form, in one place, and is it mostly correct?",
     {"y": "yes, all three", "n": "no, at least one is missing", "u": "don't know yet"}),
    ("cost", "3. Do they know what this task costs per year (hours x hourly cost, or money lost)?",
     {"y": "known, and clearly more than a pilot would cost", "s": "known, but small", "u": "not known"}),
    ("check", "4. If the AI gets an output wrong, is the damage small, or will a person check every output before it is used?",
     {"y": "yes, at least one of the two is true", "n": "no, the damage would be big and nobody checks", "u": "don't know yet"}),
    ("blocker", "5. Does a law, contract or safety rule forbid this, with no way around it? (e.g. customer data must not leave the company)",
     {"y": "yes, forbidden, no way around", "n": "no, nothing forbids it, or there is a workaround", "u": "don't know yet"}),
    ("owner", "6. Is ONE named person responsible for this use case, and do the future users want it?",
     {"y": "yes, both", "n": "no, the person or the users are missing", "u": "don't know yet"}),
]

# Answers that stop the screening: (gate key, answer) -> (verdict, reason)
STOPS = {
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