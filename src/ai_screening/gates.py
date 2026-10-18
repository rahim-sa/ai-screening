"""The six gates. Pure rules: no input, no printing."""

# (key, question text, allowed answers), in the order they are checked
QUESTIONS = [
    ("fix", "1. Could a simple fix solve it?", ["y", "n"]),
    ("data", "2. Is the data available and in good condition? (u = unknown)", ["y", "n", "u"]),
    ("cost", "3. Yearly cost known and big enough? (y = yes, s = known but small, u = unknown)", ["y", "s", "u"]),
    ("check", "4. Is a wrong output affordable, OR can a human check it?", ["y", "n"]),
    ("blocker", "5. Is there a legal/safety blocker that cannot be mitigated?", ["y", "n"]),
    ("owner", "6. Is there a named owner AND are users willing?", ["y", "n"]),
]

# Answers that stop the screening: (gate key, answer) -> (verdict, reason)
STOPS = {
    ("fix", "y"): ("NO_AI", "A simpler fix exists"),
    ("data", "n"): ("LATER", "Data not ready"),
    ("data", "u"): ("LATER", "Data availability unknown"),
    ("cost", "u"): ("LATER", "Yearly cost unknown"),
    ("cost", "s"): ("PARK", "Cost too small for a project"),
    ("check", "n"): ("NO_AI", "Errors unaffordable and cannot be checked"),
    ("blocker", "y"): ("NO_AI", "Unmitigable legal or safety blocker"),
    ("owner", "n"): ("LATER", "No owner or users not on board"),
}

PASSED = ("DO", "Passed all six gates")


def check_gate(key, answer):
    """Return (verdict, reason) if this answer stops the screening, else None."""
    return STOPS.get((key, answer))