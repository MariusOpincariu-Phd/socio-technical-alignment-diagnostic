import pandas as pd

# --- RESEARCH PROTOTYPE: Sycophancy Detection & Institutional Integrity ---

def calculate_sycophancy_probability(entry, impact_score):
    """
    Calculates the probability that the formal positive sentiment is non-genuine.
    Sycophancy is high when Formal Sentiment is high but Informal signals are dissonant.
    """
    # If formal sentiment is high (>0.7) but informal is low (<0), probability increases.
    if entry['formal_sentiment'] > 0.6 and entry['informal_mixed_sentiment'] < 0:
        base_prob = abs(entry['formal_sentiment'] - entry['informal_mixed_sentiment']) / 2
        
        # Institutional breach or high irony confirms the lack of genuine alignment
        modifier = 1.2 if entry['formal_contains_symbols'] else 1.0
        irony_mod = 1.3 if entry['informal_irony_score'] > 0.6 else 1.0
        
        prob = base_prob * modifier * irony_mod
        return min(round(prob * 100, 2), 100.0) # Cap at 100%
    return 0.0

def calculate_societal_impact(entry):
    dissonance_gap = abs(entry['formal_sentiment'] - entry['informal_mixed_sentiment'])
    
    # Trigger for breaking the "Text-Only" Institutional Norm
    breach_multiplier = 3.5 if entry['formal_contains_symbols'] else 1.0
    
    # Power Differential Mediation (Irony validated by group)
    pdm_factor = 1.8 if (entry['informal_irony_score'] > 0.5 and entry['new_subthreads'] > 5) else 1.0
            
    # Final Formula factoring in Cognitive Load
    final_score = (dissonance_gap * (1 + entry['cognitive_load_factor'])) * breach_multiplier * pdm_factor
    return round(final_score, 3)

# 1. DATASET
data = [
    {
        'topic': 'High-Stakes Evaluation',
        'formal_sentiment': 0.95,          # Apparent "perfect" compliance
        'formal_contains_symbols': True,   # BREACH: Symbols used despite norms
        'informal_mixed_sentiment': -0.8,  # Real distress in informal channels
        'informal_irony_score': 0.9,       # High irony (Power Mediation)
        'cognitive_load_factor': 0.9,
        'new_subthreads': 15,
        'upvote_density': 0.9
    },
    {
        'topic': 'Collaborative Workshop',
        'formal_sentiment': 0.5,           # Genuine, moderate alignment
        'formal_contains_symbols': False,
        'informal_mixed_sentiment': 0.45,
        'informal_irony_score': 0.1,
        'cognitive_load_factor': 0.2,
        'new_subthreads': 0,
        'upvote_density': 0.1
    }
]

# 2. EXECUTION & REPORTING
print(f"{'RESEARCH TOPIC':<25} | {'IMPACT':<8} | {'SYCOPHANCY %':<15} | {'STATUS'}")
print("-" * 80)

for entry in data:
    impact = calculate_societal_impact(entry)
    syc_prob = calculate_sycophancy_probability(entry, impact)
    
    status = "CRITICAL" if syc_prob > 50 else "NOMINAL"
        
    print(f"{entry['topic']:<25} | {impact:<8} | {syc_prob:<15}% | {status}")
    
    if syc_prob > 50:
        print(f"   [Alert]: High Sycophancy Risk. Formal compliance masks significant institutional friction.")
        print(f"   [Action]: Triggering Constitutional Re-routing to address Power Differential.")
