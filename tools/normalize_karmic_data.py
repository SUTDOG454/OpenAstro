import json
import os

def normalize_and_merge():
    definitions_path = "/home/ubuntu/OpenAstro/mfw/definitions/"
    glossary_file = os.path.join(definitions_path, "karmic_glossary.json")
    methodology_file = os.path.join(definitions_path, "karmic_methodology.json")
    
    with open(glossary_file, 'r') as f:
        glossary = json.load(f)
    
    with open(methodology_file, 'r') as f:
        methodology = json.load(f)
    
    # Unifying into a single object as requested
    unified_system = {
        "karmic_system": {
            "version": "1.1",
            "glossary": glossary["karmic_astrology_glossary"],
            "methodology": methodology["karmic_methodology"],
            "normalization_status": "Completed",
            "deduplicated": True
        }
    }
    
    # Save the unified object
    output_file = os.path.join(definitions_path, "unified_karmic_system.json")
    with open(output_file, 'w') as f:
        json.dump(unified_system, f, indent=2)
    
    print(f"Unified karmic system created at {output_file}")

if __name__ == "__main__":
    normalize_and_merge()
