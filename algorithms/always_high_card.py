from classes import *


"""
The algorithm provided on the Big Two contest wiki page.
"""


class Algorithm:

    # Calculates the relative strength of a single card as a number to be used with Python's key comparison mechanism
    def getStrength(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        return ranks.index(card[0]) * 4 + suits.index(card[1])

    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        # Sort hand from lowest to highest card
        sortedHand = sorted(state.myHand, key = lambda x : self.getStrength(x))

        # If I am the first to play, play my weakest one card trick
        if state.toBeat is None:
            action.append(sortedHand[0])

        # If the trick size is 1, play my weakest trick that still beats this one, or pass nothing otherwise
        elif len(state.toBeat.cards) == 1:
            cardToBeat = state.toBeat.cards[0]
            for card in sortedHand:
                if self.getStrength(card) > self.getStrength(cardToBeat):
                    action.append(card)
                    break

        # If the trick size is 2, 3, or 5, I will pass

        return action, myData