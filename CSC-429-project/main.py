from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def collect_initial_facts():
    facts = []
    if input("Is portability important? (y/n): ").lower().startswith("y"):
        facts.append("portable")
    if input("Do you need long battery life? (y/n): ").lower().startswith("y"):
        facts.append("long_battery")

    budget = input("What is your budget? (low/medium/high): ").strip().lower()
    if budget == "low":
        facts.append("budget_low")
    elif budget == "medium":
        facts.append("budget_medium")
    elif budget == "high":
        facts.append("budget_high")

    use = input("What is your primary use? (office/gaming/creative/other): ").strip().lower()
    if use == "office":
        facts.append("office_only")
    elif use == "gaming":
        facts.append("gaming")
    elif use == "creative":
        facts.append("creative_work")

    if input("Do you prefer a larger screen (15\" or bigger)? (y/n): ").lower().startswith("y"):
        facts.append("large_screen")

    if input("Do you travel often with your laptop? (y/n): ").lower().startswith("y"):
        facts.append("travel_often")

    os_pref = input("Do you have a preferred OS? (macos/linux/none): ").strip().lower()
    if os_pref == "macos":
        facts.append("pref_os_macos")
    elif os_pref == "linux":
        facts.append("pref_os_linux")
    
    if input("Do you need AI/ML acceleration (for deep learning or similar)? (y/n): ").lower().startswith("y"):
        facts.append("needs_ai_accel")

    return facts

def main():
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)
    initial_facts = collect_initial_facts()

    engine.assert_facts(initial_facts)
    engine.run()

    results = engine.conclusions()
    recommendations = results.get("recommendations", [])
    specs = results.get("specs", [])

    print()

    if not recommendations:
        print("=> Recommendation: none")
    else:
        for rec in recommendations:
            label = rec.split(":", 1)[1] if ":" in rec else rec
            print(f"=> Recommendation: {label}")

            fired = next(
                (step for step in engine.trace if step["consequent"] == rec),
                None
            )
            if fired:
                print(f"=> Explanation: derived from rule '{fired['rule_name']}'")
            
    if specs:
        print("\nSuggested specs:")
        for s in specs:
            spec_label = s.split(":", 1)[1] if ":" in s else s
            print(f"- {spec_label}")

if __name__ == "__main__":
    main()

