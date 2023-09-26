from Users import Participant
class Delegate:
    def __init__(self, name):
        self.name = name
        self.votes = 0

participant1 = Participant("Participant1", 200)
participant2 = Participant("Participant2", 150)
participant3 = Participant("Participant3", 100)

# Lock stakes for delegate eligibility
participant1.lock_stake_for_delegate(100)
participant2.lock_stake_for_delegate(70)
participant3.lock_stake_for_delegate(60)

# Collect eligible participants for delegate election
eligible_delegates = [participant for participant in [participant1, participant2, participant3] if participant.eligible_for_delegate]

# Create delegates for eligible participants
delegates = [Participant(f"Delegate-{i}", 0) for i, participant in enumerate(eligible_delegates)]

# Each eligible participant votes for themselves
for participant in eligible_delegates:
    participant.vote_for_delegate(participant.delegate)

# Calculate total votes for each delegate
for participant in eligible_delegates:
    if participant.delegate:
        participant.delegate.votes += participant.votes

# Determine the chosen delegate with the highest votes
chosen_delegate = max(delegates, key=lambda delegate: delegate.votes)

print("Chosen Delegate:", chosen_delegate.name)
print("Total Votes for Chosen Delegate:", chosen_delegate.votes)
