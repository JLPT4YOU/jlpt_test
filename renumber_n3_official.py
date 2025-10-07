#!/usr/bin/env python3
"""
Script to renumber mondai in N3 official exams
Remove duplicate mondai numbers, renumber sequentially from 1
"""

import json
from pathlib import Path

# Updated MONDAI to PART mapping for N3
MONDAI_PART_MAPPING_N3 = {
    "vocabulary": list(range(1, 6)),    # Mondai 1-5
    "grammar": list(range(6, 9)),       # Mondai 6-8
    "reading": list(range(9, 13)),      # Mondai 9-12
    "listening": list(range(13, 100))   # Mondai 13-last
}


def get_part_from_mondai(mondai: int) -> str:
    """Get part based on mondai number for N3"""
    if mondai in MONDAI_PART_MAPPING_N3["vocabulary"]:
        return "vocabulary"
    elif mondai in MONDAI_PART_MAPPING_N3["grammar"]:
        return "grammar"
    elif mondai in MONDAI_PART_MAPPING_N3["reading"]:
        return "reading"
    elif mondai in MONDAI_PART_MAPPING_N3["listening"]:
        return "listening"
    else:
        return "listening"  # Default for mondai > 12


def renumber_file(file_path: Path) -> bool:
    """Renumber mondai in a single N3 official file"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if it's N3
        level = data.get('level')
        if level != 3:
            return False
        
        # Renumber sections
        if 'sections' in data:
            for i, section in enumerate(data['sections'], start=1):
                section['mondai'] = i
                section['part'] = get_part_from_mondai(i)
        
        # Recalculate statistics
        stats = {}
        for section in data.get('sections', []):
            part = section.get('part')
            questions = section.get('questions', [])
            if part:
                stats[part] = stats.get(part, 0) + len(questions)
        
        data['statistics'] = stats
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function"""
    base_dir = Path(__file__).parent / "exams" / "N3" / "official"
    
    if not base_dir.exists():
        print(f"❌ N3 official directory not found: {base_dir}")
        return
    
    print("🚀 Starting N3 official files renumbering...")
    print("=" * 60)
    
    json_files = sorted(base_dir.glob("*.json"))
    
    updated_count = 0
    for json_file in json_files:
        if renumber_file(json_file):
            updated_count += 1
            print(f"  ✅ Renumbered: {json_file.name}")
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY: {updated_count}/{len(json_files)} files renumbered")
    print("=" * 60)
    
    if updated_count > 0:
        print("✅ Renumbering completed successfully!")
    else:
        print("ℹ️  No files were renumbered")


if __name__ == "__main__":
    main()
