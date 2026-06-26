#!/usr/bin/env python3
"""
ProductPower Runner
Usage: python run.py [image_path]
"""

import sys
import os
from productpower import llm_nutritionist, analyze_food_label

def main():
    print("="*60)
    print("🥗 PRODUCTPOWER - Nutrition Analyzer")
    print("="*60)
    
    # Get image path
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        img_path = "images/food_label.jpg"
    
    # Check if exists
    if not os.path.exists(img_path):
        print(f"\n❌ Image not found: {img_path}")
        print("\nUsage:")
        print("  python run.py                    # Use default image")
        print("  python run.py path/to/image.jpg  # Use custom image")
        return
    
    # Run analysis
    print(f"\n📸 Image: {img_path}\n")
    
    # Quick mode
    if "--quick" in sys.argv:
        analyze_food_label(img_path)
    
    # Batch mode
    elif "--batch" in sys.argv:
        folder = sys.argv[2] if len(sys.argv) > 2 else "images"
        analyzer = llm_nutritionist()
        analyzer.batch_analyze(folder)
    
    # Normal mode
    else:
        analyzer = llm_nutritionist()
        analyzer.analyze(img_path, show_image=True, verbose=False)
        print(analyzer.get_summary())
        
        # Ask to save
        save = input("\n💾 Save results? (y/n): ").lower()
        if save == 'y':
            analyzer.save()
    
    print("\n✅ Done!\n")

if __name__ == "__main__":
    main()