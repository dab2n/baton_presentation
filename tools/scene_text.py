# 13~15 장소 장면 문구: 피그마 문구 그대로, 글꼴만 다른 장과 같은 규칙(SF Pro +KR, 자간 0)으로
# 제목 Semibold 38 / 줄높이 1.3, 설명 Medium 20 #424242 50% / 줄높이 1.45, 라벨(#N)은 피그마 그대로
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from textout import block
T = pathlib.Path(__file__).parent.parent / 'assets/t'
TEXT = {
  'sc1t': (['처음 방문한 해외 병원도', '문제없이'],
           ['Leo는 처음 방문한 해외 병원에서도,', '국내에서 진료받았던 맥락과,', '진료 예약 내역을 손쉽게 전달합니다.', '',
            '방문 목적을 이해한 Navigator는', 'Leo를 진료실까지 안내합니다.']),
  'sc2t': (['신체 상태에 맞는', '운동 난이도'],
           ['Leo는 병원에서 확인한 검진 정보를', 'Baton을 통해 Partner에게 전달합니다.', '',
            '병원에서 진료 받은 맥락을 이해하고,', '무리하지 않는 선에서 운동할 수 있도록', '강도와 운동 방식을 조절합니다.']),
  'sc3t': (['나의 취향대로', '온전히 휴식에 집중하는 시간'],
           ['하루 일과를 마치고 호텔로 돌아온 Leo는', '자신의 취향 정보를 Baton을 통해', 'Keeper에게 전달합니다.', '',
            'Leo가 샤워를 하는 동안 Keeper는', '평소 좋아하는 음악을 재생하고,', '입맛에 맞는 음식을 주문해 편안한', '휴식을 준비합니다.']),
}
X, Y = 60, 60                       # 텍스트 프레임 위치
TITLE_TOP = Y + 29 + 15             # 라벨(29) + 간격 15
for name, (title, body) in TEXT.items():
    s = (T / f'{name}.svg').read_text()   # 피그마 내보내기: 라벨만 가져온다
    m = re.search(r'translate\((-?[\d.]+) (-?[\d.]+)\)', s); dx, dy = -float(m[1]), -float(m[2])
    els = [re.sub(r'^<path id="[^"]*"', '<path', e) for e in re.findall(r'<path id="[^"]*"[^>]*/>|<rect [^>]*rx="14.5" fill="black"/>', s)]
    pill = [e for e in els if e.startswith('<rect') or float(re.search(r'd="M\s*-?[\d.]+\s+(-?[\d.]+)', e)[1]) < 30]
    t = block(title, 'semibold', 38, 38 * 1.3, X, TITLE_TOP)
    b = block(body, 'medium', 20, 29, X, TITLE_TOP + 38 * 1.3 * len(title) + 56, fill='#424242', opacity=.5)
    g = lambda inner, d: f'<g class="a" style="--k:blurup; --t:1.2s; --d:{d}s">{inner}</g>'
    frag = ('<svg class="full" viewBox="0 0 1920 1080">' + g(f'<g transform="translate({dx:g} {dy:g})">' + ''.join(pill) + '</g>', .15)
            + g(t, .3) + g(b, .45) + '</svg>')
    (T / f'{name}.svgfrag').write_text(frag); print(name, len(frag))
