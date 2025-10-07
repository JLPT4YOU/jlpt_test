#!/usr/bin/env python3
"""
Script to update part classification in all JLPT exam JSON files
Version 2.0 - Updated mapping based on new requirements
"""

import json
import os
from pathlib import Path

# Updated MONDAI to PART mapping for each level
MONDAI_PART_MAPPING = {
    "N1": {
        "vocabulary": list(range(1, 5)),    # Mondai 1-4
        "grammar": list(range(5, 8)),       # Mondai 5-7
        "reading": list(range(8, 14)),      # Mondai 8-13
        "listening": list(range(14, 100))   # Mondai 14-last
    },
    "N2": {
        "vocabulary": list(range(1, 7)),    # Mondai 1-6
        "grammar": list(range(7, 10)),      # Mondai 7-9
        "reading": list(range(10, 15)),     # Mondai 10-14
        "listening": list(range(15, 100))   # Mondai 15-last
    },
    "N3": {
        "vocabulary": list(range(1, 6)),    # Mondai 1-5
        "grammar": list(range(6, 9)),       # Mondai 6-8
        "reading": list(range(9, 13)),      # Mondai 9-12
        "listening": list(range(13, 100))   # Mondai 13-last
    },
    "N4": {
        "vocabulary": list(range(1, 6)),    # Mondai 1-5
        "grammar": list(range(6, 9)),       # Mondai 6-8
        "reading": list(range(9, 12)),      # Mondai 9-11
        "listening": list(range(12, 100))   # Mondai 12-last
    },
    "N5": {
        "vocabulary": list(range(1, 5)),    # Mondai 1-4
        "grammar": list(range(5, 8)),       # Mondai 5-7
        "reading": list(range(8, 11)),      # Mondai 8-10
        "listening": list(range(11, 100))   # Mondai 11-last
    }
}


def get_part_from_mondai(level: str, mondai: int) -> str:
    """
    Determine the part (vocabulary, grammar, reading, listening) 
    based on level and mondai number.
    
    Args:
        level: JLPT level (N1, N2, N3, N4, N5)
        mondai: Mondai number
        
    Returns:
        Part name: 'vocabulary', 'grammar', 'reading', or 'listening'
    """
    mapping = MONDAI_PART_MAPPING.get(level)
    
    if not mapping:
        raise ValueError(f"Unknown level: {level}")
    
    # Check each part
    if mondai in mapping["vocabulary"]:
        return "vocabulary"
    elif mondai in mapping["grammar"]:
        return "grammar"
    elif mondai in mapping["reading"]:
        return "reading"
    elif mondai in mapping["listening"]:
        return "listening"
    else:
        raise ValueError(f"Mondai {mondai} not mapped for level {level}")


def update_exam_file(file_path: Path) -> bool:
    """
    Update a single exam JSON file with correct part classification.
    
    Args:
        file_path: Path to the exam JSON file
        
    Returns:
        True if file was updated, False otherwise
    """
    try:
        # Read the exam file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get level from data
        level = data.get('level')
        if isinstance(level, int):
            level = f"N{level}"
        elif not level or not level.startswith('N'):
            print(f"⚠️  Invalid level in {file_path.name}")
            return False
        
        # Update each section with correct part
        updated = False
        if 'sections' in data:
            for section in data['sections']:
                mondai = section.get('mondai')
                if mondai:
                    try:
                        correct_part = get_part_from_mondai(level, mondai)
                        if section.get('part') != correct_part:
                            section['part'] = correct_part
                            updated = True
                    except ValueError as e:
                        print(f"⚠️  Error in {file_path.name}: {e}")
                        return False
        
        # Write back if updated
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function to update all exam files."""
    
    # Base directory for exams
    base_dir = Path(__file__).parent / "exams"
    
    if not base_dir.exists():
        print(f"❌ Exams directory not found: {base_dir}")
        return
    
    print("🚀 Starting exam files update (Version 2.0)")
    print("=" * 60)
    
    # Statistics
    stats = {
        "N1": {"total": 0, "updated": 0},
        "N2": {"total": 0, "updated": 0},
        "N3": {"total": 0, "updated": 0},
        "N4": {"total": 0, "updated": 0},
        "N5": {"total": 0, "updated": 0}
    }
    
    # Process each level
    for level in ["N1", "N2", "N3", "N4", "N5"]:
        level_dir = base_dir / level
        
        if not level_dir.exists():
            continue
        
        print(f"\n📂 Processing {level}...")
        
        # Find all JSON files recursively
        json_files = list(level_dir.rglob("*.json"))
        
        for json_file in json_files:
            stats[level]["total"] += 1
            if update_exam_file(json_file):
                stats[level]["updated"] += 1
                print(f"  ✅ Updated: {json_file.name}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 UPDATE SUMMARY")
    print("=" * 60)
    
    total_files = 0
    total_updated = 0
    
    for level, data in stats.items():
        total_files += data["total"]
        total_updated += data["updated"]
        if data["total"] > 0:
            print(f"{level}: {data['updated']}/{data['total']} files updated")
    
    print("-" * 60)
    print(f"TOTAL: {total_updated}/{total_files} files updated")
    print("=" * 60)
    
    if total_updated > 0:
        print("✅ Update completed successfully!")
    else:
        print("ℹ️  No files needed updating (already up to date)")


if __name__ == "__main__":
    main()
