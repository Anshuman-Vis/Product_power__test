"""
Indian Food Additives Database (INS/E-Numbers)
FSSAI Compliant
"""

ADDITIVES_DB = {
    "INS 102": {
        "name": "Tartrazine",
        "category": "Artificial Color",
        "purpose": "Yellow food coloring",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May cause allergic reactions, hyperactivity in children"
    },
    "INS 110": {
        "name": "Sunset Yellow FCF",
        "category": "Artificial Color",
        "purpose": "Orange-yellow coloring",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May cause hyperactivity, allergic reactions"
    },
    "INS 122": {
        "name": "Carmoisine",
        "category": "Artificial Color",
        "purpose": "Red coloring",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May trigger allergies"
    },
    "INS 124": {
        "name": "Ponceau 4R",
        "category": "Artificial Color",
        "purpose": "Red coloring",
        "risk_level": "High Concern",
        "regulatory_status": "Restricted",
        "concerns": "Linked to hyperactivity, banned in some countries"
    },
    "INS 129": {
        "name": "Allura Red AC",
        "category": "Artificial Color",
        "purpose": "Red coloring",
        "risk_level": "High Concern",
        "regulatory_status": "Permitted with limits",
        "concerns": "May cause hyperactivity in children"
    },
    "INS 133": {
        "name": "Brilliant Blue FCF",
        "category": "Artificial Color",
        "purpose": "Blue coloring",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "Generally safe in small amounts"
    },
    "INS 150d": {
        "name": "Caramel Color IV",
        "category": "Color",
        "purpose": "Brown coloring",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "May contain 4-MEI (potential carcinogen)"
    },
    "INS 160a": {
        "name": "Beta-Carotene",
        "category": "Natural Color",
        "purpose": "Orange coloring, Vitamin A source",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Generally safe, natural origin"
    },
    "INS 200": {
        "name": "Sorbic Acid",
        "category": "Preservative",
        "purpose": "Prevents mold and yeast",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Generally recognized as safe"
    },
    "INS 202": {
        "name": "Potassium Sorbate",
        "category": "Preservative",
        "purpose": "Prevents mold growth",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Safe in normal amounts"
    },
    "INS 211": {
        "name": "Sodium Benzoate",
        "category": "Preservative",
        "purpose": "Prevents bacterial growth",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May form benzene with vitamin C"
    },
    "INS 220": {
        "name": "Sulphur Dioxide",
        "category": "Preservative",
        "purpose": "Antioxidant, preservative",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May trigger asthma, allergies"
    },
    "INS 223": {
        "name": "Sodium Metabisulphite",
        "category": "Preservative",
        "purpose": "Antioxidant, preservative",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May cause allergic reactions in sensitive individuals"
    },
    "INS 250": {
        "name": "Sodium Nitrite",
        "category": "Preservative",
        "purpose": "Preserves meat, prevents botulism",
        "risk_level": "High Concern",
        "regulatory_status": "Restricted",
        "concerns": "May form carcinogenic nitrosamines"
    },
    "INS 251": {
        "name": "Sodium Nitrate",
        "category": "Preservative",
        "purpose": "Meat preservation",
        "risk_level": "High Concern",
        "regulatory_status": "Restricted",
        "concerns": "Potential carcinogen formation"
    },
    "INS 282": {
        "name": "Calcium Propionate",
        "category": "Preservative",
        "purpose": "Prevents mold in bread",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Generally safe"
    },
    "INS 296": {
        "name": "Malic Acid",
        "category": "Acidity Regulator",
        "purpose": "Tartness, pH control",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Naturally occurring, safe"
    },
    "INS 300": {
        "name": "Ascorbic Acid (Vitamin C)",
        "category": "Antioxidant",
        "purpose": "Preservative, vitamin",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Essential nutrient, safe"
    },
    "INS 322": {
        "name": "Lecithin",
        "category": "Emulsifier",
        "purpose": "Blends ingredients",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Natural, generally safe"
    },
    "INS 330": {
        "name": "Citric Acid",
        "category": "Acidity Regulator",
        "purpose": "Preservative, flavor",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Naturally occurring, safe"
    },
    "INS 339": {
        "name": "Sodium Phosphates",
        "category": "Acidity Regulator",
        "purpose": "Stabilizer, emulsifier",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "High intake may affect kidney function"
    },
    "INS 407": {
        "name": "Carrageenan",
        "category": "Thickener",
        "purpose": "Thickening, stabilizing",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "May cause digestive inflammation"
    },
    "INS 415": {
        "name": "Xanthan Gum",
        "category": "Thickener",
        "purpose": "Thickening, stabilizing",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Generally safe"
    },
    "INS 420": {
        "name": "Sorbitol",
        "category": "Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "May cause digestive issues in large amounts"
    },
    "INS 466": {
        "name": "Carboxymethyl Cellulose",
        "category": "Thickener",
        "purpose": "Thickening, stabilizing",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Generally safe"
    },
    "INS 471": {
        "name": "Mono & Diglycerides",
        "category": "Emulsifier",
        "purpose": "Blending fats and water",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "May contain trans fats"
    },
    "INS 500": {
        "name": "Sodium Carbonate",
        "category": "Acidity Regulator",
        "purpose": "Raising agent",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Safe in food amounts"
    },
    "INS 503": {
        "name": "Ammonium Carbonate",
        "category": "Raising Agent",
        "purpose": "Leavening",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Safe"
    },
    "INS 575": {
        "name": "Glucono Delta-Lactone",
        "category": "Acidity Regulator",
        "purpose": "pH control",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Safe"
    },
    "INS 621": {
        "name": "Monosodium Glutamate (MSG)",
        "category": "Flavor Enhancer",
        "purpose": "Enhances umami flavor",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "May cause headaches in sensitive individuals"
    },
    "INS 627": {
        "name": "Disodium Guanylate",
        "category": "Flavor Enhancer",
        "purpose": "Flavor enhancement",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "Often used with MSG"
    },
    "INS 631": {
        "name": "Disodium Inosinate",
        "category": "Flavor Enhancer",
        "purpose": "Flavor enhancement",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "May not be suitable for vegetarians"
    },
    "INS 635": {
        "name": "Disodium Ribonucleotides",
        "category": "Flavor Enhancer",
        "purpose": "Flavor enhancement",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "Used with MSG"
    },
    "INS 950": {
        "name": "Acesulfame Potassium",
        "category": "Artificial Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "Long-term effects debated"
    },
    "INS 951": {
        "name": "Aspartame",
        "category": "Artificial Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "High Concern",
        "regulatory_status": "Permitted with limits",
        "concerns": "Not safe for PKU patients, debated safety"
    },
    "INS 952": {
        "name": "Cyclamate",
        "category": "Artificial Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "High Concern",
        "regulatory_status": "Restricted",
        "concerns": "Banned in some countries"
    },
    "INS 954": {
        "name": "Saccharin",
        "category": "Artificial Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted with limits",
        "concerns": "Historical cancer concerns (now disputed)"
    },
    "INS 955": {
        "name": "Sucralose",
        "category": "Artificial Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "Moderate",
        "regulatory_status": "Permitted",
        "concerns": "Generally considered safe"
    },
    "INS 960": {
        "name": "Steviol Glycosides (Stevia)",
        "category": "Natural Sweetener",
        "purpose": "Sugar substitute",
        "risk_level": "Safe",
        "regulatory_status": "Permitted",
        "concerns": "Natural origin, generally safe"
    },
}

# Categories for classification
ADDITIVE_CATEGORIES = {
    "Artificial Color": ["INS 102", "INS 110", "INS 122", "INS 124", "INS 129", "INS 133"],
    "Preservative": ["INS 200", "INS 202", "INS 211", "INS 220", "INS 223", "INS 250", "INS 251", "INS 282"],
    "Flavor Enhancer": ["INS 621", "INS 627", "INS 631", "INS 635"],
    "Artificial Sweetener": ["INS 950", "INS 951", "INS 952", "INS 954", "INS 955"],
    "Emulsifier": ["INS 322", "INS 471"],
    "Thickener": ["INS 407", "INS 415", "INS 466"],
}

# Risk level colors
RISK_COLORS = {
    "Safe": "#10b981",
    "Moderate": "#f59e0b",
    "High Concern": "#ef4444"
}

def get_additive_info(ins_number):
    """Get additive information by INS number"""
    ins_number = ins_number.upper().strip()
    if not ins_number.startswith("INS"):
        ins_number = f"INS {ins_number}"
    return ADDITIVES_DB.get(ins_number, None)

def find_additives_in_text(text):
    """Find all additives mentioned in text"""
    import re
    found = []
    
    # Pattern for INS numbers
    pattern = r'INS\s*(\d+[a-z]?)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    for match in matches:
        ins_key = f"INS {match}"
        info = ADDITIVES_DB.get(ins_key)
        if info:
            found.append({
                "ins": ins_key,
                **info
            })
    
    return found