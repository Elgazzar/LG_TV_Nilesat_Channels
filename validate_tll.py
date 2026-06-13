import json
import re
import sys
from pathlib import Path

def validate_tll(file_path):
    print(f"Validating {file_path}...")
    
    if not Path(file_path).exists():
        print("ERROR: File does not exist.")
        return False
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read file: {e}")
        return False

    match = re.search(r'<legacybroadcast>(.*?)</legacybroadcast>', content, re.DOTALL)
    if not match:
        print("ERROR: Could not find <legacybroadcast> payload.")
        return False
        
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON payload: {e}")
        return False

    if 'channelList' not in data:
        print("ERROR: Missing 'channelList' in JSON payload.")
        return False

    channels = data['channelList']
    active_channels = [ch for ch in channels if not (ch.get('deleted', False) or ch.get('skipped', False))]
    
    errors = []
    
    # 1. Check for orphaned / malformed data
    for i, ch in enumerate(active_channels):
        if 'channelName' not in ch:
            errors.append(f"Channel at index {i} is missing 'channelName'.")
        if 'majorNumber' not in ch:
            errors.append(f"Channel '{ch.get('channelName', 'UNKNOWN')}' is missing 'majorNumber'.")

    # 2. Check for Sequential Numbering and Duplicates
    if not errors:
        # Sort active channels by majorNumber
        active_sorted = sorted(active_channels, key=lambda x: x.get('majorNumber', 0))
        
        expected_num = 1
        seen_numbers = set()
        
        for ch in active_sorted:
            num = ch.get('majorNumber')
            name = ch.get('channelName')
            
            if num in seen_numbers:
                errors.append(f"Duplicate majorNumber {num} found for channel '{name}'.")
            seen_numbers.add(num)
            
            if num != expected_num:
                errors.append(f"Numbering GAP detected! Expected {expected_num}, but found {num} for channel '{name}'.")
                # Once we hit a gap, we just report the first few to avoid spam
                if len(errors) > 5:
                    errors.append("... additional numbering errors suppressed.")
                    break
            
            # Only increment expected_num if we matched, to keep checking relative to the offset,
            # or just assume strictly 1..N.
            expected_num += 1

    if errors:
        print("\n--- VALIDATION FAILED ---")
        for err in errors:
            print(f"[!] {err}")
        return False
        
    print(f"\n--- VALIDATION PASSED ---")
    print(f"Checked {len(channels)} total channels ({len(active_channels)} active).")
    print("No gaps, duplicates, or structural issues found.")
    return True

if __name__ == '__main__':
    target = r'C:\Workspace\LG_TV_Nilesat_Channels\GlobalClone00001.TLL'
    success = validate_tll(target)
    sys.exit(0 if success else 1)
