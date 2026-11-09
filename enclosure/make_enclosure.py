"""
make_enclosure.py  -  generates the printable parts for the repositioning patch.

    python make_enclosure.py

writes five STL files next to this script:

    bedside_box_base.stl   holds the Pico on its Grove shield, the half-size breadboard,
                           the amplifier and the speaker. Grille and button hole in the front wall,
                           cable opening in the back wall.
    bedside_box_lid.stl    friction-fit lid with the window for the NeoPixel ring.
    light_diffuser.stl     thin disc that sits flush in the window. Print in white or natural PLA.
    sensor_pod.stl         shell around the LSM6DS3TR-C board, with the key tab.
    sensor_pod_cap.stl     press-fit cap for the pod, with an arrow pointing to the head.
    body_cradle.stl        taped to the chest. The pod clicks in one way only.
    jig_cradle.stl         the same seat with screw holes, for the protractor jig.

Every dimension that depends on a part is a parameter at the top. Measure your parts with the
calipers, change the numbers, and run the script again.

Needs:  pip install manifold3d trimesh numpy
"""
import os

import numpy as np
import trimesh
from manifold3d import CrossSection, JoinType, Manifold

HERE = os.path.dirname(os.path.abspath(__file__))

# =============================================================== parameters (mm)
CLEAR = 0.25            # gap between parts that slide together. Raise to 0.35 if fits are tight

# --- parts inside the bedside box (measure these)
SHIELD = 56.9           # Grove Shield for Pi Pico, square (measured)
BREADBOARD = (82.5, 54.5)
RING_OD = 44.4          # NeoPixel Ring 16 outer diameter (measured)
RING_ID = 31.0          # inner diameter (measured)
DIFFUSER_D = 48.0       # printed light window that sits flush in the lid over the ring
DIFFUSER_T = 1.0        # thin enough that the ring glows through white or natural PLA
BUTTON_THREAD = 19.1    # widest part of the button that passes through the wall (measured)
SPEAKER_GRILLE_D = 36.0 # area of holes in front of the speaker cone
SPEAKER = 40.8          # square speaker body (measured)
SPEAKER_SCREWS = 46.0   # distance between the two mounting holes, left and right (measured)
SPEAKER_EAR_DEPTH = 7.6 # front face of the speaker to the mounting ears (measured)
SCREW_PILOT = 2.2       # pilot hole for a small self-tapping screw (M2.5 or #4)

# --- bedside box
USB_SLOT = (16.0, 14.0) # width and height of the USB opening in the left wall (cable plug end is about 12 x 8)
USB_SLOT_Z = 6.0        # bottom of the opening, above the floor
WALL = 2.4
FLOOR = 2.4
INNER = (155.0, 95.0, 55.0)     # inside width, depth, height (extra room for the speaker)
CORNER_R = 6.0
LID_T = 2.4
LIP_H = 4.0
LIP_T = 1.6

# --- sensor pod
BOARD = (18.0 + 0.6, 25.5 + 0.6)   # LSM6DS3TR-C breakout 18.0 x 25.5 (measured) plus room, x by y
BOARD_SPACE_H = 6.3     # board plus the STEMMA QT connectors
POD_WALL = 1.6
POD_FLOOR = 1.2
CABLE_SLOT_W = 9.0      # STEMMA QT plug is about 6.5 mm wide
KEY_W, KEY_OUT, KEY_Y = 4.0, 1.6, 6.0   # key tab width, how far it sticks out, offset toward the head

# --- cradle
CRADLE = (60.0, 44.0)   # flange, x by y
CRADLE_T = 1.6
CRADLE_WALL = 1.8
CRADLE_WALL_H = 4.5
STRAP_SLOT = (3.0, 18.0)
JIG_SCREW_D = 3.4       # M3 clearance

SEG = 96                # smoothness of circles


# =============================================================== helpers
def box(x, y, z, cx=0.0, cy=0.0, z0=0.0):
    return Manifold.cube((x, y, z), center=True).translate((cx, cy, z0 + z / 2))


def rounded(x, y, z, r, cx=0.0, cy=0.0, z0=0.0):
    r = min(r, x / 2 - 0.01, y / 2 - 0.01)
    cs = CrossSection.square((x - 2 * r, y - 2 * r), center=True).offset(r, JoinType.Round, circular_segments=SEG)
    return cs.extrude(z).translate((cx, cy, z0))


def cyl(d, h, cx=0.0, cy=0.0, z0=0.0):
    return Manifold.cylinder(h, d / 2, d / 2, SEG).translate((cx, cy, z0))


def ycyl(d, length, cx, cy, cz):
    """Cylinder lying along y (for holes through the front or back wall)."""
    return Manifold.cylinder(length, d / 2, d / 2, SEG).rotate((-90, 0, 0)).translate((cx, cy, cz))


def union(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out


def triangle(w, h, t, cx, cy, z0, pointing=1):
    """Flat isosceles triangle pointing toward +y (pointing=1) or -y."""
    pts = [(-w / 2, -pointing * h / 2), (w / 2, -pointing * h / 2), (0, pointing * h / 2)]
    if pointing < 0:
        pts = pts[::-1]
    return CrossSection([pts]).extrude(t).translate((cx, cy, z0))


def save(m, name):
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts))
    path = os.path.join(HERE, name)
    tm.export(path)
    lo, hi = tm.bounds
    print("%-24s %6.1f x %5.1f x %5.1f mm   watertight=%s" % (name, *(hi - lo), tm.is_watertight))
    return tm


# =============================================================== bedside box
IX, IY, IH = INNER
OX, OY = IX + 2 * WALL, IY + 2 * WALL
FRONT_ZONE = 25.0       # strip along the front wall kept clear for the speaker and button


def bedside_base():
    shell = rounded(OX, OY, FLOOR + IH, CORNER_R) - rounded(IX, IY, IH + 1, CORNER_R - WALL, z0=FLOOR)

    # coordinates inside: x from -IX/2 (left) to +IX/2, y from -IY/2 (front) to +IY/2 (back)
    left, back = -IX / 2, IY / 2

    # low fences that locate the shield (back left) and the breadboard (back right)
    sx0, sy1 = left + 4, back - 2
    sh = SHIELD + 2 * CLEAR
    shield_fence = (rounded(sh + 3.2, sh + 3.2, 3, 1, cx=sx0 + sh / 2, cy=sy1 - sh / 2, z0=FLOOR)
                    - box(sh, sh, 10, cx=sx0 + sh / 2, cy=sy1 - sh / 2, z0=FLOOR)
                    - box(20, sh + 10, 10, cx=sx0 + sh / 2, cy=sy1 - sh / 2, z0=FLOOR)
                    - box(sh + 10, 20, 10, cx=sx0 + sh / 2, cy=sy1 - sh / 2, z0=FLOOR))
    bx, by = BREADBOARD[0] + 2 * CLEAR, BREADBOARD[1] + 2 * CLEAR
    bcx, bcy = sx0 + sh + 6 + bx / 2, sy1 - by / 2
    bb_fence = (rounded(bx + 3.2, by + 3.2, 3, 1, cx=bcx, cy=bcy, z0=FLOOR)
                - box(bx, by, 10, cx=bcx, cy=bcy, z0=FLOOR)
                - box(30, by + 10, 10, cx=bcx, cy=bcy, z0=FLOOR)
                - box(bx + 10, 24, 10, cx=bcx, cy=bcy, z0=FLOOR))

    base = shell + shield_fence + bb_fence

    # back wall: one opening for the USB cable and the sensor cable, behind the shield
    base = base - rounded(50, WALL * 4, 16, 3, cx=sx0 + sh / 2, cy=back + WALL / 2, z0=FLOOR + 6)

    # left wall: opening for the Pico's USB plug, level with the middle of the shield,
    # since the Pico sits centred on the shield. Tall enough for the plug to pass through
    base = base - rounded(WALL * 4, USB_SLOT[0], USB_SLOT[1], 2.5, cx=left - WALL / 2, cy=sy1 - sh / 2, z0=FLOOR + USB_SLOT_Z)

    # front wall: speaker grille and the acknowledge button
    fy = -IY / 2 - WALL - 1
    zc = FLOOR + IH / 2
    gx = -5.0
    holes = []
    pitch = 4.6
    for row in range(-5, 6):
        for col in range(-5, 6):
            x = col * pitch + (pitch / 2 if row % 2 else 0)
            z = row * pitch * 0.866
            if x * x + z * z <= (SPEAKER_GRILLE_D / 2 - 1.6) ** 2:
                holes.append(ycyl(3.0, WALL + 2, gx + x, fy, zc + z))
    base = base - union(holes)

    # two posts on the inside of the front wall. The speaker face presses against the grille,
    # and its ears land on the end of the posts, where a small screw holds each one
    wall_in = -IY / 2
    for s in (-1, 1):
        post = ycyl(7.0, SPEAKER_EAR_DEPTH + 0.2, gx + s * SPEAKER_SCREWS / 2, wall_in - 0.2, zc)
        hole = ycyl(SCREW_PILOT, SPEAKER_EAR_DEPTH + 1, gx + s * SPEAKER_SCREWS / 2, wall_in + 0.6, zc)
        base = base + post - hole
    # shallow square pocket so the speaker face sits centred on the grille
    base = base + (box(SPEAKER + 2 * CLEAR + 3.2, 1.6, SPEAKER + 2 * CLEAR + 3.2, gx, wall_in + 0.8, zc - (SPEAKER + 2 * CLEAR + 3.2) / 2)
                   - box(SPEAKER + 2 * CLEAR, 4, SPEAKER + 2 * CLEAR, gx, wall_in + 0.8, zc - (SPEAKER + 2 * CLEAR) / 2)
                   - box(SPEAKER + 10, 4, 10, gx, wall_in + 0.8, zc - 5)
                   - box(10, 4, SPEAKER + 10, gx, wall_in + 0.8, zc - (SPEAKER + 10) / 2))

    base = base - ycyl(BUTTON_THREAD + 0.5, WALL + 2, IX / 2 - 24, fy, zc)
    return base


def bedside_lid():
    plate = rounded(OX, OY, LID_T, CORNER_R)
    # lip that drops inside the walls and holds the lid by friction
    lx, ly = IX - 2 * CLEAR, IY - 2 * CLEAR
    lip = (rounded(lx, ly, LIP_H, CORNER_R - WALL, z0=-LIP_H)
           - rounded(lx - 2 * LIP_T, ly - 2 * LIP_T, LIP_H + 1, max(1, CORNER_R - WALL - LIP_T), z0=-LIP_H - 0.5))
    lid = plate + lip

    # ring window above the shield. The ring sits in a short collar under the lid,
    # and a thin printed diffuser disc sits flush in a recess on top
    rx = -IX / 2 + 4 + SHIELD / 2
    ry = IY / 2 - 2 - SHIELD / 2
    collar_in = RING_OD + 2 * CLEAR + 0.4
    collar = cyl(collar_in + 3.2, 5, rx, ry, -5) - cyl(collar_in, 7, rx, ry, -6)
    collar = collar - box(10, 40, 10, rx, ry - collar_in / 2, -6)        # gap for the ring's wires
    lid = lid + collar
    lid = lid - cyl(RING_OD - 1.0, LID_T + 2, rx, ry, -1)                        # window the LEDs shine through
    lid = lid - cyl(DIFFUSER_D + 2 * CLEAR, DIFFUSER_T + 1, rx, ry, LID_T - DIFFUSER_T)   # recess for the diffuser
    return lid


def diffuser():
    return cyl(DIFFUSER_D, DIFFUSER_T)


# =============================================================== sensor pod and cradle
PX = BOARD[0] + 2 * POD_WALL
PY = BOARD[1] + 2 * POD_WALL
PH = POD_FLOOR + BOARD_SPACE_H


def sensor_pod():
    body = rounded(PX, PY, PH, 2.5) - rounded(BOARD[0], BOARD[1], PH, 1.0, z0=POD_FLOOR)
    # cable slot at the feet end (-y)
    body = body - box(CABLE_SLOT_W, POD_WALL * 3, PH, cy=-PY / 2, z0=POD_FLOOR + 0.8)
    # key tab on the +x side, offset toward the head, so the pod fits the cradle one way only
    body = body + rounded(KEY_OUT * 2 + 1, KEY_W, PH - 1.0, 0.6, cx=PX / 2 + KEY_OUT / 2 - 0.5, cy=KEY_Y)
    return body


def sensor_pod_cap():
    cap = rounded(PX, PY, 1.4, 2.5)
    lip = (rounded(BOARD[0] - 2 * 0.2, BOARD[1] - 2 * 0.2, 1.5, 1.0, z0=-1.5)
           - rounded(BOARD[0] - 2 * 0.2 - 2.4, BOARD[1] - 2 * 0.2 - 2.4, 2, 0.6, z0=-1.8))
    lip = lip - box(CABLE_SLOT_W + 2, 6, 3, cy=-BOARD[1] / 2, z0=-2)    # do not block the cable
    cap = cap + lip
    cap = cap - triangle(8, 9, 0.7, 0, 3, 1.4 - 0.7, 1)                 # arrow to the head
    return cap


def cradle(for_jig=False):
    plate = rounded(CRADLE[0], CRADLE[1], CRADLE_T, 8)
    ix, iy = PX + 2 * CLEAR, PY + 2 * CLEAR
    walls = (rounded(ix + 2 * CRADLE_WALL, iy + 2 * CRADLE_WALL, CRADLE_WALL_H, 3, z0=CRADLE_T)
             - rounded(ix, iy, CRADLE_WALL_H + 1, 2.5 + CLEAR, z0=CRADLE_T - 0.5))
    # snap bumps near the top of the long walls, 0.4 mm into the opening
    bumps = union([box(0.8, 8, 0.8, cx=s * (ix / 2 - 0.0), cy=-4, z0=CRADLE_T + CRADLE_WALL_H - 1.4) for s in (-1, 1)])
    walls = walls + bumps
    # notch for the key tab, and an opening at the feet end for the cable
    walls = walls - box(KEY_OUT * 4, KEY_W + 2 * CLEAR + 0.2, CRADLE_WALL_H + 2,
                        cx=ix / 2 + CRADLE_WALL / 2, cy=KEY_Y, z0=CRADLE_T)
    walls = walls - box(CABLE_SLOT_W + 2, CRADLE_WALL * 3, CRADLE_WALL_H + 2, cy=-iy / 2 - CRADLE_WALL / 2, z0=CRADLE_T)
    part = plate + walls

    # raised arrows pointing to the head, between the pod and the strap slots
    ax = (ix / 2 + CRADLE_WALL + CRADLE[0] / 2 - 6) / 2
    part = part + triangle(6, 7, 0.8, -ax, 6, CRADLE_T) + triangle(6, 7, 0.8, ax, 6, CRADLE_T)

    if for_jig:
        part = part - cyl(JIG_SCREW_D, 10, -CRADLE[0] / 2 + 6, -12, -1) - cyl(JIG_SCREW_D, 10, CRADLE[0] / 2 - 6, -12, -1)
    else:
        sx = CRADLE[0] / 2 - 5
        part = part - box(STRAP_SLOT[0], STRAP_SLOT[1], 10, cx=-sx, z0=-1) - box(STRAP_SLOT[0], STRAP_SLOT[1], 10, cx=sx, z0=-1)
    return part


if __name__ == "__main__":
    save(bedside_base(), "bedside_box_base.stl")
    lid = bedside_lid()
    # flip the lid so it prints top face down, lip and collar up
    save(lid.rotate((180, 0, 0)).translate((0, 0, LID_T)), "bedside_box_lid.stl")
    save(diffuser(), "light_diffuser.stl")
    save(sensor_pod(), "sensor_pod.stl")
    save(sensor_pod_cap().rotate((180, 0, 0)).translate((0, 0, 1.4)), "sensor_pod_cap.stl")
    save(cradle(False), "body_cradle.stl")
    save(cradle(True), "jig_cradle.stl")
