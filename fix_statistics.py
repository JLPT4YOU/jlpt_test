#!/usr/bin/env python3
"""
Script to recalculate and update statistics in all exam files
based on new part mapping
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Updated MONDAI to PART mapping
MONDAI_PART_MAPPING = {
    "N1": {
        "vocabulary": list(range(1, 5)),
        "grammar": list(range(5, 8)),
        "reading": list(range(8, 14)),
        "listening": list(range(14, 100))
    },
    "N2": {
        "vocabulary": list(range(1, 7)),
        "grammar": list(range(7, 10)),
        "reading": list(range(10, 15)),
        "listening": list(range(15, 100))
    },
    "N3": {
        "vocabulary": list(range(1, 6)),
        "grammar": list(range(6, 9)),
        "reading": list(range(9, 13)),
        "listening": list(range(13, 100))
    },
    "N4": {
        "vocabulary": list(range(1, 6)),
        "grammar": list(range(6, 9)),
        "reading": list(range(9, 12)),
        "listening": list(range(12, 100))
    },
    "N5": {
        "vocabulary": list(range(1, 5)),
        "grammar": list(range(5, 8)),
        "reading": list(range(8, 11)),
        "listening": list(range(11, 100))
    }
}


def recalculate_statistics(data):
    """Recalculate statistics based on actual questions in sections"""
    stats = defaultdict(int)
    
    if 'sections' in data:
        for section in data['sections']:
            part = section.get('part')
            questions = section.get('questions', [])
            if part and questions:
                stats[part] += len(questions)
    
    return dict(stats)


def update_file_statistics(file_path: Path) -> bool:
    """Update statistics in a single exam file"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Recalculate statistics
        new_stats = recalculate_statistics(data)
        
        # Check if statistics need updating
        old_stats = data.get('statistics', {})
        if old_stats != new_stats:
            data['statistics'] = new_stats
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function"""
    base_dir = Path(__file__).parent / "exams"
    
    if not base_dir.exists():
        print(f"❌ Exams directory not found: {base_dir}")
        return
    
    print("🚀 Starting statistics recalculation...")
    print("=" * 60)
    
    stats = {
        "N1": {"total": 0, "updated": 0},
        "N2": {"total": 0, "updated": 0},
        "N3": {"total": 0, "updated": 0},
        "N4": {"total": 0, "updated": 0},
        "N5": {"total": 0, "updated": 0}
    }
    
    for level in ["N1", "N2", "N3", "N4", "N5"]:
        level_dir = base_dir / level
        
        if not level_dir.exists():
            continue
        
        print(f"\n📂 Processing {level}...")
        
        json_files = list(level_dir.rglob("*.json"))
        
        for json_file in json_files:
            stats[level]["total"] += 1
            if update_file_statistics(json_file):
                stats[level]["updated"] += 1
                print(f"  ✅ Updated: {json_file.name}")
    
    # Summary
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
        print("✅ Statistics update completed successfully!")
    else:
        print("ℹ️  No files needed updating")


if __name__ == "__main__":
    main()
