import math
import random

import pygame


class Ripple:
    """Expanding concentric ring on the water surface (world coordinates)."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.radius = 3.0
        self.max_radius = 55.0
        self.alpha = 200
        self.speed = 1.6

    def update(self):
        self.radius += self.speed
        self.alpha = max(0, int(200 * (1.0 - self.radius / self.max_radius)))

    @property
    def alive(self) -> bool:
        return self.alpha > 0


class SplashDrop:
    """Airborne water droplet launched on splash impact (world coordinates)."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(-math.pi + 0.3, -0.3)  # upward fan
        speed = random.uniform(3, 11)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = random.randint(2, 5)
        self.alpha = 230

    def update(self):
        self.vy += 0.4  # gravity
        self.vx *= 0.98  # air resistance
        self.x += self.vx
        self.y += self.vy
        self.alpha = max(0, self.alpha - 7)

    @property
    def alive(self) -> bool:
        return self.alpha > 0


class WaterBody:
    """
    Spring-based water simulation using Hooke's law  (F = -kx).

    Each column of the water surface is a damped harmonic oscillator.
    Adjacent springs exchange energy, propagating waves laterally.

    • Water is completely flat at rest – no idle animation.
    • A player landing pushes springs down proportional to impact speed.
    • Waves naturally decay back to flat via the DAMPING coefficient.
    • Translucent gradient body rendered with a SRCALPHA surface.
    """

    # ---- spring parameters ----
    K = 0.025  # restoring-force constant  (F = -K * x)
    SPREAD = 0.25  # lateral coupling between adjacent springs
    DAMPING = 0.985  # velocity multiplier per frame  (< 1 → decay to flat)

    # ---- geometry ----
    COLUMN_W = 8  # world pixels represented by each spring column

    # ---- colours ----
    SURFACE_COLOR = (45, 155, 255)  # near-surface tint
    DEEP_COLOR = (10, 55, 140)  # deep-water tint
    CREST_COLOR = (190, 230, 255)  # wave-crest highlight
    DROP_COLOR = (120, 200, 255)  # splash droplet colour
    BASE_ALPHA = 160  # overall translucency (0-255)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))

        n = max(2, (self.rect.width + self.COLUMN_W - 1) // self.COLUMN_W)
        self.n = n
        self.displace = [0.0] * n  # spring displacement in px (+ = downward)
        self.vel = [0.0] * n  # spring velocity

        self.ripples: list[Ripple] = []
        self.drops: list[SplashDrop] = []
        self._inside = False  # debounce: was player inside last frame?

    # ------------------------------------------------------------------ #
    #  Public interface                                                    #
    # ------------------------------------------------------------------ #

    def update(self, player_hitbox: pygame.Rect, velocity_y: float) -> bool:
        """
        Advance one physics frame.
        Returns True on the frame the player first contacts the water surface
        so the caller can play a splash sound.  No death is triggered here.
        """
        self._step()

        self.ripples = [r for r in self.ripples if r.alive]
        self.drops = [d for d in self.drops if d.alive]
        for r in self.ripples:
            r.update()
        for d in self.drops:
            d.update()

        # Thin band at the water's top surface for entry detection
        entry_band = pygame.Rect(self.rect.x, self.rect.y - 6, self.rect.width, 14)
        touching = player_hitbox.colliderect(self.rect)
        entered = (
            velocity_y > 0
            and player_hitbox.colliderect(entry_band)
            and not self._inside
        )
        self._inside = touching

        if entered:
            cx = player_hitbox.centerx
            self._impact(cx, velocity_y)
            self._spawn_visual_splash(cx, self.rect.top)

        return entered

    def draw(self, win: pygame.Surface, scroll: list):
        """Render the water body and any active particles onto win."""
        sw, sh = win.get_size()
        sx = self.rect.x - scroll[0]
        sy = self.rect.y - scroll[1]

        # Clip to screen bounds
        vis_x1 = max(0, sx)
        vis_x2 = min(sw, sx + self.rect.width)
        vis_y1 = max(0, sy)
        vis_y2 = min(sh, sy + self.rect.height)
        if vis_x2 <= vis_x1 or vis_y2 <= vis_y1:
            return

        vis_w = int(vis_x2 - vis_x1)
        vis_h = int(vis_y2 - vis_y1)

        # Position of the visible strip within the water rect
        wx_base = int(vis_x1 - sx)  # x offset inside the water rect
        wy_base = int(vis_y1 - sy)  # y offset inside the water rect (top of strip)

        surf = pygame.Surface((vis_w, vis_h), pygame.SRCALPHA)

        # ---- 1. Gradient fill across the entire surf area ----
        sc, dc = self.SURFACE_COLOR, self.DEEP_COLOR
        wh = self.rect.height
        for row in range(vis_h):
            t = (wy_base + row) / max(wh - 1, 1)
            cr = int(sc[0] + (dc[0] - sc[0]) * t)
            cg = int(sc[1] + (dc[1] - sc[1]) * t)
            cb = int(sc[2] + (dc[2] - sc[2]) * t)
            a = int(self.BASE_ALPHA * (1.0 - t * 0.15))
            surf.fill((cr, cg, cb, a), (0, row, vis_w, 1))

        # ---- 2. Wave surface points (one per screen column) ----
        surface_pts = []
        for px in range(vis_w):
            rect_x = wx_base + px
            col_f = rect_x / self.COLUMN_W
            col = int(col_f)
            frac = col_f - col
            c0 = max(0, min(self.n - 1, col))
            c1 = max(0, min(self.n - 1, col + 1))
            # Linear interpolation between adjacent springs
            d = self.displace[c0] * (1.0 - frac) + self.displace[c1] * frac
            surf_y = max(0, min(vis_h - 1, int(wy_base + d)))
            surface_pts.append((px, surf_y))

        # ---- 3. Erase gradient above the wave surface ----
        # Build a polygon covering the area above the wave, then subtract its
        # alpha channel from surf so only the water body is visible.
        if surface_pts:
            above_poly = [(0, 0)] + surface_pts + [(vis_w - 1, 0)]
            clip_surf = pygame.Surface((vis_w, vis_h), pygame.SRCALPHA)
            pygame.draw.polygon(clip_surf, (0, 0, 0, 255), above_poly)
            surf.blit(clip_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        # ---- 4. Wave-crest highlight line ----
        if len(surface_pts) >= 2:
            pygame.draw.lines(surf, (*self.CREST_COLOR, 220), False, surface_pts, 2)

        # ---- 5. Ripple rings ----
        for rip in self.ripples:
            rx = int(rip.x - scroll[0] - vis_x1)
            ry = int(rip.y - scroll[1] - vis_y1)
            if rip.alpha > 0:
                pygame.draw.circle(
                    surf, (255, 255, 255, rip.alpha), (rx, ry), int(rip.radius), 2
                )

        win.blit(surf, (int(vis_x1), int(vis_y1)))

        # ---- 6. Splash droplets (drawn on win; may fly above water level) ----
        for drop in self.drops:
            dx = int(drop.x - scroll[0])
            dy = int(drop.y - scroll[1])
            if drop.alpha > 0:
                r2 = drop.radius
                ds = pygame.Surface((r2 * 2, r2 * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    ds, (*self.DROP_COLOR, int(drop.alpha)), (r2, r2), r2
                )
                win.blit(ds, (dx - r2, dy - r2))

    # ------------------------------------------------------------------ #
    #  Private                                                             #
    # ------------------------------------------------------------------ #

    def _step(self):
        """
        One step of Hooke's-law spring simulation with lateral spreading.

        For each spring i:
            F_restore  = -K * x[i]              (pulls back to zero)
            F_spread   = SPREAD * (x[i-1] - x[i]) + SPREAD * (x[i+1] - x[i])
            a[i]       = F_restore + F_spread
            v[i]       = v[i] * DAMPING + a[i]  (velocity decays each frame)
            x[i]      += v[i]
        """
        acc = [0.0] * self.n
        for i in range(self.n):
            acc[i] = -self.K * self.displace[i]
            if i > 0:
                acc[i] += self.SPREAD * (self.displace[i - 1] - self.displace[i])
            if i < self.n - 1:
                acc[i] += self.SPREAD * (self.displace[i + 1] - self.displace[i])

        for i in range(self.n):
            self.vel[i] = self.vel[i] * self.DAMPING + acc[i]
            self.displace[i] += self.vel[i]

    def _impact(self, world_x: float, velocity_y: float):
        """
        Push springs downward at world_x.
        Impact strength is proportional to the player's falling speed.
        """
        col = int((world_x - self.rect.x) / self.COLUMN_W)
        col = max(0, min(self.n - 1, col))
        push = min(velocity_y * 1.2, 18.0)

        self.vel[col] += push
        if col > 0:
            self.vel[col - 1] += push * 0.6
        if col > 1:
            self.vel[col - 2] += push * 0.25
        if col < self.n - 1:
            self.vel[col + 1] += push * 0.6
        if col < self.n - 2:
            self.vel[col + 2] += push * 0.25

    def _spawn_visual_splash(self, cx: float, cy: float):
        """Airborne droplets centred at (cx, cy) – no ripple rings."""
        for _ in range(22):
            self.drops.append(SplashDrop(cx, cy))
