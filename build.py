# 피그마에서 내보낸 텍스트 아웃라인 SVG(assets/t)를 template.html 의 <!--T:name--> 자리에 넣어 index.html 을 만든다.
# 폰트(Delight, SF Pro KR)는 재배포 금지라 글자를 벡터로 넣는다.
import re, pathlib

root = pathlib.Path(__file__).parent
T = root / 'assets/t'

def parts(name):
    s = (T / f'{name}.svg').read_text()
    m = re.search(r'width="1920" height="1080" transform="translate\((-?[\d.]+) (-?[\d.]+)\)"', s)
    dx, dy = (-float(m[1]), -float(m[2])) if m else (0, 0)
    els = re.findall(r'<path id="[^"]*"[^>]*/>|<rect [^>]*rx="(?:14.5|19.5)" fill="(?:black|white)"/>', s)
    els = [re.sub(r'^<path id="[^"]*"', '<path', e) for e in els]  # 피그마 레이어 이름 id 가 페이지 id 와 겹치지 않게
    return dx, dy, els

def first_y(el):
    m = re.search(r'(?:d="M\s*-?[\d.]+\s+|y=")(-?[\d.]+)', el)
    return float(m[1]) if m else 0

def g(els, dx=0, dy=0, cls='a', style=''):
    st = f' style="{style}"' if style else ''
    return f'<g class="{cls}"{st}><g transform="translate({dx:g} {dy:g})">' + ''.join(els) + '</g></g>'

out = {}
for n in ['c377', 'c378', 'c379', 'c380', 'c381', 'ringA', 'ringB', 's9t', 's10a', 's10b', 's10c', 'scenpill', 'scenintro']:
    dx, dy, els = parts(n)
    out[n] = ''.join(els) if n.startswith('ring') else g(els, dx, dy)
    out[n + '_xy'] = f'{dx:g} {dy:g}'

# 목차: CONTENTS + 4줄로 나눠 줄마다 따로 움직인다
_, _, els = parts('toc')
rows = [[] for _ in range(5)]
for el in els:
    y = first_y(el)
    rows[0 if y < 200 else 1 + min(3, int((y - 236) // 200))].append(el)
out['toc'] = ''.join(g(r, style=f'--d:{0.15 + i * 0.12:.2f}s') for i, r in enumerate(rows))

# 표지 baton 로고: 글자마다 왼쪽부터 차례로 올라온다
b = (root / 'assets/baton.svg').read_text()
b = b[b.index('<g id="Group">') + 14:b.index('</svg>')].replace('</g>\n<defs>', '<defs>')
xs = sorted(float(x) for x in re.findall(r'<path id="Vector[^"]*" d="M([\d.]+)', b))
b = re.sub(r'<path id="Vector[^"]*" d="M([\d.]+)', lambda m: f'<path class="a" style="--k:rise; --t:1.2s; --d:{0.1 + xs.index(float(m[1])) * 0.08:.2f}s" d="M{m[1]}', b)
out['baton'] = b
out['robots'] = (T / 'robots.svgfrag').read_text()  # 4장: 피그마 SVG 통째 (로봇 마스크 + 아웃라인 텍스트)

# 11 Scene: 카드별로 라벨(pill) → 제목 순서로 블러가 걷히며 떠오른다
_, _, els = parts('scenes')
grp = {}
for el in els:
    x = float(re.search(r'(?:d="M\s*|x=")(-?[\d.]+)', el)[1]); y = first_y(el)
    grp.setdefault((0 if x < 659 else 1 if x < 1273 else 2, y > 470), []).append(el)
out['scenes'] = ''.join(g(grp[(c, t)], cls='st', style=f'--d:{1.3 + c * 0.2 + t * 0.2:.2f}s') for c in range(3) for t in (False, True))

# 13~15 장소 장면: 라벨 → 제목 → 설명 순서로 블러가 걷히며 떠오른다
for n in ('sc1t', 'sc2t', 'sc3t'):
    dx, dy, els = parts(n)
    rows = [[], [], []]
    for el in els:
        y = first_y(el)  # 프레임 기준: 라벨 < 30 < 제목 < 140 < 설명
        rows[0 if y < 30 else 1 if y < 140 else 2].append(el)
    out[n] = ''.join(g(r, dx, dy, style=f'--k:blurup; --t:1.2s; --d:{0.15 + i * 0.15:.2f}s') for i, r in enumerate(rows))

html = (root / 'template.html').read_text()
html = re.sub(r'<!--T:(\w+)-->', lambda m: out[m[1]], html)
(root / 'index.html').write_text(html)
print('ok', len(html))
