#!/usr/bin/env python3
"""
Script to validate exam files structure and part assignments
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Mondai to Part mapping
MONDAI_PART_MAPPING = {
    "N1": {
        "vocabulary": list(range(1, 6)),
        "grammar": list(range(6, 9)),
        "reading": list(range(9, 14)),
        "listening": list(range(14, 19))
    },
    "N2": {
        "vocabulary": list(range(1, 6)),
        "grammar": list(range(6, 9)),
        "reading": list(range(9, 14)),
        "listening": list(range(14, 20))  # Mondai 14-19
    },
    "N3": {
        "vocabulary": list(range(1, 6)),
        "grammar": list(range(6, 9)),
        "reading": list(range(9, 13)),
        "listening": list(range(13, 18))
    },
    "N4": {
        "vocabulary": list(range(1, 6)),
        "grammar": list(range(6, 9)),
        "reading": list(range(9, 12)),
        "listening": list(range(12, 16))
    },
    "N5": {
        "vocabulary": list(range(1, 5)),
        "grammar": list(range(5, 8)),
        "reading": list(range(8, 11)),
        "listening": list(range(11, 15))
    }
}


def validate_exam_file(file_path: Path) -> dict:
    """Validate a single exam file"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"valid": False, "error": f"Cannot read file: {str(e)}"}
    
    # Check required fields
    required_fields = ["id", "title", "level", "type", "sections"]
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field: {field}")
    
    level = data.get("level")
    if level:
        level_str = f"N{level}"
    else:
        issues.append("Level field is missing or invalid")
        return {"valid": False, "issues": issues}
    
    if level_str not in MONDAI_PART_MAPPING:
        issues.append(f"Unknown level: {level_str}")
        return {"valid": False, "issues": issues}
    
    # Validate sections
    sections = data.get("sections", [])
    if not sections:
        issues.append("No sections found")
    
    seen_mondai = set()
    for idx, section in enumerate(sections):
        # Check section structure
        if "mondai" not in section:
            issues.append(f"Section {idx}: Missing mondai field")
            continue
        
        if "part" not in section:
            issues.append(f"Section {idx} (Mondai {section.get('mondai')}): Missing part field")
        
        if "questions" not in section:
            issues.append(f"Section {idx} (Mondai {section.get('mondai')}): Missing questions field")
        
        mondai = section.get("mondai")
        
        # Check for duplicate mondai
        if mondai in seen_mondai:
            issues.append(f"Duplicate mondai: {mondai}")
        seen_mondai.add(mondai)
        
        # Validate part assignment
        expected_part = None
        for part, mondai_list in MONDAI_PART_MAPPING[level_str].items():
            if mondai in mondai_list:
                expected_part = part
                break
        
        actual_part = section.get("part")
        if expected_part and actual_part != expected_part:
            issues.append(
                f"Mondai {mondai}: Incorrect part '{actual_part}', should be '{expected_part}'"
            )
        elif not expected_part:
            issues.append(f"Mondai {mondai}: Not in mapping for level {level_str}")
    
    # Validate statistics
    if "statistics" in data:
        stats = data["statistics"]
        if "by_part" in stats:
            # Recalculate and compare
            actual_stats = defaultdict(int)
            for section in sections:
                part = section.get("part")
                if part:
                    actual_stats[part] += len(section.get("questions", []))
            
            reported_stats = stats.get("by_part", {})
            for part in ["vocabulary", "grammar", "reading", "listening"]:
                if reported_stats.get(part) != actual_stats.get(part, 0):
                    issues.append(
                        f"Statistics mismatch for {part}: "
                        f"reported {reported_stats.get(part)}, actual {actual_stats.get(part, 0)}"
                    )
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "level": level_str,
        "sections": len(sections)
    }


def main():
    """Main validation function"""
    script_dir = Path(__file__).parent
    exams_dir = script_dir / "exams"
    
    if not exams_dir.exists():
        print(f"❌ Error: exams directory not found")
        return
    
    print("🔍 Starting validation...\n")
    
    total_files = 0
    valid_files = 0
    invalid_files = 0
    level_stats = defaultdict(lambda: {"valid": 0, "invalid": 0})
    
    # Process each level
    for level_dir in sorted(exams_dir.glob("N*")):
        if not level_dir.is_dir():
            continue
        
        print(f"📂 Validating {level_dir.name}...")
        
        for subdir in ["custom", "official"]:
            exam_dir = level_dir / subdir
            if not exam_dir.exists():
                continue
            
            json_files = list(exam_dir.glob("*.json"))
            
            for json_file in json_files:
                total_files += 1
                result = validate_exam_file(json_file)
                
                if result.get("valid"):
                    valid_files += 1
                    level_stats[level_dir.name]["valid"] += 1
                else:
                    invalid_files += 1
                    level_stats[level_dir.name]["invalid"] += 1
                    print(f"   ⚠️  {json_file.name}:")
                    for issue in result.get("issues", [])[:5]:
                        print(f"      - {issue}")
                    if len(result.get("issues", [])) > 5:
                        print(f"      ... and {len(result.get('issues', [])) - 5} more issues")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60)
    print(f"✅ Valid files: {valid_files}")
    print(f"❌ Invalid files: {invalid_files}")
    print(f"📝 Total files: {total_files}")
    print(f"✓  Success rate: {valid_files/total_files*100:.1f}%")
    
    print("\n📊 By Level:")
    for level in sorted(level_stats.keys()):
        stats = level_stats[level]
        total = stats["valid"] + stats["invalid"]
        print(f"   {level}: {stats['valid']}/{total} valid "
              f"({stats['valid']/total*100:.1f}%)")
    
    if invalid_files == 0:
        print("\n✨ All files are valid!")
    else:
        print(f"\n⚠️  Found {invalid_files} files with issues")


if __name__ == "__main__":
    main()
