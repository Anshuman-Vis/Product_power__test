"""
FSSAI License Number Validator
"""

import re

def extract_fssai_number(text):
    """Extract FSSAI license number from text"""
    # FSSAI numbers are 14 digits
    patterns = [
        r'FSSAI\s*[:.]?\s*(\d{14})',
        r'Lic\s*No\s*[:.]?\s*(\d{14})',
        r'License\s*[:.]?\s*(\d{14})',
        r'\b(\d{14})\b'  # Any 14-digit number
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def validate_fssai(license_number):
    """
    Validate FSSAI license number
    
    Returns dict with validation results
    """
    if not license_number:
        return {
            "valid": False,
            "number": None,
            "message": "No FSSAI number found",
            "details": {}
        }
    
    # Clean the number
    license_number = str(license_number).strip().replace(" ", "")
    
    result = {
        "number": license_number,
        "valid": True,
        "message": "Valid FSSAI License",
        "details": {}
    }
    
    # Check 1: Length (must be 14 digits)
    if len(license_number) != 14:
        result["valid"] = False
        result["message"] = "Potentially Invalid License"
        result["details"]["length_check"] = f"Failed: {len(license_number)} digits (expected 14)"
    else:
        result["details"]["length_check"] = "Passed: 14 digits"
    
    # Check 2: Numeric validation
    if not license_number.isdigit():
        result["valid"] = False
        result["message"] = "Potentially Invalid License"
        result["details"]["numeric_check"] = "Failed: Contains non-numeric characters"
    else:
        result["details"]["numeric_check"] = "Passed: All numeric"
    
    # Check 3: First digit validation (1 or 2 for India)
    if license_number and license_number[0] in ['1', '2']:
        result["details"]["prefix_check"] = "Passed: Valid prefix"
    else:
        result["details"]["prefix_check"] = "Warning: Unusual prefix"
    
    # Check 4: State code (digits 2-3)
    if len(license_number) >= 3:
        state_code = license_number[1:3]
        result["details"]["state_code"] = f"State Code: {state_code}"
    
    return result