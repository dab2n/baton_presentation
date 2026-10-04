# 원본 이미지가 피그마 화면에서 어디에 어떤 크기로 놓였는지 역산 (흰 배경 위 합성 비교)
from PIL import Image, ImageOps
import numpy as np
def fit(raw, fig, region, init, flip=False, uniform=False, steps=(.004, 6), iters=300, bg=(255, 255, 255)):
    F = np.asarray(Image.open(fig).convert('RGB')).astype(float)
    R = Image.open(raw).convert('RGBA')
    if flip: R = ImageOps.mirror(R)
    k = 1024 / max(R.size); Rs = R.resize((round(R.width * k), round(R.height * k)), Image.LANCZOS)
    x0, y0, x1, y1 = region; tgt = F[y0:y1, x0:x1]
    def comp(p):
        sx, sy, ox, oy = p
        if uniform: sy = sx
        w, h = max(1, round(R.width * sx)), max(1, round(R.height * sy))
        can = Image.new('RGBA', (x1 - x0 + 4000, y1 - y0 + 4000), bg + (255,))
        can.alpha_composite(Rs.resize((w, h), Image.BILINEAR), (round(ox - x0) + 2000, round(oy - y0) + 2000))
        return np.asarray(can.crop((2000, 2000, 2000 + x1 - x0, 2000 + y1 - y0)).convert('RGB')).astype(float)
    f = lambda p: np.abs(comp(p) - tgt).mean()
    q = np.array(init, float); st = np.array([steps[0], steps[0], steps[1], steps[1]]); b = f(q)
    for _ in range(iters):
        b = f(q); imp = False
        for i in range(4):
            if uniform and i == 1: continue
            for sg in (1, -1):
                t = q.copy(); t[i] += sg * st[i]; e = f(t)
                if e < b: b, q, imp = e, t, True
        if not imp:
            st /= 2
            if st[2] < .25: break
    if uniform: q[1] = q[0]
    return q, b
