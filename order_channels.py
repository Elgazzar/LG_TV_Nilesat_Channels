import json, re, sys, os

# CONSTITUTION: High Quality / Low Quality Rules
HIGH_QUALITY_KEYWORDS = ['HD', 'Alhayat', 'MBC', 'DMC', 'ON', 'CBC', 'Rotana', 'OSN', 'Sky News', 'Al Jazeera', 'Extra News']

EXPLICIT_HQ = [
    'Al Qahera News',
    'beIN SPORTS',
    'beIN SPORTS NEWS',
    'ON SPORT HD',
    'ON SPORT MAX HD',
    'ON SPORT PLUS HD',
    'AD Sport 1 HD',
    'AD Sport 2 HD'
]

EXPLICIT_LQ = [
    'Hawa Baghdad Drama'
]

GROUPS_ORDER = [
    'Religion & Quran',
    'Premium & General',
    'English Movies',
    'Arabic Movies & Cinema',
    'Series & Drama',
    'Music',
    'News',
    'Sports',
    'Kids & Family',
    'Cooking',
    'Regional & Uncategorized'
]

HQ_SPLIT_GROUPS = ['English Movies', 'Arabic Movies & Cinema', 'Series & Drama', 'News', 'Sports', 'Kids & Family']

def is_high_quality(ch_name):
    if ch_name in EXPLICIT_LQ: return False
    if ch_name in EXPLICIT_HQ: return True
    for kw in HIGH_QUALITY_KEYWORDS:
        if kw.lower() in ch_name.lower():
            return True
    return False

def load_tll(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<legacybroadcast>(.*?)</legacybroadcast>', content, re.DOTALL)
    if not match: raise ValueError("No legacybroadcast found")
    return json.loads(match.group(1)), content, match.start(1), match.end(1)

def parse_readme_groups(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    groups_map = {g: [] for g in GROUPS_ORDER}
    current_group = None
    for line in lines:
        mg = re.match(r'<summary><b>(.*?) \(\d+ channels\)</b></summary>', line)
        if mg:
            current_group = mg.group(1)
            continue
        mc = re.match(r'- \d+: (.*)', line)
        if mc and current_group in groups_map:
            groups_map[current_group].append(mc.group(1).strip())
    return groups_map

def main():
    print("Executing SpecKit order_channels.py Engine...")
    tll_path = r'C:\Workspace\LG_TV_Nilesat_Channels\GlobalClone00001.TLL'
    readme_path = r'C:\Workspace\LG_TV_Nilesat_Channels\README.md'
    md_list_path = r'C:\Workspace\LG_TV_Nilesat_Channels\2026_channels_list.md'
    
    data, raw_content, start_idx, end_idx = load_tll(tll_path)
    readme_map = parse_readme_groups(readme_path)
    
    channels = sorted(data['channelList'], key=lambda x: (x.get('deleted', False) or x.get('skipped', False), x.get('majorNumber', 99999)))
    active = [ch for ch in channels if not (ch.get('deleted', False) or ch.get('skipped', False))]
    inactive = [ch for ch in channels if ch.get('deleted', False) or ch.get('skipped', False)]
    
    ch_map = {ch.get('channelName', ''): ch for ch in active}
    
    # 1. Group the channels based on README map
    group_objects = {k: [] for k in GROUPS_ORDER}
    for g_name, names in readme_map.items():
        for n in names:
            if n in ch_map:
                group_objects[g_name].append(ch_map[n])
                
    # Handle orphans (newly scanned channels not in README)
    processed = set(ch.get('channelName') for g in group_objects.values() for ch in g)
    orphans = [ch for ch in active if ch.get('channelName') not in processed]
    group_objects['Regional & Uncategorized'].extend(orphans)
    
    # 2. Sort Quality internally for required groups
    for g_name in HQ_SPLIT_GROUPS:
        ch_list = group_objects[g_name]
        
        if g_name == 'Sports':
            hq_names = [n for n in EXPLICIT_HQ if 'SPORT' in n.upper()]
            hq = [ch for ch in ch_list if ch.get('channelName') in hq_names]
            lq = [ch for ch in ch_list if ch not in hq]
        else:
            hq = [ch for ch in ch_list if is_high_quality(ch.get('channelName'))]
            lq = [ch for ch in ch_list if not is_high_quality(ch.get('channelName'))]
            
        group_objects[g_name] = hq + lq

    # 3. Flatten back to active list and renumber
    new_active = []
    for g_name in GROUPS_ORDER:
        new_active.extend(group_objects[g_name])
        
    current_num = 1
    for ch in new_active:
        ch['majorNumber'] = current_num
        current_num += 1
        
    data['channelList'] = new_active + inactive
    new_json = json.dumps(data, separators=(',', ':'))
    new_tll_content = raw_content[:start_idx] + new_json + raw_content[end_idx:]
    
    with open(tll_path, 'w', encoding='utf-8') as f:
        f.write(new_tll_content)
        
    # 4. Rebuild Markdown List
    md_lines = ['# 2026 TV Channels List', '', '| Channel Number | Channel Name | Program Num |', '| --- | --- | --- |']
    for ch in new_active:
        md_lines.append(f"| {ch.get('majorNumber')} | {ch.get('channelName', '').replace('|', '\\|')} | {ch.get('programNum', 0)} |")
    
    with open(md_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
        
    # 5. Rebuild README
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_text = f.read()
    idx = readme_text.find("## Channel Groups Overview")
    if idx != -1: readme_text = readme_text[:idx].strip()
    
    readme_append = "\n\n## Channel Groups Overview\n\nBelow is the complete list of channels grouped by their category. Click on each section to expand it.\n\n"
    
    for group_name in GROUPS_ORDER:
        ch_list = group_objects[group_name]
        readme_append += f"<details>\n<summary><b>{group_name} ({len(ch_list)} channels)</b></summary>\n\n"
        
        if group_name in HQ_SPLIT_GROUPS:
            if group_name == 'Sports':
                hq_names = [n for n in EXPLICIT_HQ if 'SPORT' in n.upper()]
                hq = [ch for ch in ch_list if ch.get('channelName') in hq_names]
                lq = [ch for ch in ch_list if ch not in hq]
            else:
                hq = [ch for ch in ch_list if is_high_quality(ch.get('channelName'))]
                lq = [ch for ch in ch_list if not is_high_quality(ch.get('channelName'))]
                
            readme_append += "### High Quality\n"
            for ch in hq: readme_append += f"- {ch.get('majorNumber')}: {ch.get('channelName')}\n"
            readme_append += "\n### Low Quality\n"
            for ch in lq: readme_append += f"- {ch.get('majorNumber')}: {ch.get('channelName')}\n"
        else:
            for ch in ch_list: readme_append += f"- {ch.get('majorNumber')}: {ch.get('channelName')}\n"
                
        readme_append += "\n</details>\n\n"
        
    readme_text += readme_append
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_text)
        
    print("Channel ordering, HQ/LQ sorting, and markdown synchronization completed successfully.")

if __name__ == '__main__':
    main()
