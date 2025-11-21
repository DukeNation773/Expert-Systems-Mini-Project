from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        if not all(a in self.facts for a in rule.antecedents):
            return False
        if rule.consequent in self.facts:
            return False

        return True

    def run(self) -> None:
        while True:
            applicable = [r for r in self.rules if self.can_fire(r)]
            if not applicable:
                break

            applicable.sort(key=lambda r: (-r.priority, r.name))

            rule = applicable[0]

            self.facts.add(rule.consequent)

            self.trace.append({
                "rule_name": rule.name,
                "antecedents": list(rule.antecedents),
                "consequent": rule.consequent,
                "priority": rule.priority,
            })

    def conclusions(self) -> Dict[str, List[str]]:
        recommendations: List[str] = []
        specs: List[str] = []
        other: List[str] = []

        for fact in self.facts:
            if fact.startswith("recommend:"):
                recommendations.append(fact)
            elif fact.startswith("spec:"):
                specs.append(fact)
            else:
                other.append(fact)
        return {
            "recommendations": sorted(recommendations),
            "specs": sorted(specs),
            "other": sorted(other),
        }
