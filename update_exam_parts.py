#!/usr/bin/env python3
"""
Script to update and validate exam files with correct part assignments
Based on MONDAI_PART_MAPPING.md
"""

import json
import os
from pathlib import Path
from typing import Dict, List

# Mondai to Part mapping for each level
MONDAI_PART_MAPPING = {
    "N1": {
        "vocabulary": list(range(1, 6)),  # Mondai 1-5
        "grammar": list(range(6, 9)),     # Mondai 6-8
        "reading": list(range(9, 14)),    # Mondai 9-13
        "listening": list(range(14, 19))  # Mondai 14-18
    },
    "N2": {
        "vocabulary": list(range(1, 6)),  # Mondai 1-5
        "grammar": list(range(6, 9)),     # Mondai 6-8
        "reading": list(range(9, 14)),    # Mondai 9-13
        "listening": list(range(14, 20))  # Mondai 14-19 (some exams have 19)
    },
    "N3": {
        "vocabulary": list(range(1, 6)),  # Mondai 1-5
        "grammar": list(range(6, 9)),     # Mondai 6-8
        "reading": list(range(9, 13)),    # Mondai 9-12
        "listening": list(range(13, 18))  # Mondai 13-17
    },
    "N4": {
        "vocabulary": list(range(1, 6)),  # Mondai 1-5
        "grammar": list(range(6, 9)),     # Mondai 6-8
        "reading": list(range(9, 12)),    # Mondai 9-11
        "listening": list(range(12, 16))  # Mondai 12-15
    },
    "N5": {
        "vocabulary": list(range(1, 5)),  # Mondai 1-4
        "grammar": list(range(5, 8)),     # Mondai 5-7
        "reading": list(range(8, 11)),    # Mondai 8-10
        "listening": list(range(11, 15))  # Mondai 11-14
    }
}


def get_part_for_mondai(level: str, mondai: int) -> str:
    """Get the part name for a given level and mondai number"""
    mapping = MONDAI_PART_MAPPING.get(level)
    if not mapping:
        return None
    
    for part, mondai_list in mapping.items():
        if mondai in mondai_list:
            return part
    return None


def calculate_statistics(sections: List[Dict]) -> Dict:
    """Calculate statistics from sections"""
    stats = {
        "vocabulary": 0,
        "grammar": 0,
        "reading": 0,
        "listening": 0
    }
    
    for section in sections:
        part = section.get("part")
        if part in stats:
            stats[part] += len(section.get("questions", []))
    
    return stats


def update_exam_file(file_path: Path) -> Dict:
    """Update a single exam file with correct part assignments"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get level from filename or data
        level = data.get("level")
        if level:
            level_str = f"N{level}"
        else:
            # Try to extract from filename
            filename = file_path.stem
            for l in ["N1", "N2", "N3", "N4", "N5"]:
                if l in filename.upper():
                    level_str = l
                    break
            else:
                return {"status": "error", "message": "Could not determine level", "file": str(file_path)}
        
        # Check if mapping exists for this level
        if level_str not in MONDAI_PART_MAPPING:
            return {"status": "error", "message": f"No mapping for level {level_str}", "file": str(file_path)}
        
        updated = False
        sections = data.get("sections", [])
        
        # Update each section with correct part
        for section in sections:
            mondai = section.get("mondai")
            if mondai is None:
                continue
            
            correct_part = get_part_for_mondai(level_str, mondai)
            if correct_part:
                current_part = section.get("part")
                if current_part != correct_part:
                    section["part"] = correct_part
                    updated = True
                elif current_part is None:
                    section["part"] = correct_part
                    updated = True
        
        # Update or add statistics
        stats = calculate_statistics(sections)
        total_questions = sum(stats.values())
        
        if "statistics" not in data:
            data["statistics"] = {}
            updated = True
        
        if data["statistics"].get("by_part") != stats:
            data["statistics"]["by_part"] = stats
            updated = True
        
        if data["statistics"].get("total_questions") != total_questions:
            data["statistics"]["total_questions"] = total_questions
            updated = True
        
        if data["statistics"].get("total_sections") != len(sections):
            data["statistics"]["total_sections"] = len(sections)
            updated = True
        
        # Save if updated
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {"status": "updated", "file": str(file_path), "level": level_str}
        else:
            return {"status": "ok", "file": str(file_path), "level": level_str}
    
    except Exception as e:
        return {"status": "error", "message": str(e), "file": str(file_path)}


def process_directory(base_path: Path) -> Dict:
    """Process all exam JSON files in the directory"""
    results = {
        "updated": [],
        "ok": [],
        "errors": []
    }
    
    # Process each level
    for level_dir in base_path.glob("N*"):
        if not level_dir.is_dir():
            continue
        
        print(f"\n📂 Processing {level_dir.name}...")
        
        # Process custom and official subdirectories
        for subdir in ["custom", "official"]:
            exam_dir = level_dir / subdir
            if not exam_dir.exists():
                continue
            
            json_files = list(exam_dir.glob("*.json"))
            print(f"   Found {len(json_files)} files in {subdir}/")
            
            for json_file in json_files:
                result = update_exam_file(json_file)
                status = result["status"]
                
                if status == "updated":
                    results["updated"].append(result)
                    print(f"   ✅ Updated: {json_file.name}")
                elif status == "ok":
                    results["ok"].append(result)
                elif status == "error":
                    results["errors"].append(result)
                    print(f"   ❌ Error: {json_file.name} - {result.get('message')}")
    
    return results


def main():
    """Main execution function"""
    # Get the exams directory
    script_dir = Path(__file__).parent
    exams_dir = script_dir / "exams"
    
    if not exams_dir.exists():
        print(f"❌ Error: exams directory not found at {exams_dir}")
        return
    
    print("🚀 Starting exam files update...")
    print(f"📁 Base directory: {exams_dir}")
    
    results = process_directory(exams_dir)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"✅ Updated files: {len(results['updated'])}")
    print(f"✓  Already correct: {len(results['ok'])}")
    print(f"❌ Errors: {len(results['errors'])}")
    print(f"📝 Total processed: {len(results['updated']) + len(results['ok']) + len(results['errors'])}")
    
    if results['errors']:
        print("\n⚠️  Errors encountered:")
        for error in results['errors'][:10]:  # Show first 10 errors
            print(f"   - {error['file']}: {error.get('message', 'Unknown error')}")
        if len(results['errors']) > 10:
            print(f"   ... and {len(results['errors']) - 10} more errors")
    
    print("\n✨ Update complete!")


if __name__ == "__main__":
    main()
