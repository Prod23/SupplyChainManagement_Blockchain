from Users import Participant
class Delegate:
    def __init__(self, name):
        self.name = name
        self.votes = 0

# Create participants
participant1 = Participant("Participant1", 200)
participant2 = Participant("Participant2", 150)
participant3 = Participant("Participant3", 100)

# Create delegates
delegate1 = Delegate("Delegate1")
delegate2 = Delegate("Delegate2")

# Lock stakes and vote for delegates
participant1.lock_stake_for_delegate(100)
participant1.vote_for_delegate(delegate1)

participant2.lock_stake_for_delegate(70)
participant2.vote_for_delegate(delegate1)

participant3.lock_stake_for_delegate(60)
participant3.vote_for_delegate(delegate2)

# Determine the chosen delegate
chosen_delegate = delegate1 if delegate1.votes > delegate2.votes else delegate2

print("Chosen Delegate:", chosen_delegate.name)
print("Total Votes for Chosen Delegate:", chosen_delegate.votes)
