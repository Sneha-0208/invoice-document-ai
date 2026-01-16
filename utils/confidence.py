def compute_confidence(dealer, model, hp, cost, stamp, signature):
    conf = 1.0

    # Core business fields
    if not dealer:
        conf -= 0.30
    if not model:
        conf -= 0.30
    if not cost:
        conf -= 0.30

    # Secondary numeric field
    if not hp:
        conf -= 0.10

    # Verification fields
    if not stamp:
        conf -= 0.15
    if not signature:
        conf -= 0.15

    return round(max(conf, 0.0), 2)
