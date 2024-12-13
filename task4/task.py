import math

def entropy(prob_dist):
    return -sum(p * math.log2(p) for p in prob_dist if p > 0)

def main():
    values = range(1, 7)

    joint_counts = {}
    total_outcomes = 36  # 6*6

    for x in values:
        for y in values:
            A = x + y
            B = x * y
            joint_counts[(A, B)] = joint_counts.get((A, B), 0) + 1

    joint_probs = {k: v / total_outcomes for k, v in joint_counts.items()}

    pA = {}
    pB = {}
    for (A, B), p in joint_probs.items():
        pA[A] = pA.get(A, 0) + p
        pB[B] = pB.get(B, 0) + p

    H_AB = entropy(joint_probs.values())
    H_A = entropy(pA.values())
    H_B = entropy(pB.values())

    H_B_given_A = H_AB - H_A

    I_AB = H_A + H_B - H_AB

    print(f"H(AB) = {H_AB:.2f}")
    print(f"H(A)  = {H_A:.2f}")
    print(f"H(B)  = {H_B:.2f}")
    print(f"H_a(B) = {H_B_given_A:.2f}")
    print(f"I(A,B) = {I_AB:.2f}")

if __name__ == "__main__":
    main()
