"""
Food Risk Score Calculator
"""

def calculate_food_risk_score(nutrition_data, additives_found):
    """
    Calculate Food Risk Score (0-100)
    Higher score = Higher risk
    
    Returns score and breakdown
    """
    score = 0
    breakdown = {}
    
    macro = nutrition_data.get('nutrition', {}) if nutrition_data else {}
    
    # Helper to extract numeric value
    def get_num(value):
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            import re
            nums = re.findall(r'[\d.]+', value)
            return float(nums[0]) if nums else 0
        return 0
    
    # 1. Sugar content (max 20 points)
    sugar = get_num(macro.get('sugar', 0))
    sugar_score = min(sugar * 1.5, 20)
    score += sugar_score
    breakdown['sugar'] = round(sugar_score, 1)
    
    # 2. Sodium content (max 20 points)
    sodium = get_num(macro.get('sodium', 0))
    sodium_score = min(sodium / 50, 20)
    score += sodium_score
    breakdown['sodium'] = round(sodium_score, 1)
    
    # 3. Saturated fat (max 15 points)
    sat_fat = get_num(macro.get('saturated_fat', 0))
    sat_fat_score = min(sat_fat * 2, 15)
    score += sat_fat_score
    breakdown['saturated_fat'] = round(sat_fat_score, 1)
    
    # 4. Artificial additives (max 25 points)
    additive_score = 0
    for additive in additives_found:
        risk = additive.get('risk_level', 'Safe')
        if risk == 'High Concern':
            additive_score += 8
        elif risk == 'Moderate':
            additive_score += 4
        elif risk == 'Safe':
            additive_score += 1
    
    additive_score = min(additive_score, 25)
    score += additive_score
    breakdown['additives'] = round(additive_score, 1)
    
    # 5. Preservatives (max 10 points)
    preservative_count = sum(1 for a in additives_found 
                            if a.get('category') == 'Preservative')
    preservative_score = min(preservative_count * 3, 10)
    score += preservative_score
    breakdown['preservatives'] = round(preservative_score, 1)
    
    # 6. Ultra-processed indicators (max 10 points)
    artificial_count = sum(1 for a in additives_found 
                          if 'Artificial' in a.get('category', ''))
    processed_score = min(artificial_count * 3, 10)
    score += processed_score
    breakdown['ultra_processed'] = round(processed_score, 1)
    
    final_score = min(int(score), 100)
    
    return final_score, breakdown

def get_risk_category(score):
    """Get risk category from score"""
    if score <= 20:
        return "Excellent", "#10b981", "🟢"
    elif score <= 40:
        return "Good", "#84cc16", "🟢"
    elif score <= 60:
        return "Moderate", "#f59e0b", "🟡"
    elif score <= 80:
        return "High Risk", "#f97316", "🟠"
    else:
        return "Very High Risk", "#ef4444", "🔴"