import sys, json
from backend import sort_contents
js = []
content = sys.stdin.read()
decoder = json.JSONDecoder()
pos = 0
while True:
    try:
        js_exp, pos = decoder.raw_decode(content, pos)
        js.append(js_exp)
    except json.JSONDecodeError:
        try:
            content = content[pos:]
            pos = content.index('{')
            js_exp, pos = decoder.raw_decode(content, pos)
            js.append(js_exp)
        except:
            break


sorted_list = sort_contents(js[0:10])
sys.stdout.write(json.dumps(sorted_list)) 