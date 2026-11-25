from itertools import combinations


def generate_association_rules(freq_itemsets, num_transactions, min_confidence=0.5):
    rules = []
  
    support = {frozenset(k): v for k, v in freq_itemsets.items()}
    #frozenset instead of tuple so the order is not important

    for itemset, sup_ab in freq_itemsets.items():
        if len(itemset) < 2:
            continue

        for r in range(1, len(itemset)):
            for ant in combinations(itemset, r):
                antecedent = frozenset(ant)
                consequent = frozenset(itemset) - antecedent

                if antecedent in support and consequent in support:
                    confidence = sup_ab / support[antecedent]
                    support_b = support[consequent] / num_transactions  
                    if confidence >= min_confidence:
                        lift = round(confidence / support_b, 4)
                        if lift > 1:
                            strength = "positive"
                        elif lift == 1:
                            strength = "independent"
                        else:
                            strength = "negative"
                        rules.append({
                            "rule": f"{', '.join(sorted(antecedent))} -> {', '.join(sorted(consequent))}",
                            "support": round(sup_ab / num_transactions, 4),
                            "confidence": round(confidence, 4),
                            "lift": lift,
                            "strength": strength
                        })

    rules.sort(key=lambda x: x["confidence"], reverse=True)

    return rules