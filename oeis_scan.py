import re, json, time, urllib.request, urllib.parse, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
t = open('data/problems.yaml', encoding='utf-8').read()
blocks = re.split(r'\n- number:', t)[1:]
poss = []
for b in blocks:
    if re.search(r'oeis:\s*\[[^\]]*possible', b):
        n = re.match(r'\s*"?(\d+)', b).group(1)
        cur = re.findall(r'A\d{6}', re.search(r'oeis:\s*\[([^\]]*)\]', b).group(1))
        poss.append((n, cur))
print('possible problems:', len(poss), flush=True)
out = {}
for n, cur in poss:
    q = f'erdosproblems.com/{n}'
    url = 'https://oeis.org/search?' + urllib.parse.urlencode({'q': '"' + q + '"', 'fmt': 'json'})
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'erdosproblems-link-check/0.1 (research; low rate)'})
            data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
            break
        except Exception as e:
            data = None; time.sleep(3)
    res = []
    if data:
        # new API returns list or {"results":[...]}
        items = data if isinstance(data, list) else (data.get('results') or [])
        for it in items or []:
            a = 'A%06d' % it['number']
            # only keep entries whose links actually mention exactly this problem number
            links = ' '.join(it.get('link', []) + it.get('comment', []) + it.get('reference', []))
            if re.search(r'erdosproblems\.com/%s(?!\d)' % n, links):
                res.append((a, it['name'][:90]))
    out[n] = {'current': cur, 'oeis': res}
    time.sleep(1.2)
json.dump(out, open('../oeis_scan.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('done', flush=True)
