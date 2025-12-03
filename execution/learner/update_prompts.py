"""
Update prompts based on learnings.
"""
import sys
import json
from pathlib import Path

def update_prompts(analysis_results: dict, prompt_dir: str = 'config/prompts') -> dict:
    """
    Update prompt templates based on analysis.
    
    Args:
        analysis_results: Results from analyze_corrections
        prompt_dir: Directory containing prompts
    
    Returns:
        Dict with update status
    """
    import shutil
    prompts_updated = []
    backup_created = False
    # Backup all prompt files
    prompt_path = Path(prompt_dir)
    backup_path = prompt_path.parent / (prompt_path.name + '_backup')
    if not backup_path.exists():
        shutil.copytree(prompt_path, backup_path)
        backup_created = True
    # Update prompt files based on corrections and patterns
    corrections = analysis_results.get('common_corrections', [])
    patterns = analysis_results.get('successful_patterns', [])
    for prompt_file in prompt_path.glob('*.txt'):
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Apply top correction and pattern to prompt
        if corrections:
            top_correction = corrections[0][0]
            content += f"\n\n# Correction Insight: {top_correction}"
        if patterns:
            top_pattern = patterns[0][0]
            content += f"\n# Successful Pattern: {top_pattern}"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(content)
        prompts_updated.append(prompt_file.name)
    return {
        'success': True,
        'prompts_updated': prompts_updated,
        'backup_created': backup_created
    }

if __name__ == "__main__":
    print("update_prompts.py - Prompt update tool")
