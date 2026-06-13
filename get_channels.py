import json, re

with open('C:/Workspace/LG_TV_Nilesat_Channels/GlobalClone00001.TLL', 'r', encoding='utf-8') as f:
    content = f.read()

data = json.loads(re.search(r'<legacybroadcast>(.*?)</legacybroadcast>', content, re.DOTALL).group(1))

channels = sorted(data['channelList'], key=lambda x: x.get('majorNumber', 99999))
active = [ch for ch in channels if not ch.get('deleted') and not ch.get('skipped')]

print('Total Active:', len(active))
for ch in active[:150]:
    print(str(ch.get('majorNumber')) + ': ' + ch.get('channelName'))
