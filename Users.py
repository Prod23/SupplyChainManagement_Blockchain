class Participant:
    def __init__(self, name, stake):
        self.name = name
        self.stake = stake
        self.locked_stake = 0
        self.delegate = None

    def lock_stake_for_delegate(self, amount):
        if self.stake >= amount:
            self.locked_stake = amount
            self.stake -= amount
        else:
            print("Insufficient stake to lock.")

    def vote_for_delegate(self, delegate):
        if self.locked_stake > 0:
            delegate.votes += self.locked_stake
            self.locked_stake = 0
            self.delegate = delegate
        else:
            print("You need to lock up stake to vote for a delegate.")
