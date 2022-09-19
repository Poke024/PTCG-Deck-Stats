class CardStats:
    def __init__(self, name):
        self.card = name
        # A array that tracks the number of copies in each deck.
        self._count = []
        self._avg_count = 0
        # A dictionary of arrays that tracks the win rate of decks by the number of card copies they have.
        self._count_WR = {
            "1": [],
            "2": [],
            "3": [],
            "4": []
            }
        # A dictionary that tracks if a number of card copies occurs in every deck.
        self._in_all = {
            "1": True,
            "2": True,
            "3": True,
            "4": True
        }

    def get_Avg_Count(self):
        return self._avg_count

    def get_Count_WR(self, count):
        if len(self._count_WR[count]) == 0:
            return "N/A"
        else:
            return (sum(self._count_WR[count])/len(self._count_WR[count]))

    def add_Count(self, new_count):
        self._count.append(new_count)
        self.avg_count = sum(self._count)/len(self._count)

    def add_Count_WR(self, count, rate):
        self._count_WR[count].append(float(rate))

    def if_Count_In_All(self, count):
        return self._in_all[count]

    def __str__(self):
        return (f"{self.card} Avg Count: {self.get_Avg_Count()},")
    