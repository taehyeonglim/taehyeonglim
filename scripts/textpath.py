#!/usr/bin/env python3
"""TTF 글리프를 SVG 패스 아웃라인으로 변환하는 조판 도구.

GitHub README의 <img> SVG는 외부 폰트를 로드할 수 없으므로, 대형
디스플레이 타이포(Chakra Petch)는 이 도구로 패스를 생성해 임베드한다.
사용: python3 scripts/textpath.py FONT.ttf "TEXT" SIZE [tracking_em]
출력: 1행 <!-- width=NNN.N -->, 2행 <path d="..."> 에 넣을 d 문자열.
원점은 베이스라인 좌측 (SVG 좌표계, y축 아래방향).
"""
import sys

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


def text_to_path(font_path, text, size, tracking_em=0.0):
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    upm = font["head"].unitsPerEm
    scale = size / upm
    x = 0.0
    d = []
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:  # 글리프 없음 → 0.5em 전진
            x += size * 0.5 + tracking_em * size
            continue
        glyph = glyphs[name]
        pen = SVGPathPen(glyphs)
        glyph.draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0)))
        cmd = pen.getCommands()
        if cmd:
            d.append(cmd)
        x += glyph.width * scale + tracking_em * size
    return " ".join(d), x


def main():
    font_path, text, size = sys.argv[1], sys.argv[2], float(sys.argv[3])
    tracking = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    d, width = text_to_path(font_path, text, size, tracking)
    print("<!-- width=%.1f -->" % width)
    print(d)


if __name__ == "__main__":
    main()
