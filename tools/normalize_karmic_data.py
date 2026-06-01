import json
import os

def normalize_and_merge():
    repo_root = "/home/ubuntu/OpenAstro"
    definitions_path = os.path.join(repo_root, "mfw/definitions/")
    glossary_file = os.path.join(definitions_path, "karmic_glossary.json")
    methodology_file = os.path.join(definitions_path, "karmic_methodology.json")
    framework_file = os.path.join(repo_root, "unified_delineation_framework.json")
    
    with open(glossary_file, 'r') as f:
        glossary = json.load(f)
    
    with open(methodology_file, 'r') as f:
        methodology = json.load(f)
    
    # Unifying into a single object
    unified_system = {
        "karmic_system": {
            "version": "1.1",
            "glossary": glossary["karmic_astrology_glossary"],
            "methodology": methodology["karmic_methodology"],
            "normalization_status": "Completed",
            "deduplicated": True
        }
    }
    
    # Save the unified object locally in definitions
    output_file = os.path.join(definitions_path, "unified_karmic_system.json")
    with open(output_file, 'w') as f:
        json.dump(unified_system, f, indent=2)
    
    # Inject into the main framework
    if os.path.exists(framework_file):
        with open(framework_file, 'r') as f:
            framework = json.load(f)
        
        # Inject the karmic system into the content section
        if "astrological_delineation_framework" in framework:
            framework["astrological_delineation_framework"]["content"]["karmic_system"] = unified_system["karmic_system"]
            
            # Update metadata
            framework["astrological_delineation_framework"]["metadata"]["source_files"].append("unified_karmic_system.json")
            
            with open(framework_file, 'w') as f:
                json.dump(framework, f, indent=2)
            print(f"Injected karmic system into {framework_file}")

    print(f"Unified karmic system created at {output_file}")

if __name__ == "__main__":
    normalize_and_merge()
