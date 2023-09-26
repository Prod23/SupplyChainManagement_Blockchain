class Participant:
    def __init__(self, name, stake):
        self.name = name
        self.stake = stake
        self.locked_stake = 0
        self.delegate = None
        self.eligible_for_delegate = False  # Initialize as not eligible

    def lock_stake_for_delegate(self, amount):
        if self.stake >= amount:
            self.locked_stake = amount
            if self.locked_stake >= 50:
                self.eligible_for_delegate = True  # Become eligible for delegate

    def vote_for_delegate(self, delegate):
        delegate.votes += self.locked_stake
        self.stake -= self.locked_stake
        self.locked_stake = 0
        self.delegate = delegate
