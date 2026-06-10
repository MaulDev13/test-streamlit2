"""
calculations.py
Modul perhitungan GPP dan rekomendasi beban latihan.
Menggunakan metode numerik: Fixed Point Iteration + Epley 1RM.
"""

from __future__ import annotations


# ════════════════════════════════════════════════════════════════════════════
# TAHAP 1: GPP
# ════════════════════════════════════════════════════════════════════════════

def hitung_gpp(pushup: int, situp: int, lari: int) -> dict:
    """
    Hitung nilai GPP berdasarkan push-up, sit-up, dan lari 12 menit.

    Rumus:
        S_PU = (pushup / 60) * 100   (maks 100)
        S_SU = (situp  / 60) * 100   (maks 100)
        S_L  = (lari   / 3000) * 100 (maks 100)
        GPP  = 0.4*S_L + 0.3*S_PU + 0.3*S_SU
    """
    s_pu = min((pushup / 60) * 100, 100.0)
    s_su = min((situp  / 60) * 100, 100.0)
    s_l  = min((lari   / 3000) * 100, 100.0)
    gpp  = 0.4 * s_l + 0.3 * s_pu + 0.3 * s_su

    return {
        "pushup": pushup,
        "situp":  situp,
        "lari":   lari,
        "s_pu":   round(s_pu, 2),
        "s_su":   round(s_su, 2),
        "s_l":    round(s_l, 2),
        "gpp":    round(gpp, 2),
    }


# ════════════════════════════════════════════════════════════════════════════
# TAHAP 2: ESTIMASI 1RM — EPLEY
# ════════════════════════════════════════════════════════════════════════════

def hitung_1rm(beban: float, repetisi: int) -> float:
    """
    Hitung estimasi 1RM menggunakan rumus Epley:
        1RM = W * (1 + R / 30)
    """
    return round(beban * (1 + repetisi / 30), 2)


# ════════════════════════════════════════════════════════════════════════════
# TAHAP 3: INTENSITAS BERDASARKAN GPP
# ════════════════════════════════════════════════════════════════════════════

_INTENSITY_TABLE = [
    (0,  50,  0.55, "< 50"),
    (50, 60,  0.65, "50–60"),
    (60, 70,  0.70, "60–70"),
    (70, 80,  0.75, "70–80"),
    (80, 90,  0.80, "80–90"),
    (90, 200, 0.85, "> 90"),
]


def tentukan_intensitas(gpp: float) -> dict:
    """
    Kembalikan persentase intensitas (dari 1RM) berdasarkan skor GPP.
    """
    for lo, hi, pct, label in _INTENSITY_TABLE:
        if lo <= gpp < hi:
            return {"pct": pct, "range": label}
    return {"pct": 0.55, "range": "< 50"}


# ════════════════════════════════════════════════════════════════════════════
# MODEL RPE SEDERHANA (estimasi internal)
# ════════════════════════════════════════════════════════════════════════════

def _estimasi_rpe(beban: float, beban_awal: float, rpe_awal: float = 6.0) -> float:
    """
    Estimasi RPE secara linier relatif terhadap beban awal.
    Setiap kenaikan 2.5% dari beban awal ≈ +0.5 RPE.
    """
    if beban_awal == 0:
        return rpe_awal
    rasio = (beban - beban_awal) / beban_awal
    rpe   = rpe_awal + rasio * 20          # skala sederhana
    return round(max(1.0, min(10.0, rpe)), 2)


# ════════════════════════════════════════════════════════════════════════════
# TAHAP 5: FIXED POINT ITERATION — BEBAN
# ════════════════════════════════════════════════════════════════════════════

def iterasi_beban(
    beban_awal: float,
    rpe_target: float = 8.0,
    k: float = 2.0,
    max_iter: int = 15,
    tol_rpe: float = 0.5,
    tol_w: float = 0.5,
) -> dict:
    """
    Fixed Point Iteration untuk menyesuaikan beban terhadap target RPE.

    Algoritma:
        W(n+1) = W(n) + k * (RPE_t - RPE(n))

    Konvergensi jika:
        |RPE_t - RPE(n)| < tol_rpe  ATAU  |W(n+1) - W(n)| < tol_w

    RPE diestimasi secara relatif terhadap beban awal
    (RPE awal diasumsikan = 6.0 pada beban_awal).
    """
    w        = beban_awal
    rpe_init = 6.0
    history  = []
    converged_at = max_iter

    for i in range(max_iter):
        rpe_n   = _estimasi_rpe(w, beban_awal, rpe_init)
        delta_rpe = abs(rpe_target - rpe_n)
        w_new   = w + k * (rpe_target - rpe_n)
        delta_w = abs(w_new - w)

        history.append([i, round(w, 2), round(rpe_n, 2),
                        round(delta_rpe, 3), round(delta_w, 3)])

        if delta_rpe < tol_rpe or delta_w < tol_w:
            converged_at = i
            w = w_new
            break

        w = max(0.0, w_new)
    else:
        rpe_n = _estimasi_rpe(w, beban_awal, rpe_init)

    return {
        "history":       history,
        "final_weight":  round(w, 2),
        "final_rpe":     round(_estimasi_rpe(w, beban_awal, rpe_init), 2),
        "converged_at":  converged_at,
    }


# ════════════════════════════════════════════════════════════════════════════
# TAHAP 6: PULL-UP — ITERASI REPETISI
# ════════════════════════════════════════════════════════════════════════════

def iterasi_pullup(
    rep_awal: int,
    berat_badan: float,
    rep_target: int = 10,
    max_iter: int = 30,
) -> dict:
    """
    Iterasi progresi repetisi pull-up.

    R(n+1) = R(n) + 0.2 * (R_t - R(n))

    Jika rep_awal >= rep_target, rekomendasikan weighted pull-up
    dengan beban tambahan = 5% berat badan.
    """
    r       = float(rep_awal)
    history = []
    converged = False

    for i in range(max_iter):
        delta = rep_target - r
        r_new = r + 0.2 * delta
        history.append([i, round(r, 2), round(abs(delta), 3)])

        if abs(delta) < 0.5:
            converged = True
            break
        r = r_new

    weighted     = rep_awal >= rep_target
    extra_weight = round(0.05 * berat_badan, 2)

    return {
        "history":      history,
        "target_rep":   rep_target,
        "final_rep":    round(r, 1),
        "weighted":     weighted,
        "extra_weight": extra_weight,
        "converged":    converged,
    }