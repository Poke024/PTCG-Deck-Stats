class CardStats:
    def __init__(self, name:str, set:str):
        self.name = name
        self.set = set
        # A array that tracks the number of copies in each deck.
        self._counts = []
        self._avg_count = 0
        # A dictionary of arrays that tracks the win rate of decks by the number of card copies they have.
        # Format: { '#': [#, #, #, ...]}
        self._count_WR = {}
        # Tracks the number of copies in a card that appears in all decks analyzed.
        # Changes to first count retrieved. Changes to 5 if any other count is noted.
        self._count_in_all = 0

    # Returns the average number of card copies
    def get_Avg_Count(self):
        return self._avg_count

    # Calculates and returns the average winrate for decks with a given number of card copies.
    def get_Count_WR(self, count:int):
        if len(self._count_WR[count]) == 0:
            return "N/A"
        else:
            return (sum(self._count_WR[count])/len(self._count_WR[count]))

    # Adds a count of copies of a card from a deck
    def add_Count(self, new_count:int):
        self._counts.append(new_count)
        self._avg_count = sum(self._counts)/len(self._counts)
        if self._count_in_all == 0:
            self._count_in_all = new_count
        elif self._count_in_all != None and new_count != self._count_in_all:
            self._count_in_all = None

    # Adds a winrate percentage from a deck to a given number of card copies
    def add_Count_WR(self, count:int, rate:float):
        self._count_WR[count].append(float(rate))

    # Returns the number of copies that appears in every deck
    # Returns 1 - 4 dependent on copies
    # Returns None if any deck had a different number of copies
    def get_Count_In_All(self):
        return self._count_in_all

    def __str__(self):
        return (f"{self.card} ({self.set}) Avg Count: {self.get_Avg_Count()}")
