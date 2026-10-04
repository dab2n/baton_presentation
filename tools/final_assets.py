# 2026-10-04 최종본(사정회 피피티) 반영용 이미지 생성
from PIL import Image, ImageOps
import re, pathlib
R = 'raw/final/img/'; A = 'assets/'
DL = '/Users/bugi/Downloads/'

def place(src, out, box, crop=None, img=None, K=2, flip=False, clip=(0, 0, 1920, 1080), save=True):
    """box=(x,y,w,h) 위에 crop=(left,top,width,height 박스 비율) 또는 img=(x,y,w,h 절대) 로 원본을 놓고, clip 과 겹치는 부분만 저장"""
    im = Image.open(src).convert('RGBA')
    if flip: im = ImageOps.mirror(im)
    bx, by, bw, bh = box
    if img: ix, iy, W, H = img
    else:
        l, t, w, h = crop; ix, iy, W, H = bx + l * bw, by + t * bh, w * bw, h * bh
    x0, y0, x1, y1 = max(bx, clip[0]), max(by, clip[1]), min(bx + bw, clip[2]), min(by + bh, clip[3])
    sx, sy = im.width / W, im.height / H; m = 1500
    pad = Image.new('RGBA', (im.width + 2 * m, im.height + 2 * m)); pad.paste(im, (m, m))
    r = pad.resize((round((x1 - x0) * K), round((y1 - y0) * K)), Image.LANCZOS,
                   box=((x0 - ix) * sx + m, (y0 - iy) * sy + m, (x1 - ix) * sx + m, (y1 - iy) * sy + m))
    if save: r.save(A + out, optimize=True)
    print(out, (round(x0, 3), round(y0, 3), round(x1 - x0, 3), round(y1 - y0, 3)))
    return r

def cover(src, box):
    im = Image.open(src); r = im.width / im.height; bx, by, bw, bh = box
    w, h = ((bh * r) / bw, 1) if bw / bh < r else (1, (bw / r) / bh)
    return (-(w - 1) / 2, -(h - 1) / 2, w, h)

# 3 오버뷰
place(R + 'ov281_27852042-b941-4c00-8314-64c420478475.png', 'ov2-sit.png', (668.1363, 330.5, 1124 * .3709, 1399 * .3794), crop=(0, 0, 1, 1))
place(R + 'kpr25_87128cde-22b1-4811-a73a-3fbac2b3798e.png', 'ov2-kpr.png', (910, 551, 212, 322), crop=(-.8539, 0, 2.7078, 1))
place('raw/src/ov-walk.png', 'ov2-walk.png', (308, 104, 264, 495), crop=(-1.1353, 0, 3.3237, 1))
place(DL + 'NAV 02 (1).png', 'ov2-nav.png', (181, 278, 202.88, 345), crop=(-1.0329, 0, 3.0224, 1))
place('raw/src/ov-ptr.png', 'ov2-ptr.png', (1558, 133, 158, 307), crop=(-1.1836, -.0001, 3.4585, 1.0001))
ImageOps.mirror(place(R + 'ov290_aacaef53-97b5-453d-88fc-4ea043da292a.png', 'ov2-golf.png', (1353, 204, 205, 538), crop=(-.4663, 0, 1.8654, 1.0659), save=False)).save(A + 'ov2-golf.png')  # 피그마는 크롭 후 박스째 좌우 반전
# 17 Expansion
place(R + 'exw_66169e05-1164-421f-ad42-f9be84c5ae67.png', 'exp-woman.png', (793.8, -12.25, 2957 * .9801, 1678 * .9801), crop=(0, 0, 1, 1), flip=True, clip=(1403, 181, 1920, 1080))
place(DL + 'NAV 02 (1).png', 'exp-nav.png', (111, 317, 291, 605), crop=(-3.0989, -.2371, 7.0897, 1.9145))
place(DL + 'PTR 01 (1).png', 'exp-ptr.png', (551, 328, 351, 642), crop=(-1.6086, 0, 4.1517, 1.2752))
place(R + 'ptr17_466c6044-66dc-447f-983c-1fd7715db5d2.png', 'exp-kpr.png', (1061, 633, 284, 358), crop=(-.6106, 0, 2.24, 1))
# 12 Scene 카드 (피그마가 블러·그라데이션까지 그린 이미지)
for i in (1, 2, 3):
    Image.open(R + f'scene{i}x.png').convert('RGB').save(A + f'scene{i}.jpg', quality=88)
# 16 호텔: 인물, 테이블 다리 조각 (테이블 이미지 아래쪽 76.93px 를 잘라 이어 붙임)
place('raw/s13/w3.png', 'sc3-woman.png', (781, -49, 1271, 1876), crop=cover('raw/s13/w3.png', (781, -49, 1271, 1876)))
leg = R + 'leg_568f2957-627b-4de6-8232-1f5648b91da6.png'
s = 823.4508 / 3840; H = 2160 * s
place(leg, 'sc3-leg.png', (307.2746, 0, 823.4508, 76.9276), img=(307.2746, 76.9276 - H, 823.4508, H), clip=(0, -9999, 1920, 9999))
# 18 전시 구성
Image.open(R + 'exhleft.png').convert('RGB').save(A + 'exh-left.jpg', quality=88)
place('raw/exh/display.png', 'exh-display.png', (117, 319, 353, 467.909), crop=(-.3672, -.1532, 1.7474, 1.3183), clip=(-9999, -9999, 9999, 9999))
