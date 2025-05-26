# Setting payoff matrix dictionary
prisoner_payoffs = {
    "MM": (4,4),
    "MF": (-1,5),
    "FM": (5,-1),
    "FF": (1,1)
}

# Defining lists for lookup
strategies = list(("MMM", "MMF", "MFM", "MFF", "FMM", "MMF", "FFM", "FFF"))
strategies_minus_i = strategies

def repeated_payoff(s_i: str, s_j: str, delta: float) -> tuple[float,float]:
    """
    Compute (v_i, v_j) = stage1_payoff + delta * stage2_payoff
    for strategies s_i, s_j (each a 3‐char string “XYZ”):
      • s[0] = action in period 1 (“M” or “F”)
      • s[1] = action in period 2 if opponent played “M”
      • s[2] = action in period 2 if opponent played “F”
    """
    # 1) first‐stage outcome
    out1 = s_i[0] + s_j[0]
    
    # 2) second‐stage outcome, contingent moves
    a_i2 = s_i[1] if s_j[0]=="M" else s_i[2]
    a_j2 = s_j[1] if s_i[0]=="M" else s_j[2]
    out2 = a_i2 + a_j2
    
    # 3) look up payoffs
    pi_i1, pi_j1 = prisoner_payoffs[out1]
    pi_i2, pi_j2 = prisoner_payoffs[out2]
    
    # 4) return discounted‐sum for each player
    v_i = pi_i1 + delta * pi_i2
    v_j = pi_j1 + delta * pi_j2
    return v_i, v_j


def best_response_max(strategies, s_j, delta):
    best_si = max(
        strategies,
        key=lambda s_i: repeated_payoff(s_i, s_j, delta)[0]
    )
    best_val = repeated_payoff(best_si, s_j, delta)[0]
    return best_si, best_val

best_strats = [
    s_i
    for s_i in strategies
    if repeated_payoff(s_i, s_j = "FFF", delta = 1)[0] == best_val
]

### other random

from itertools import product

# 1) Payoff matrix
prisoner_payoffs = {
    "MM": (4, 4),
    "MF": (-1, 5),
    "FM": (5, -1),
    "FF": (1, 1)
}

# 2) Generate all 3-period strategies
strategies = [''.join(p) for p in product("MF", repeat=3)]

# 3) Repeated‐game payoff function
def repeated_payoff(s_i: str, s_j: str, delta: float) -> tuple[float, float]:
    # first‐stage actions
    out1 = s_i[0] + s_j[0]

    # second‐stage contingent actions
    a_i2 = s_i[1] if s_j[0] == "M" else s_i[2]
    a_j2 = s_j[1] if s_i[0] == "M" else s_j[2]
    out2 = a_i2 + a_j2

    # look up stage payoffs
    pi_i1, pi_j1 = prisoner_payoffs[out1]
    pi_i2, pi_j2 = prisoner_payoffs[out2]

    # discounted sum
    return pi_i1 + delta * pi_i2, pi_j1 + delta * pi_j2

# 4) Best‐response finder
def best_response_max(strategies, s_j: str, delta: float):
    best_si = max(strategies,
                  key=lambda s_i: repeated_payoff(s_i, s_j, delta)[0])
    best_val = repeated_payoff(best_si, s_j, delta)[0]
    return best_si, best_val

# 5) Compute best responses against "FFF" with δ=1
best_si, best_val = best_response_max(strategies, s_j="FFF", delta=1)

best_strats = [
    s_i
    for s_i in strategies
    if repeated_payoff(s_i, "FFF", 1)[0] == best_val
]

print("Against FFF, best single strategy value:", best_val)
print("All strategies attaining that value:", best_strats)
