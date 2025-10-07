#!/usr/bin/env python3
"""
Remove SVG icons (lucide icons) from exam JSON files.
Targets: circle-question-mark, highlighter, triangle-alert icons
"""

import json
import re
from pathlib import Path

def remove_svg_icons(text):
    """Remove all lucide SVG icons from text."""
    # Pattern to match any SVG tag with lucide class
    svg_pattern = r'<svg[^>]*class="[^"]*lucide[^"]*"[^>]*>.*?</svg>'
    
    # Remove SVG tags
    cleaned = re.sub(svg_pattern, '', text, flags=re.DOTALL)
    
    # Also remove any standalone closing span tags that might be left
    # and extra <br> tags that often accompany these icons
    cleaned = re.sub(r'</span>(<br>)*\s*$', '', cleaned)
    
    return cleaned

def process_exam_file(file_path):
    """Process a single exam JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        
        # Process each section (mondai)
        if 'sections' in data:
            for section in data['sections']:
                if 'questions' in section:
                    for question in section['questions']:
                        # Clean passage field if it exists
                        if 'passage' in question and question['passage']:
                            original = question['passage']
                            cleaned = remove_svg_icons(original)
                            if cleaned != original:
                                question['passage'] = cleaned
                                modified = True
                        
                        # Clean text field if it contains HTML
                        if 'text' in question and question['text'] and '<svg' in question['text']:
                            original = question['text']
                            cleaned = remove_svg_icons(original)
                            if cleaned != original:
                                question['text'] = cleaned
                                modified = True
                        
                        # Clean options if they contain HTML
                        if 'options' in question:
                            for i, option in enumerate(question['options']):
                                if option and '<svg' in option:
                                    original = option
                                    cleaned = remove_svg_icons(original)
                                    if cleaned != original:
                                        question['options'][i] = cleaned
                                        modified = True
        
        # Save if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    exams_dir = Path('/Users/nguyenbahoanglong/Desktop/exams-api/exams')
    
    # Find all JSON files
    json_files = list(exams_dir.rglob('*.json'))
    
    print(f"Found {len(json_files)} JSON files")
    print("Removing SVG icons...")
    
    modified_count = 0
    
    for i, file_path in enumerate(json_files, 1):
        if process_exam_file(file_path):
            modified_count += 1
            print(f"[{i}/{len(json_files)}] ✓ {file_path.name}")
        else:
            if i % 50 == 0:
                print(f"[{i}/{len(json_files)}] Processed...")
    
    print(f"\n✅ Complete!")
    print(f"   Modified: {modified_count} files")
    print(f"   Total processed: {len(json_files)} files")

if __name__ == '__main__':
    main()
