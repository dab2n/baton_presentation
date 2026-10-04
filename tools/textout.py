# SF Pro +KR 로 글자를 SVG 아웃라인 path 로 만든다 (폰트 파일은 배포하지 않음).
# 피그마 줄 배치 규칙: 줄 높이 박스 안에서 (ascender-descender) 를 세로 가운데 정렬.
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = '/Users/bugi/Library/Fonts/SFProKR-{}.otf'
WEIGHT = {'regular': 'Regular-04', 'medium': 'Medium-05', 'semibold': 'Semibold-06', 'bold': 'Bold-07'}
OTHER = {'pretendard-bold': '/Users/bugi/Library/Fonts/Pretendard-Bold.otf'}  # 목차 페이지 숫자용
_cache = {}

def _font(w):
    if w not in _cache:
        path = OTHER[w] if w in OTHER else FONTS.format(WEIGHT[w])
        blob = hb.Blob.from_file_path(path)
        _cache[w] = (TTFont(path), hb.Font(hb.Face(blob)))
    return _cache[w]

def block(lines, weight, size, lh, x, top, fill='#000', opacity=None, tracking=0, align='left', width=None):
    """lines: 줄 목록(빈 문자열 = 빈 줄). lh: 줄 높이(px). 반환: <path> 문자열 하나"""
    tt, hbf = _font(weight)
    upm = tt['head'].unitsPerEm; k = size / upm
    asc, desc = tt['hhea'].ascent, tt['hhea'].descent
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    pen = SVGPathPen(gs)
    for i, line in enumerate(lines):
        if not line: continue
        buf = hb.Buffer(); buf.add_str(line); buf.guess_segment_properties()
        hb.shape(hbf, buf, {})
        adv = sum(p.x_advance for p in buf.glyph_positions) * k + tracking * len(line)
        x0 = x if align == 'left' else x - adv if align == 'right' else x + (width - adv) / 2
        base = round(top + i * lh + (lh - (asc - desc) * k) / 2 + asc * k)  # 피그마는 기준선을 정수 픽셀에 맞춤
        cx = x0
        for inf, pos in zip(buf.glyph_infos, buf.glyph_positions):
            g = order[inf.codepoint]
            gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx + pos.x_offset * k, base - pos.y_offset * k)))
            cx += pos.x_advance * k + tracking
    op = f' opacity="{opacity}"' if opacity is not None else ''
    return f'<path d="{pen.getCommands()}" fill="{fill}"{op}/>'
