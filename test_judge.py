from itertools import permutations

from judge import TrickType, validate_trick_and_get_strength, get_strength

# ChatGPT4o is responsible for any mistakes :)
test_cases = [
    # Single
    (["AD"], TrickType.SINGLE, "AD"),
    (["4C"], TrickType.SINGLE, "4C"),
    (["TH"], TrickType.SINGLE, "TH"),
    (["9S"], TrickType.SINGLE, "9S"),
    (["2D"], TrickType.SINGLE, "2D"),
    (["3H"], TrickType.SINGLE, "3H"),
    (["KC"], TrickType.SINGLE, "KC"),
    (["7S"], TrickType.SINGLE, "7S"),
    (["6C"], TrickType.SINGLE, "6C"),
    (["5H"], TrickType.SINGLE, "5H"),
    (["JS"], TrickType.SINGLE, "JS"),
    (["QS"], TrickType.SINGLE, "QS"),
    (["8D"], TrickType.SINGLE, "8D"),
    (["JD"], TrickType.SINGLE, "JD"),
    (["5S"], TrickType.SINGLE, "5S"),
    (["4H"], TrickType.SINGLE, "4H"),
    (["3S"], TrickType.SINGLE, "3S"),
    (["AS"], TrickType.SINGLE, "AS"),
    (["KH"], TrickType.SINGLE, "KH"),
    (["2S"], TrickType.SINGLE, "2S"),

    # Pair
    (["9S", "9D"], TrickType.PAIR, "9S"),
    (["AD", "AC"], TrickType.PAIR, "AC"),
    (["5H", "5C"], TrickType.PAIR, "5H"),
    (["7S", "7C"], TrickType.PAIR, "7S"),
    (["KH", "KC"], TrickType.PAIR, "KH"),
    (["6H", "6S"], TrickType.PAIR, "6S"),
    (["TS", "TC"], TrickType.PAIR, "TS"),
    (["8H", "8D"], TrickType.PAIR, "8H"),
    (["QD", "QC"], TrickType.PAIR, "QC"),
    (["3S", "3C"], TrickType.PAIR, "3S"),
    (["JS", "JD"], TrickType.PAIR, "JS"),
    (["4H", "4D"], TrickType.PAIR, "4H"),
    (["2C", "2H"], TrickType.PAIR, "2H"),
    (["9H", "9C"], TrickType.PAIR, "9H"),
    (["KD", "KS"], TrickType.PAIR, "KS"),
    (["5S", "5D"], TrickType.PAIR, "5S"),
    (["3D", "3H"], TrickType.PAIR, "3H"),
    (["6C", "6D"], TrickType.PAIR, "6C"),
    (["JC", "JH"], TrickType.PAIR, "JH"),
    (["8C", "8S"], TrickType.PAIR, "8S"),

    # Triplet
    (["3S", "3D", "3C"], TrickType.TRIPLET, "3S"),
    (["QS", "QD", "QC"], TrickType.TRIPLET, "QS"),
    (["6H", "6S", "6C"], TrickType.TRIPLET, "6S"),
    (["9C", "9H", "9S"], TrickType.TRIPLET, "9S"),
    (["AS", "AC", "AD"], TrickType.TRIPLET, "AS"),
    (["TH", "TS", "TC"], TrickType.TRIPLET, "TS"),
    (["8D", "8C", "8S"], TrickType.TRIPLET, "8S"),
    (["4S", "4C", "4H"], TrickType.TRIPLET, "4S"),
    (["5H", "5D", "5S"], TrickType.TRIPLET, "5S"),
    (["KD", "KH", "KS"], TrickType.TRIPLET, "KS"),
    (["2S", "2C", "2H"], TrickType.TRIPLET, "2S"),
    (["7D", "7C", "7H"], TrickType.TRIPLET, "7H"),
    (["JC", "JD", "JS"], TrickType.TRIPLET, "JS"),
    (["AD", "AH", "AS"], TrickType.TRIPLET, "AS"),
    (["QH", "QS", "QC"], TrickType.TRIPLET, "QS"),
    (["TD", "TH", "TC"], TrickType.TRIPLET, "TH"),
    (["KH", "KS", "KC"], TrickType.TRIPLET, "KS"),
    (["4D", "4H", "4C"], TrickType.TRIPLET, "4H"),
    (["8H", "8S", "8C"], TrickType.TRIPLET, "8S"),
    (["JD", "JH", "JC"], TrickType.TRIPLET, "JH"),

    # Straight
    (["3S", "4D", "5C", "6C", "7C"], TrickType.STRAIGHT, "7C"),
    (["7H", "8D", "9C", "TH", "JH"], TrickType.STRAIGHT, "JH"),
    (["4S", "5D", "6H", "7D", "8C"], TrickType.STRAIGHT, "8C"),
    (["5H", "6S", "7C", "8H", "9D"], TrickType.STRAIGHT, "9D"),
    (["TS", "JD", "QC", "KH", "AD"], TrickType.STRAIGHT, "AD"),
    (["3D", "4C", "5H", "6S", "7H"], TrickType.STRAIGHT, "7H"),
    (["9S", "TC", "JD", "QH", "KC"], TrickType.STRAIGHT, "KC"),
    (["6H", "7D", "8C", "9H", "TS"], TrickType.STRAIGHT, "TS"),
    (["JC", "QH", "KH", "AD", "2S"], TrickType.STRAIGHT, "2S"),
    (["5S", "6D", "7C", "8H", "9C"], TrickType.STRAIGHT, "9C"),
    (["3H", "4S", "5C", "6H", "7C"], TrickType.STRAIGHT, "7C"),
    (["JH", "QD", "KC", "AD", "2D"], TrickType.STRAIGHT, "2D"),
    (["8C", "9D", "TH", "JC", "QD"], TrickType.STRAIGHT, "QD"),
    (["3H", "4S", "5D", "6C", "7H"], TrickType.STRAIGHT, "7H"),
    (["4H", "5D", "6C", "7S", "8D"], TrickType.STRAIGHT, "8D"),
    (["6D", "7H", "8S", "9C", "TD"], TrickType.STRAIGHT, "TD"),
    (["9H", "TC", "JD", "QH", "KC"], TrickType.STRAIGHT, "KC"),
    (["7C", "8H", "9S", "TH", "JC"], TrickType.STRAIGHT, "JC"),
    (["5C", "6D", "7H", "8C", "9S"], TrickType.STRAIGHT, "9S"),
    (["TD", "JD", "QD", "KS", "AD"], TrickType.STRAIGHT, "AD"),

    # Flush
    (["8C", "AC", "3C", "9C", "QC"], TrickType.FLUSH, None),
    (["2H", "9H", "KH", "7H", "5H"], TrickType.FLUSH, None),
    (["4D", "5D", "8D", "QD", "AD"], TrickType.FLUSH, None),
    (["5S", "7S", "9S", "JS", "KS"], TrickType.FLUSH, None),
    (["6C", "7C", "8C", "KC", "2C"], TrickType.FLUSH, None),
    (["TS", "4S", "8S", "JS", "KS"], TrickType.FLUSH, None),
    (["6D", "8D", "9D", "JD", "KD"], TrickType.FLUSH, None),
    (["3H", "4H", "6H", "QH", "AH"], TrickType.FLUSH, None),
    (["2C", "4C", "9C", "JC", "KC"], TrickType.FLUSH, None),
    (["3S", "5S", "6S", "7S", "QS"], TrickType.FLUSH, None),
    (["7D", "8D", "JD", "KD", "AD"], TrickType.FLUSH, None),
    (["5H", "6H", "8H", "KH", "3H"], TrickType.FLUSH, None),
    (["4C", "5C", "7C", "JC", "QC"], TrickType.FLUSH, None),
    (["8S", "TS", "JS", "QS", "KS"], TrickType.FLUSH, None),
    (["3D", "5D", "6D", "8D", "TD"], TrickType.FLUSH, None),
    (["5H", "7H", "9H", "QH", "AH"], TrickType.FLUSH, None),
    (["4S", "6S", "9S", "JS", "AS"], TrickType.FLUSH, None),
    (["7C", "9C", "TC", "KC", "AC"], TrickType.FLUSH, None),
    (["2S", "4S", "5S", "JS", "KS"], TrickType.FLUSH, None),
    (["2D", "3D", "7D", "QD", "AD"], TrickType.FLUSH, None),

    # Full House
    (["8S", "8D", "8C", "6C", "6S"], TrickType.FULL_HOUSE, "8S"),
    (["TS", "TD", "TC", "4C", "4D"], TrickType.FULL_HOUSE, "TS"),
    (["6H", "6S", "6D", "3H", "3C"], TrickType.FULL_HOUSE, "6S"),
    (["QD", "QC", "QS", "2C", "2S"], TrickType.FULL_HOUSE, "QS"),
    (["5C", "5D", "5H", "7S", "7H"], TrickType.FULL_HOUSE, "5H"),
    (["4H", "4D", "4C", "KH", "KS"], TrickType.FULL_HOUSE, "4H"),
    (["JC", "JD", "JS", "3C", "3D"], TrickType.FULL_HOUSE, "JS"),
    (["9S", "9C", "9D", "5H", "5C"], TrickType.FULL_HOUSE, "9S"),
    (["KH", "KC", "KS", "6H", "6D"], TrickType.FULL_HOUSE, "KS"),
    (["3D", "3S", "3H", "8H", "8D"], TrickType.FULL_HOUSE, "3S"),
    (["AS", "AH", "AC", "2H", "2C"], TrickType.FULL_HOUSE, "AS"),
    (["7H", "7D", "7S", "QH", "QC"], TrickType.FULL_HOUSE, "7S"),
    (["2S", "2H", "2C", "JD", "JC"], TrickType.FULL_HOUSE, "2S"),
    (["8D", "8H", "8C", "9S", "9D"], TrickType.FULL_HOUSE, "8H"),
    (["TD", "TC", "TH", "KH", "KC"], TrickType.FULL_HOUSE, "TH"),
    (["QS", "QH", "QC", "8H", "8C"], TrickType.FULL_HOUSE, "QS"),
    (["5H", "5S", "5C", "JD", "JC"], TrickType.FULL_HOUSE, "5S"),
    (["6D", "6H", "6C", "4S", "4D"], TrickType.FULL_HOUSE, "6H"),
    (["JD", "JS", "JC", "TD", "TS"], TrickType.FULL_HOUSE, "JS"),
    (["4C", "4S", "4H", "5C", "5D"], TrickType.FULL_HOUSE, "4S"),

    # Four-of-a-kind
    (["4S", "4D", "4H", "4C", "AD"], TrickType.FOUR_OF_A_KIND, "4S"),
    (["KH", "KS", "KD", "KC", "3D"], TrickType.FOUR_OF_A_KIND, "KS"),
    (["9H", "9S", "9D", "9C", "6H"], TrickType.FOUR_OF_A_KIND, "9S"),
    (["2S", "2C", "2D", "2H", "7D"], TrickType.FOUR_OF_A_KIND, "2S"),
    (["5D", "5C", "5H", "5S", "KH"], TrickType.FOUR_OF_A_KIND, "5S"),
    (["7C", "7D", "7H", "7S", "8H"], TrickType.FOUR_OF_A_KIND, "7S"),
    (["AS", "AC", "AD", "AH", "3C"], TrickType.FOUR_OF_A_KIND, "AS"),
    (["JD", "JS", "JC", "JH", "6C"], TrickType.FOUR_OF_A_KIND, "JS"),
    (["TC", "TH", "TD", "TS", "2H"], TrickType.FOUR_OF_A_KIND, "TS"),
    (["8S", "8C", "8H", "8D", "QD"], TrickType.FOUR_OF_A_KIND, "8S"),
    (["3C", "3D", "3H", "3S", "AC"], TrickType.FOUR_OF_A_KIND, "3S"),
    (["QH", "QC", "QS", "QD", "9C"], TrickType.FOUR_OF_A_KIND, "QS"),
    (["6S", "6D", "6C", "6H", "4D"], TrickType.FOUR_OF_A_KIND, "6S"),
    (["KC", "KH", "KD", "KS", "9H"], TrickType.FOUR_OF_A_KIND, "KS"),
    (["JS", "JD", "JC", "JH", "3D"], TrickType.FOUR_OF_A_KIND, "JS"),
    (["8C", "8S", "8H", "8D", "7S"], TrickType.FOUR_OF_A_KIND, "8S"),
    (["3H", "3S", "3D", "3C", "5S"], TrickType.FOUR_OF_A_KIND, "3S"),
    (["9C", "9D", "9H", "9S", "7H"], TrickType.FOUR_OF_A_KIND, "9S"),
    (["QC", "QD", "QH", "QS", "2S"], TrickType.FOUR_OF_A_KIND, "QS"),
    (["5S", "5H", "5C", "5D", "JC"], TrickType.FOUR_OF_A_KIND, "5S"),

    # Straight Flush
    (["4S", "5S", "6S", "7S", "8S"], TrickType.STRAIGHT_FLUSH, "8S"),
    (["9D", "TD", "JD", "QD", "KD"], TrickType.STRAIGHT_FLUSH, "KD"),
    (["6H", "7H", "8H", "9H", "TH"], TrickType.STRAIGHT_FLUSH, "TH"),
    (["3C", "4C", "5C", "6C", "7C"], TrickType.STRAIGHT_FLUSH, "7C"),
    (["7C", "8C", "9C", "TC", "JC"], TrickType.STRAIGHT_FLUSH, "JC"),
    (["5H", "6H", "7H", "8H", "9H"], TrickType.STRAIGHT_FLUSH, "9H"),
    (["3D", "4D", "5D", "6D", "7D"], TrickType.STRAIGHT_FLUSH, "7D"),
    (["8S", "9S", "TS", "JS", "QS"], TrickType.STRAIGHT_FLUSH, "QS"),
    (["6C", "7C", "8C", "9C", "TC"], TrickType.STRAIGHT_FLUSH, "TC"),
    (["9H", "TH", "JH", "QH", "KH"], TrickType.STRAIGHT_FLUSH, "KH"),
    (["4H", "5H", "6H", "7H", "8H"], TrickType.STRAIGHT_FLUSH, "8H"),
    (["4S", "5S", "6S", "7S", "8S"], TrickType.STRAIGHT_FLUSH, "8S"),
    (["JD", "QD", "KD", "AD", "2D"], TrickType.STRAIGHT_FLUSH, "2D"),
    (["TH", "JH", "QH", "KH", "AH"], TrickType.STRAIGHT_FLUSH, "AH"),
    (["5D", "6D", "7D", "8D", "9D"], TrickType.STRAIGHT_FLUSH, "9D"),
    (["TC", "JC", "QC", "KC", "AC"], TrickType.STRAIGHT_FLUSH, "AC"),
    (["3H", "4H", "5H", "6H", "7H"], TrickType.STRAIGHT_FLUSH, "7H"),
    (["7S", "8S", "9S", "TS", "JS"], TrickType.STRAIGHT_FLUSH, "JS"),
    (["3H", "4H", "5H", "6H", "7H"], TrickType.STRAIGHT_FLUSH, "7H"),
    (["JC", "QC", "KC", "AC", "2C"], TrickType.STRAIGHT_FLUSH, "2C"),

    # Invalid cases
    (["AD", "4C", "TH"], TrickType.PASS, None),  # Invalid combination of single cards
    (["9S", "9D", "4C"], TrickType.PASS, None),  # Pair with an extra card
    (["3S", "3D", "3C", "KH"], TrickType.PASS, None),  # Triplet with an extra card
    (["5C", "6H", "7D"], TrickType.PASS, None),  # Incomplete straight
    (["8H", "9H", "JC"], TrickType.PASS, None),  # Mixed suits, incomplete flush
    (["4D", "4H", "4S", "4C", "5H", "6H"], TrickType.PASS, None),  # Extra card in four-of-a-kind
    (["2S", "2H", "3S", "4S"], TrickType.PASS, None),  # Mixed combination
    (["6D", "6H", "7S", "8D"], TrickType.PASS, None),  # Invalid mixed sequence
    (["5S", "6C", "7D", "8H", "9S", "TS"], TrickType.PASS, None),  # Too many cards for a valid trick
    (["AS", "AC", "AD", "KD"], TrickType.PASS, None),  # Four cards without a full set
    (["7C", "8C", "9D"], TrickType.PASS, None),  # Incomplete flush
    (["3H", "4H", "5D", "6S"], TrickType.PASS, None),  # Invalid straight
    (["JS", "JD", "2C"], TrickType.PASS, None),  # Pair with an unrelated card
    (["KH", "KS", "KC", "TH"], TrickType.PASS, None),  # Triplet with an unrelated card
    (["9H", "9S", "9D", "9C", "9S"], TrickType.PASS, None),  # Four-of-a-kind with an duplicate card
    (["2D", "3D", "4D", "6D"], TrickType.PASS, None),  # Incomplete straight flush
    (["5H", "5D", "AS"], TrickType.PASS, None),  # Triplet missing a full house pair
    (["QC", "KC", "AC", "2C", "3H"], TrickType.PASS, None),  # Invalid straight flush
    (["4S", "5S", "6H"], TrickType.PASS, None),  # Invalid combination, mixed suit straight
    (["JD", "QD", "KD", "AD"], TrickType.PASS, None),  # Missing one card for a straight
    (["7H", "8H", "9C"], TrickType.PASS, None),  # Invalid combination, mixed suits
    (["5C", "5H", "6C", "7C", "8C"], TrickType.PASS, None),  # Mixed flush
    (["TS", "JS", "QD"], TrickType.PASS, None),  # Incomplete straight
    (["6D", "6S", "7H"], TrickType.PASS, None),  # Invalid combination of pairs and singles
    (["KH", "KC", "KD", "KS", "3D", "3C"], TrickType.PASS, None),  # Too many cards for any trick
    (["8S", "9S", "TD"], TrickType.PASS, None),  # Invalid flush
    (["7S", "8H", "9H", "TH"], TrickType.PASS, None),  # Invalid mixed flush
    (["5D", "6D", "8D"], TrickType.PASS, None),  # Invalid flush
    (["QS", "QH", "4S"], TrickType.PASS, None),  # Pair with extra single
    (["3D", "3C", "4D"], TrickType.PASS, None),  # Mixed invalid combination
    (["AS", "KS", "QS"], TrickType.PASS, None),  # Incomplete straight
    (["2H", "3H", "4H", "5H", "7D"], TrickType.PASS, None),  # Invalid combination with flush
    (["8C", "8D", "8H", "2C"], TrickType.PASS, None),  # Triplet with unrelated card
    (["3S", "3C", "6C", "6H"], TrickType.PASS, None),  # Two pairs, no full house
    (["7S", "7C", "8D"], TrickType.PASS, None),  # Invalid mixed cards
    (["KC", "KH", "4C", "4H"], TrickType.PASS, None),  # Two pairs, not a full house
    (["9H", "9C", "6S"], TrickType.PASS, None),  # Pair with extra unrelated card
    (["4H", "5H", "6S"], TrickType.PASS, None),  # Invalid straight combination
    (["3C", "4C", "5D", "6C"], TrickType.PASS, None),  # Incomplete straight with mixed suits
    (["JD", "JD"], TrickType.PASS, None),  # Duplicate cards
    (["5S", "6S", "7S"], TrickType.PASS, None),  # Incomplete flush
    (["AD", "2D", "3D"], TrickType.PASS, None),  # Invalid mixed sequence
    (["KS", "KD", "KH", "4D"], TrickType.PASS, None),  # Triplet with unrelated card
    (["2C", "2H", "3S"], TrickType.PASS, None),  # Pair with extra unrelated card
    (["7H", "8H", "9H", "9S"], TrickType.PASS, None),  # Invalid flush
    (["4C", "5C", "6H"], TrickType.PASS, None),  # Mixed suits in straight
    (["TC", "TD", "4H"], TrickType.PASS, None),  # Pair with extra unrelated card
    (["JS", "QS", "KS"], TrickType.PASS, None),  # Incomplete straight flush
    (["6D", "6H", "9D"], TrickType.PASS, None),  # Pair with unrelated card
    (["AS", "AH", "AD", "5D", "6D"], TrickType.PASS, None),  # Missing full house pair
    (["4C", "5C"], TrickType.PASS, None),  # Two different ranks, invalid pair
    (["7H", "8H"], TrickType.PASS, None),  # Two different ranks, invalid pair
    (["2D", "3D"], TrickType.PASS, None),  # Two different ranks, invalid pair
    (["KH", "QS"], TrickType.PASS, None),  # Different ranks and suits, invalid pair
    (["JD", "9D"], TrickType.PASS, None),  # Different ranks, invalid pair
    (["8S", "6S"], TrickType.PASS, None),  # Different ranks, invalid pair
    (["TS", "JD"], TrickType.PASS, None),  # Different ranks, invalid pair
    (["AC", "2C"], TrickType.PASS, None),  # Different ranks, invalid pair
    (["6H", "7H"], TrickType.PASS, None),  # Two different ranks, invalid pair
    (["QC", "KC"], TrickType.PASS, None),  # Different ranks, invalid pair
]


def main():
    for cards, expected_trick_type, determinant in test_cases:
        print(cards)
        for card_perm in permutations(cards):
            is_valid, strength, trick_type, reason = validate_trick_and_get_strength(None, list(card_perm))
            assert trick_type == expected_trick_type
            assert determinant is None or get_strength(determinant) == strength


if __name__ == '__main__':
    main()
