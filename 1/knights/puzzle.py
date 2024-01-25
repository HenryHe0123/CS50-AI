from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# debug: Don't forget common sense!
Common = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave))
)

# Puzzle 0
# A says "I am both a knight and a knave."
A0 = And(AKnight, AKnave)
knowledge0 = And(
    Common,
    Implication(AKnight, A0),
    Implication(AKnave, Not(A0))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A1 = And(AKnave, BKnave)
knowledge1 = And(
    Common,
    Implication(AKnight, A1),
    Implication(AKnave, Not(A1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A2 = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
)
B2 = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight)
)
knowledge2 = And(
    Common,
    Implication(AKnight, A2),
    Implication(AKnave, Not(A2)),
    Implication(BKnight, B2),
    Implication(BKnave, Not(B2))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# trivia: either...or... maybe both
ASaysKnight = Symbol("A says 'I am a knight.'")
ASaysKnave = Symbol("A says 'I am a knave.'")
B31 = ASaysKnave
B32 = CKnave
# B3 = And(B31, B32)
# debug: We should not simply combine B31 and B32 together,
# as every sentence spoken by a knight/knave is true/false.
C3 = AKnight
knowledge3 = And(
    Common,
    Or(ASaysKnight, ASaysKnave),
    # AKnight
    Implication(And(AKnight, ASaysKnight), AKnight),
    Implication(And(AKnight, ASaysKnave), AKnave),
    # AKnave
    Implication(And(AKnave, ASaysKnight), Not(AKnight)),
    Implication(And(AKnave, ASaysKnave), Not(AKnave)),
    #
    Implication(BKnight, B31),
    Implication(BKnight, B32),
    Implication(BKnave, Not(B31)),
    Implication(BKnave, Not(B32)),
    Implication(CKnight, C3),
    Implication(CKnave, Not(C3))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
