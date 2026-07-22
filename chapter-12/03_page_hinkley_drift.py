"""Chapter 12 - Page-Hinkley drift detector.

The Page-Hinkley test flags a persistent shift in the mean of a
quality-score stream. It is cheap enough to run in an hour, and it is
a good first drift detector for an agent's judge scores over time.

No API key needed -- this runs on a simulated score stream.

Run:
    python 03_page_hinkley_drift.py
"""
import random


def page_hinkley(scores, delta=0.005, lam=0.05):
    mean, n, m_t, min_m = 0.0, 0, 0.0, 0.0
    alarms = []
    for t, x in enumerate(scores):
        n += 1
        mean += (x - mean) / n
        m_t += (x - mean - delta)
        min_m = min(min_m, m_t)
        if m_t - min_m > lam:
            alarms.append(t)
            mean, n, m_t, min_m = 0.0, 0, 0.0, 0.0  # reset
    return alarms


def simulate_scores(n=1000, drift_at=500, seed=0):
    """Illustrative helper (not in the book): simulate quality scores
    that drop after `drift_at`, to demonstrate the detector above."""
    rng = random.Random(seed)
    scores = []
    for t in range(n):
        base = 0.9 if t < drift_at else 0.6
        scores.append(max(0.0, min(1.0, base + rng.gauss(0, 0.05))))
    return scores


if __name__ == "__main__":
    scores = simulate_scores(n=1000, drift_at=500)
    alarms = page_hinkley(scores)
    print(f"Alarms raised at steps: {alarms}")
