from backend import sort_contents
import sys, json
        
js = []
content = sys.stdin.read()
decoder = json.JSONDecoder()
pos = 0
while True:
    try:
        o, pos = decoder.raw_decode(content, pos)
        js.append(o)
    except json.JSONDecodeError:
        try:
            content = content[pos:]
            pos = content.index('{')
            o, pos = decoder.raw_decode(content, pos)
            js.append(o)
        except:
            try:
                content = content[pos+1:]
                pos = content.index('{')
                o, pos = decoder.raw_decode(content, pos)
                js.append(o)
            except:
                break
clean = []
for obj in js:
    if type(obj) == dict:
        if 'content' in obj and len(obj) == 1:
            if type(obj['content']) == int:
                if obj['content'] < 25 and obj['content'] > 0:
                    clean.append(obj)
obj = []
blocks = []
for i in range(0, len(clean), 10):
        blocks.append(clean[i:i + 10])
to_sort = []
for b in blocks:
    if len(b) == 10:
        to_sort.append(b)

for ts in to_sort:
    sort = sort_contents(ts)
    obj.append(sort)

print(json.dumps(obj))

