#!/usr/bin/env python3
"""
Generate comprehensive statistics for all exam files
"""

import json
from pathlib import Path
from collections import defaultdict

def analyze_exams():
    """Analyze all exam files and generate statistics"""
    exams_dir = Path(__file__).parent / "exams"
    
    stats = {
        "total_exams": 0,
        "by_level": defaultdict(lambda: {
            "count": 0,
            "total_questions": 0,
            "by_part": defaultdict(int),
            "by_type": defaultdict(int)
        })
    }
    
    # Process each level
    for level_dir in sorted(exams_dir.glob("N*")):
        if not level_dir.is_dir():
            continue
        
        level_name = level_dir.name
        
        for subdir in ["custom", "official"]:
            exam_dir = level_dir / subdir
            if not exam_dir.exists():
                continue
            
            for json_file in exam_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    stats["total_exams"] += 1
                    level_stats = stats["by_level"][level_name]
                    level_stats["count"] += 1
                    level_stats["by_type"][subdir] += 1
                    
                    # Count questions by part
                    for section in data.get("sections", []):
                        part = section.get("part", "unknown")
                        questions = len(section.get("questions", []))
                        level_stats["by_part"][part] += questions
                        level_stats["total_questions"] += questions
                
                except Exception as e:
                    print(f"Error processing {json_file}: {e}")
    
    return stats


def print_statistics(stats):
    """Print formatted statistics"""
    print("="*70)
    print("📊 JLPT EXAM DATABASE STATISTICS")
    print("="*70)
    print(f"\n🎯 Total Exams: {stats['total_exams']}")
    
    print("\n" + "="*70)
    print("📈 BREAKDOWN BY LEVEL")
    print("="*70)
    
    for level in sorted(stats["by_level"].keys()):
        level_stats = stats["by_level"][level]
        print(f"\n🔹 {level}")
        print(f"   Total exams: {level_stats['count']}")
        print(f"   Total questions: {level_stats['total_questions']:,}")
        
        if level_stats["by_type"]:
            print(f"   By type:")
            for exam_type, count in sorted(level_stats["by_type"].items()):
                print(f"      • {exam_type}: {count} exams")
        
        if level_stats["by_part"]:
            print(f"   Questions by part:")
            total = sum(level_stats["by_part"].values())
            for part in ["vocabulary", "grammar", "reading", "listening"]:
                count = level_stats["by_part"].get(part, 0)
                percentage = (count / total * 100) if total > 0 else 0
                print(f"      • {part.capitalize()}: {count:,} ({percentage:.1f}%)")
        
        # Calculate average questions per exam
        if level_stats["count"] > 0:
            avg = level_stats["total_questions"] / level_stats["count"]
            print(f"   Average questions per exam: {avg:.1f}")
    
    print("\n" + "="*70)
    print("📊 SUMMARY TABLE")
    print("="*70)
    print(f"{'Level':<8} {'Exams':<10} {'Questions':<12} {'Vocab':<10} {'Grammar':<10} {'Reading':<10} {'Listening':<10}")
    print("-"*70)
    
    for level in sorted(stats["by_level"].keys()):
        level_stats = stats["by_level"][level]
        vocab = level_stats["by_part"].get("vocabulary", 0)
        grammar = level_stats["by_part"].get("grammar", 0)
        reading = level_stats["by_part"].get("reading", 0)
        listening = level_stats["by_part"].get("listening", 0)
        
        print(f"{level:<8} {level_stats['count']:<10} {level_stats['total_questions']:<12,} "
              f"{vocab:<10,} {grammar:<10,} {reading:<10,} {listening:<10,}")
    
    print("\n" + "="*70)
    print("✨ Statistics generated successfully!")
    print("="*70)


def save_statistics_json(stats):
    """Save statistics to JSON file"""
    output_file = Path(__file__).parent / "exam_statistics.json"
    
    # Convert defaultdict to regular dict for JSON serialization
    json_stats = {
        "total_exams": stats["total_exams"],
        "by_level": {}
    }
    
    for level, level_stats in stats["by_level"].items():
        json_stats["by_level"][level] = {
            "count": level_stats["count"],
            "total_questions": level_stats["total_questions"],
            "by_part": dict(level_stats["by_part"]),
            "by_type": dict(level_stats["by_type"])
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Statistics saved to: {output_file}")


def main():
    """Main function"""
    print("🔍 Analyzing exam database...\n")
    stats = analyze_exams()
    print_statistics(stats)
    save_statistics_json(stats)


if __name__ == "__main__":
    main()
