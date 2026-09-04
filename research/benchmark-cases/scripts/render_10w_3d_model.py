"""Render a paper-style model-definition figure from 10w-3d.bdf.

The script reads the external BDF but never modifies or copies it.  It draws
geometry, property regions, SPC locations and PLOAD4 faces only; no solution
field is implied.
"""

from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1800, 900
PID_COLORS = {1: (188, 203, 216), 2: (226, 184, 96)}
LOAD_COLOR = (205, 66, 58)
SPC_COLOR = (30, 91, 145)


def fields(line: str) -> list[str]:
    line = line.rstrip("\r\n").ljust(80)
    return [line[i : i + 8].strip() for i in range(8, 80, 8)]


def bdf_float(value: str) -> float:
    value = value.strip().upper().replace("D", "E")
    if "E" not in value:
        value = re.sub(r"(?<=\d)([+-]\d+)$", r"E\1", value)
    return float(value)


def read_bdf(path: Path):
    nodes: dict[int, np.ndarray] = {}
    tets: list[tuple[int, int, tuple[int, int, int, int]]] = []
    spc_nodes: set[int] = set()
    pload: dict[int, tuple[int, int]] = {}

    with path.open("r", encoding="ascii", errors="strict") as stream:
        for line in stream:
            card = line[:8].strip()
            if card not in {"GRID", "CTETRA", "SPC", "PLOAD4"}:
                continue
            f = fields(line)
            if card == "GRID":
                nodes[int(f[0])] = np.array(
                    [bdf_float(f[2]), bdf_float(f[3]), bdf_float(f[4])],
                    dtype=float,
                )
            elif card == "CTETRA":
                tets.append((int(f[0]), int(f[1]), tuple(map(int, f[2:6]))))
            elif card == "SPC" and int(f[0]) == 2:
                spc_nodes.add(int(f[1]))
            elif card == "PLOAD4" and int(f[0]) == 3:
                pload[int(f[1])] = (int(f[6]), int(f[7]))
    return nodes, tets, spc_nodes, pload


def exterior_faces(tets):
    boundary = {}
    for eid, pid, n in tets:
        candidates = (
            ((n[0], n[1], n[2]), n[3]),
            ((n[0], n[1], n[3]), n[2]),
            ((n[0], n[2], n[3]), n[1]),
            ((n[1], n[2], n[3]), n[0]),
        )
        for face, opposite in candidates:
            key = tuple(sorted(face))
            if key in boundary:
                boundary.pop(key)
            else:
                boundary[key] = (face, opposite, pid, eid)
    return list(boundary.values())


def select_loaded_faces(boundary, pload):
    by_eid = defaultdict(list)
    for item in boundary:
        by_eid[item[3]].append(item)
    loaded = []
    missing = []
    for eid, pair in pload.items():
        # For a CTETRA PLOAD4, G1 lies on the loaded triangular face and
        # G34 identifies the corner excluded from that face.
        g1, g34 = pair
        matches = [item for item in by_eid[eid] if g1 in item[0] and g34 not in item[0]]
        if len(matches) == 1:
            loaded.append(matches[0])
        else:
            missing.append(eid)
    if missing:
        raise RuntimeError(f"Cannot identify {len(missing)} PLOAD4 faces; first EID={missing[0]}")
    return loaded


def camera(azimuth_deg=-48.0, elevation_deg=18.0):
    az = math.radians(azimuth_deg)
    el = math.radians(elevation_deg)
    right = np.array([-math.sin(az), math.cos(az), 0.0])
    up = np.array(
        [-math.cos(az) * math.sin(el), -math.sin(az) * math.sin(el), math.cos(el)]
    )
    view = np.array([math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el)])
    return right, up, view


def project(points, panel, bounds):
    right, up, view = camera()
    centre = (bounds[0] + bounds[1]) / 2
    q = points - centre
    uv = np.column_stack((q @ right, q @ up))
    corners = np.array(
        [[x, y, z] for x in (bounds[0][0], bounds[1][0])
         for y in (bounds[0][1], bounds[1][1])
         for z in (bounds[0][2], bounds[1][2])]
    ) - centre
    cuv = np.column_stack((corners @ right, corners @ up))
    span = np.ptp(cuv, axis=0)
    x0, y0, x1, y1 = panel
    scale = min((x1 - x0) / span[0], (y1 - y0) / span[1]) * 0.88
    mid = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
    screen = (uv - (cuv.min(axis=0) + cuv.max(axis=0)) / 2) * scale
    screen[:, 1] *= -1
    screen += mid
    depth = q @ view
    return screen, depth, scale


def face_geometry(item, nodes):
    face, opposite, pid, eid = item
    xyz = np.array([nodes[n] for n in face])
    centre = xyz.mean(axis=0)
    normal = np.cross(xyz[1] - xyz[0], xyz[2] - xyz[0])
    norm = np.linalg.norm(normal)
    if norm:
        normal /= norm
    if np.dot(normal, nodes[opposite] - centre) > 0:
        normal *= -1
    return xyz, centre, normal, pid, eid


def shade(color, normal):
    light = np.array([-0.35, -0.3, 0.88])
    light /= np.linalg.norm(light)
    factor = 0.76 + 0.24 * abs(float(np.dot(normal, light)))
    return tuple(int(255 - (255 - c) * factor) for c in color)


def load_fonts():
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
    ]
    font_path = next((p for p in candidates if p.exists()), None)
    if font_path is None:
        return ImageFont.load_default(), ImageFont.load_default(), ImageFont.load_default()
    return (
        ImageFont.truetype(str(font_path), 34),
        ImageFont.truetype(str(font_path), 25),
        ImageFont.truetype(str(font_path), 18),
    )


def draw_arrow(draw, start, end, color, width=4):
    draw.line([tuple(start), tuple(end)], fill=color, width=width)
    v = np.asarray(start, dtype=float) - np.asarray(end, dtype=float)
    norm = np.linalg.norm(v)
    if not norm:
        return
    v /= norm
    p = np.array([-v[1], v[0]])
    tip = np.asarray(end)
    a = tip + v * 15 + p * 7
    b = tip + v * 15 - p * 7
    draw.polygon([tuple(tip), tuple(a), tuple(b)], fill=color)


def add_double_arrow(draw, start, end, label, font):
    draw_arrow(draw, start, end, (60, 60, 60), 2)
    draw_arrow(draw, end, start, (60, 60, 60), 2)
    pos = (np.asarray(start) + np.asarray(end)) / 2
    box = draw.textbbox((0, 0), label, font=font)
    draw.rectangle(
        [pos[0] - (box[2] - box[0]) / 2 - 5, pos[1] - 14,
         pos[0] + (box[2] - box[0]) / 2 + 5, pos[1] + 14],
        fill=(255, 255, 255),
    )
    draw.text(tuple(pos), label, fill=(55, 55, 55), font=font, anchor="mm")


def render_png(output, nodes, boundary, loaded, spc_nodes):
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image, "RGBA")
    title_font, label_font, small_font = load_fonts()
    all_xyz = np.array(list(nodes.values()))
    bounds = (all_xyz.min(axis=0), all_xyz.max(axis=0))
    panels = [(55, 125, 870, 725), (930, 125, 1745, 725)]
    node_ids = list(nodes)
    node_xyz = np.array([nodes[n] for n in node_ids])
    index = {nid: i for i, nid in enumerate(node_ids)}

    draw.text((WIDTH / 2, 45), "10w-3d 线弹性模型", fill=(30, 30, 30), font=title_font, anchor="mm")
    draw.text((panels[0][0], 92), "(a) 几何与材料分区", fill=(35, 35, 35), font=label_font)
    draw.text((panels[1][0], 92), "(b) 载荷与位移约束", fill=(35, 35, 35), font=label_font)
    draw.line((900, 105, 900, 735), fill=(220, 220, 220, 255), width=2)

    for panel_idx, panel in enumerate(panels):
        projected, depth, scale = project(node_xyz, panel, bounds)
        records = []
        for item in boundary:
            xyz, _, normal, pid, _ = face_geometry(item, nodes)
            ids = [index[n] for n in item[0]]
            records.append((float(depth[ids].mean()), ids, normal, pid))
        records.sort(key=lambda rec: rec[0])
        for _, ids, normal, pid in records:
            poly = [tuple(projected[i]) for i in ids]
            draw.polygon(poly, fill=shade(PID_COLORS.get(pid, (200, 200, 200)), normal) + (255,))

        if panel_idx == 1:
            loaded_records = []
            for item in loaded:
                xyz, centre, normal, _, eid = face_geometry(item, nodes)
                ids = [index[n] for n in item[0]]
                loaded_records.append((float(depth[ids].mean()), ids, centre, normal, eid))
            loaded_records.sort(key=lambda rec: rec[0])
            for _, ids, _, _, _ in loaded_records:
                draw.polygon([tuple(projected[i]) for i in ids], fill=LOAD_COLOR + (210,))

            step = max(1, len(loaded_records) // 9)
            right, up, _ = camera()
            for _, _, centre, normal, _ in loaded_records[::step][:9]:
                end3 = centre
                start3 = centre + normal * 22
                pair = np.array([start3, end3])
                uv, _, _ = project(pair, panel, bounds)
                draw_arrow(draw, uv[0], uv[1], LOAD_COLOR, 4)

            for nid in sorted(spc_nodes):
                p = projected[index[nid]]
                r = 8
                draw.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r),
                             fill=SPC_COLOR + (255,), outline=(255, 255, 255, 255), width=2)

    # Legend and definition notes
    y = 765
    draw.rectangle((85, y - 11, 113, y + 11), fill=PID_COLORS[1] + (255,))
    draw.text((123, y), "PID 1 / MAT1 1", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.rectangle((310, y - 11, 338, y + 11), fill=PID_COLORS[2] + (255,))
    draw.text((348, y), "PID 2 / MAT1 2", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.rectangle((955, y - 11, 983, y + 11), fill=LOAD_COLOR + (255,))
    draw.text((993, y), "PLOAD4：p=0.025，LOAD 系数 10", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.ellipse((1328, y - 8, 1344, y + 8), fill=SPC_COLOR + (255,))
    draw.text((1354, y), "SPC 2：9 节点，g=(0.1, 0.2, 0.3)",
              fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.text((85, 825), "包围盒：Δx=200，Δy=319.947，Δz=470（单位未声明）",
              fill=(45, 45, 45), font=small_font, anchor="lm")
    draw_arrow(draw, np.array([1130, 840]), np.array([1130, 808]), (55, 55, 55), 3)
    draw.text((1145, 824), "GRAV：a=(0, -9800, 0)", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.text((WIDTH / 2, 870), "箭头表示模型定义；未绘制位移、应力或拓扑优化结果。",
              fill=(90, 90, 90), font=small_font, anchor="mm")

    image.save(output, dpi=(200, 200), optimize=True)


def render_svg(output, png_name):
    # Keep labels editable while reusing the verified raster geometry layer.
    with Image.open(output.with_name(png_name)) as source:
        width, height = source.size
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
 width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>10w-3d 线弹性模型定义图</title>
  <image x="0" y="0" width="{width}" height="{height}" xlink:href="{png_name}"/>
</svg>
'''
    output.write_text(svg, encoding="utf-8")


def connected_components(tets):
    """Group volume nodes by element connectivity."""
    parent = {}
    size = {}

    def find(x):
        parent.setdefault(x, x)
        size.setdefault(x, 1)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    for _, _, tet in tets:
        for node in tet:
            find(node)
        union(tet[0], tet[1])
        union(tet[0], tet[2])
        union(tet[0], tet[3])

    groups = defaultdict(set)
    for node in parent:
        groups[find(node)].add(node)
    ordered = sorted(groups.values(), key=len, reverse=True)
    node_component = {node: idx + 1 for idx, group in enumerate(ordered) for node in group}
    return ordered, node_component


def view_basis(name):
    if name == "iso":
        return camera()
    if name == "xy":
        return np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])
    if name == "xz":
        return np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), np.array([0.0, -1.0, 0.0])
    if name == "yz":
        return np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0])
    raise ValueError(name)


def projection_for_bounds(bounds, width, height, basis, margin=0.08):
    right, up, view = basis
    centre = (bounds[0] + bounds[1]) / 2
    corners = np.array(
        [[x, y, z] for x in (bounds[0][0], bounds[1][0])
         for y in (bounds[0][1], bounds[1][1])
         for z in (bounds[0][2], bounds[1][2])]
    )
    q = corners - centre
    cuv = np.column_stack((q @ right, q @ up))
    span = np.maximum(np.ptp(cuv, axis=0), 1.0e-12)
    scale = min(width * (1 - 2 * margin) / span[0], height * (1 - 2 * margin) / span[1])
    uv_mid = (cuv.min(axis=0) + cuv.max(axis=0)) / 2

    def transform(points):
        qpts = np.asarray(points) - centre
        uv = np.column_stack((qpts @ right, qpts @ up))
        uv = (uv - uv_mid) * scale
        uv[:, 1] *= -1
        uv += np.array([width / 2, height / 2])
        return uv, qpts @ view

    return transform, scale


def raster_triangle(rgb, zbuffer, xy, depth, color):
    height, width = zbuffer.shape
    xmin = max(0, int(math.floor(float(xy[:, 0].min()))))
    xmax = min(width - 1, int(math.ceil(float(xy[:, 0].max()))))
    ymin = max(0, int(math.floor(float(xy[:, 1].min()))))
    ymax = min(height - 1, int(math.ceil(float(xy[:, 1].max()))))
    if xmin > xmax or ymin > ymax:
        return

    x0, y0 = xy[0]
    x1, y1 = xy[1]
    x2, y2 = xy[2]
    denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(float(denom)) < 1.0e-12:
        return
    xs = np.arange(xmin, xmax + 1, dtype=float) + 0.5
    ys = np.arange(ymin, ymax + 1, dtype=float) + 0.5
    xx, yy = np.meshgrid(xs, ys)
    w0 = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / denom
    w1 = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / denom
    w2 = 1.0 - w0 - w1
    inside = (w0 >= -1.0e-8) & (w1 >= -1.0e-8) & (w2 >= -1.0e-8)
    zz = w0 * depth[0] + w1 * depth[1] + w2 * depth[2]
    zview = zbuffer[ymin : ymax + 1, xmin : xmax + 1]
    update = inside & (zz > zview)
    if not np.any(update):
        return
    zview[update] = zz[update]
    patch = rgb[ymin : ymax + 1, xmin : xmax + 1]
    patch[update] = color


def render_zbuffer_panel(nodes, faces, bounds, size, view_name, loaded_keys=None, muted=False):
    width, height = size
    rgb = np.full((height, width, 3), 255, dtype=np.uint8)
    zbuffer = np.full((height, width), -np.inf, dtype=float)
    transform, scale = projection_for_bounds(bounds, width, height, view_basis(view_name))
    loaded_keys = loaded_keys or set()

    for item in faces:
        xyz, _, normal, pid, _ = face_geometry(item, nodes)
        xy, depth = transform(xyz)
        key = tuple(sorted(item[0]))
        if key in loaded_keys:
            color = LOAD_COLOR
        else:
            base = PID_COLORS.get(pid, (200, 200, 200))
            if muted:
                base = tuple(int(0.55 * c + 0.45 * 255) for c in base)
            color = shade(base, normal)
        raster_triangle(rgb, zbuffer, xy, depth, color)

    mask = np.isfinite(zbuffer)
    edge = mask & (
        ~np.roll(mask, 1, axis=0) | ~np.roll(mask, -1, axis=0)
        | ~np.roll(mask, 1, axis=1) | ~np.roll(mask, -1, axis=1)
    )
    rgb[edge] = (85, 91, 96)
    return Image.fromarray(rgb, "RGB"), transform, zbuffer, scale


def draw_axes(draw, origin, labels, font):
    origin = np.asarray(origin, dtype=float)
    vectors = (np.array([55.0, 0.0]), np.array([0.0, -55.0]))
    for vector, label in zip(vectors, labels):
        draw_arrow(draw, origin, origin + vector, (45, 45, 45), 3)
        draw.text(tuple(origin + vector * 1.18), label, fill=(45, 45, 45), font=font, anchor="mm")


def draw_projected_axes(draw, origin, view_name, font):
    right, up, _ = view_basis(view_name)
    axes = [("x", np.array([1.0, 0.0, 0.0])),
            ("y", np.array([0.0, 1.0, 0.0])),
            ("z", np.array([0.0, 0.0, 1.0]))]
    if view_name == "xy":
        axes = axes[:2]
    elif view_name == "xz":
        axes = [axes[0], axes[2]]
    elif view_name == "yz":
        axes = axes[1:]
    origin = np.asarray(origin, dtype=float)
    for label, axis in axes:
        vector = np.array([axis @ right, -(axis @ up)])
        norm = np.linalg.norm(vector)
        if norm < 1.0e-12:
            continue
        vector = vector / norm * 52
        draw_arrow(draw, origin, origin + vector, (45, 45, 45), 3)
        draw.text(tuple(origin + vector * 1.20), label, fill=(45, 45, 45), font=font, anchor="mm")


def paste_panel(canvas, panel_image, box):
    canvas.paste(panel_image, (box[0], box[1]))


def render_geometry_four_views(output, nodes, boundary, components, node_component):
    width, height = 2100, 1550
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas, "RGBA")
    title_font, label_font, small_font = load_fonts()
    all_xyz = np.array(list(nodes.values()))
    bounds = (all_xyz.min(axis=0), all_xyz.max(axis=0))
    boxes = [
        (70, 150, 1010, 725), (1090, 150, 2030, 725),
        (70, 825, 1010, 1400), (1090, 825, 2030, 1400),
    ]
    views = ["iso", "xy", "xz", "yz"]
    titles = ["(a) 轴测图", "(b) xy 投影", "(c) xz 投影", "(d) yz 投影"]
    dims = [
        "PID 材料分区", "Δx=200，Δy=319.947",
        "Δx=200，Δz=470", "Δy=319.947，Δz=470",
    ]
    axis_labels = [("x", "z"), ("x", "y"), ("x", "z"), ("y", "z")]
    draw.text((width / 2, 60), "10w-3d 几何与材料分区", fill=(25, 25, 25), font=title_font, anchor="mm")

    for box, view_name, subtitle, dim, axes in zip(boxes, views, titles, dims, axis_labels):
        pw, ph = box[2] - box[0], box[3] - box[1]
        panel, transform, _, _ = render_zbuffer_panel(nodes, boundary, bounds, (pw, ph), view_name)
        paste_panel(canvas, panel, box)
        draw.rectangle(box, outline=(205, 205, 205, 255), width=2)
        draw.text((box[0] + 18, box[1] + 15), subtitle, fill=(35, 35, 35), font=label_font)
        draw.text(((box[0] + box[2]) / 2, box[3] - 22), dim, fill=(65, 65, 65), font=small_font, anchor="mm")
        draw_projected_axes(draw, (box[2] - 92, box[3] - 78), view_name, small_font)

        if view_name == "iso":
            for idx, group in enumerate(components, 1):
                centre = np.mean([nodes[n] for n in group], axis=0)
                uv, _ = transform(np.array([centre]))
                p = uv[0] + np.array([box[0], box[1]])
                draw.ellipse((p[0] - 22, p[1] - 22, p[0] + 22, p[1] + 22),
                             fill=(255, 255, 255, 225), outline=(45, 45, 45, 255), width=2)
                draw.text(tuple(p), f"C{idx}", fill=(35, 35, 35), font=small_font, anchor="mm")

    y = 1470
    draw.rectangle((660, y - 12, 690, y + 12), fill=PID_COLORS[1] + (255,))
    draw.text((705, y), "PID 1 / MAT1 1", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.rectangle((1050, y - 12, 1080, y + 12), fill=PID_COLORS[2] + (255,))
    draw.text((1095, y), "PID 2 / MAT1 2", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.text((width - 60, height - 30), "undeformed geometry · unit not declared",
              fill=(95, 95, 95), font=small_font, anchor="rm")
    canvas.save(output, dpi=(200, 200), optimize=True)


def render_geometry_figure(output, nodes, boundary, components):
    width, height = 1900, 900
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas, "RGBA")
    title_font, label_font, small_font = load_fonts()
    all_xyz = np.array(list(nodes.values()))
    bounds = (all_xyz.min(axis=0), all_xyz.max(axis=0))
    boxes = [(55, 140, 915, 790), (985, 140, 1845, 790)]
    views = ["iso", "yz"]
    titles = ["(a) 轴测图", "(b) yz 投影"]
    notes = ["C1–C3：三个体网格连通分量", "Δy=319.947，Δz=470"]
    draw.text((width / 2, 55), "10w-3d 几何与材料分区", fill=(25, 25, 25), font=title_font, anchor="mm")

    for box, view_name, subtitle, note in zip(boxes, views, titles, notes):
        pw, ph = box[2] - box[0], box[3] - box[1]
        panel, transform, _, _ = render_zbuffer_panel(nodes, boundary, bounds, (pw, ph), view_name)
        paste_panel(canvas, panel, box)
        draw.rectangle(box, outline=(205, 205, 205, 255), width=2)
        draw.text((box[0] + 18, box[1] + 15), subtitle, fill=(35, 35, 35), font=label_font)
        draw.text(((box[0] + box[2]) / 2, box[3] - 22), note,
                  fill=(65, 65, 65), font=small_font, anchor="mm")
        draw_projected_axes(draw, (box[2] - 90, box[3] - 80), view_name, small_font)

        if view_name == "iso":
            for idx, group in enumerate(components, 1):
                centre = np.mean([nodes[n] for n in group], axis=0)
                uv, _ = transform(np.array([centre]))
                p = uv[0] + np.array([box[0], box[1]])
                draw.ellipse((p[0] - 22, p[1] - 22, p[0] + 22, p[1] + 22),
                             fill=(255, 255, 255, 225), outline=(45, 45, 45, 255), width=2)
                draw.text(tuple(p), f"C{idx}", fill=(35, 35, 35), font=small_font, anchor="mm")

    y = 850
    draw.rectangle((555, y - 12, 585, y + 12), fill=PID_COLORS[1] + (255,))
    draw.text((600, y), "PID 1 / MAT1 1", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.rectangle((985, y - 12, 1015, y + 12), fill=PID_COLORS[2] + (255,))
    draw.text((1030, y), "PID 2 / MAT1 2", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.text((width - 45, height - 22), "undeformed geometry · unit not declared",
              fill=(95, 95, 95), font=small_font, anchor="rm")
    canvas.save(output, dpi=(200, 200), optimize=True)


def render_boundary_figure(output, nodes, boundary, loaded, spc_nodes, components, node_component):
    width, height = 2100, 1400
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas, "RGBA")
    title_font, label_font, small_font = load_fonts()
    all_xyz = np.array(list(nodes.values()))
    bounds = (all_xyz.min(axis=0), all_xyz.max(axis=0))
    loaded_keys = {tuple(sorted(item[0])) for item in loaded}
    overview_box = (60, 145, 1320, 1260)
    pw, ph = overview_box[2] - overview_box[0], overview_box[3] - overview_box[1]
    overview, transform, _, scale = render_zbuffer_panel(
        nodes, boundary, bounds, (pw, ph), "iso", loaded_keys=loaded_keys, muted=True
    )
    paste_panel(canvas, overview, overview_box)
    draw.rectangle(overview_box, outline=(205, 205, 205, 255), width=2)
    draw.text((width / 2, 58), "10w-3d 载荷与位移约束", fill=(25, 25, 25), font=title_font, anchor="mm")
    draw.text((overview_box[0] + 20, overview_box[1] + 18), "(a) 整体边界条件",
              fill=(35, 35, 35), font=label_font)

    for nid in sorted(spc_nodes):
        uv, _ = transform(np.array([nodes[nid]]))
        p = uv[0] + np.array([overview_box[0], overview_box[1]])
        draw.ellipse((p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10),
                     fill=SPC_COLOR + (255,), outline=(255, 255, 255, 255), width=2)

    loaded_centres = []
    for item in loaded:
        _, centre, normal, _, _ = face_geometry(item, nodes)
        loaded_centres.append((centre, normal))
    selected = loaded_centres[::max(1, len(loaded_centres) // 8)][:8]
    for centre, normal in selected:
        uv, _ = transform(np.array([centre + normal * 20, centre]))
        uv += np.array([overview_box[0], overview_box[1]])
        draw_arrow(draw, uv[0], uv[1], LOAD_COLOR, 5)

    centre = (bounds[0] + bounds[1]) / 2
    grav_pair = np.array([centre, centre + np.array([0.0, -70.0, 0.0])])
    guv, _ = transform(grav_pair)
    guv += np.array([overview_box[0], overview_box[1]])
    draw_arrow(draw, guv[0], guv[1], (35, 35, 35), 5)
    draw.text(tuple(guv[1] + np.array([10.0, 0.0])), "a=(0,-9800,0)",
              fill=(35, 35, 35), font=small_font, anchor="lm")

    spc_by_component = defaultdict(list)
    for nid in spc_nodes:
        spc_by_component[node_component[nid]].append(nid)
    zoom_components = sorted(spc_by_component)
    zoom_boxes = [(1400, 145, 2040, 500), (1400, 555, 2040, 910), (1400, 965, 2040, 1320)]
    for zoom_idx, (cid, box) in enumerate(zip(zoom_components, zoom_boxes), 1):
        group = components[cid - 1]
        group_xyz = np.array([nodes[n] for n in group])
        group_bounds = (group_xyz.min(axis=0), group_xyz.max(axis=0))
        group_faces = [item for item in boundary if node_component[item[0][0]] == cid]
        pw, ph = box[2] - box[0], box[3] - box[1]
        panel, ztransform, _, _ = render_zbuffer_panel(
            nodes, group_faces, group_bounds, (pw, ph), "iso", loaded_keys=loaded_keys, muted=True
        )
        paste_panel(canvas, panel, box)
        draw.rectangle(box, outline=(205, 205, 205, 255), width=2)
        ids = sorted(spc_by_component[cid])
        draw.text((box[0] + 15, box[1] + 12), f"({chr(97 + zoom_idx)}) C{cid}：SPC 节点",
                  fill=(35, 35, 35), font=label_font)
        for nid in ids:
            uv, _ = ztransform(np.array([nodes[nid]]))
            p = uv[0] + np.array([box[0], box[1]])
            draw.ellipse((p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10),
                         fill=SPC_COLOR + (255,), outline=(255, 255, 255, 255), width=2)
        draw.text(((box[0] + box[2]) / 2, box[3] - 18),
                  "IDs: " + ", ".join(map(str, ids)),
                  fill=SPC_COLOR, font=small_font, anchor="mm")

    y = 1355
    draw.rectangle((250, y - 12, 280, y + 12), fill=LOAD_COLOR + (255,))
    draw.text((295, y), "Γp：909 个 PLOAD4 面，|tp|=0.25", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.ellipse((900, y - 9, 918, y + 9), fill=SPC_COLOR + (255,))
    draw.text((933, y), "Nc：9 个节点，g=(0.1,0.2,0.3)", fill=(45, 45, 45), font=small_font, anchor="lm")
    draw.text((width - 55, y), "undeformed geometry", fill=(95, 95, 95), font=small_font, anchor="rm")
    canvas.save(output, dpi=(200, 200), optimize=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--boundary-output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    nodes, tets, spc_nodes, pload = read_bdf(args.input)
    boundary = exterior_faces(tets)
    loaded = select_loaded_faces(boundary, pload)
    components, node_component = connected_components(tets)
    used_nodes = {node for _, _, tet in tets for node in tet}
    unused_nodes = sorted(set(nodes) - used_nodes)
    if (len(nodes), len(tets), len(spc_nodes), len(pload), len(loaded)) != (43209, 221599, 9, 909, 909):
        raise RuntimeError("BDF statistics differ from the documented model")

    boundary_output = args.boundary_output or args.output.with_name("10w-3d-boundary-conditions.png")
    boundary_output.parent.mkdir(parents=True, exist_ok=True)
    four_view_output = args.output.with_name("10w-3d-model-four-views.png")
    render_geometry_figure(args.output, nodes, boundary, components)
    render_geometry_four_views(four_view_output, nodes, boundary, components, node_component)
    render_boundary_figure(
        boundary_output, nodes, boundary, loaded, spc_nodes, components, node_component
    )
    svg_output = args.output.with_suffix(".svg")
    boundary_svg = boundary_output.with_suffix(".svg")
    four_view_svg = four_view_output.with_suffix(".svg")
    render_svg(svg_output, args.output.name)
    render_svg(four_view_svg, four_view_output.name)
    render_svg(boundary_svg, boundary_output.name)
    print(f"GRID={len(nodes)}, CTETRA={len(tets)}, exterior_faces={len(boundary)}")
    print(f"SPC_nodes={len(spc_nodes)}, PLOAD4_faces={len(loaded)}")
    print(f"connected_components={len(components)}, component_nodes={[len(c) for c in components]}")
    print(f"unused_GRID={unused_nodes}")
    print(args.output)
    print(svg_output)
    print(four_view_output)
    print(four_view_svg)
    print(boundary_output)
    print(boundary_svg)


if __name__ == "__main__":
    main()
