import random

ROWS = ["front", "mid", "back"]

# -----------------------------
# CARD
# -----------------------------

class Card:
    def __init__(self, name, power, row, ability=None):
        self.name = name
        self.base_power = power
        self.power = power
        self.row = row
        self.ability = ability

    def reset(self):
        self.power = self.base_power

    def __str__(self):
        return f"{self.name} ({self.power}) [{self.row}]"


# -----------------------------
# PLAYER
# -----------------------------

class Player:
    def __init__(self, name, deck, ai=False):
        self.name = name
        self.deck = deck
        self.hand = []
        self.rows = {row: [] for row in ROWS}
        self.passed = False
        self.rounds_won = 0
        self.ai = ai

    def draw(self, n=1):
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop())

    def total_power(self):
        return sum(card.power for row in self.rows.values() for card in row)

    def reset_board(self):
        for row in self.rows.values():
            for card in row:
                card.reset()
        self.rows = {row: [] for row in ROWS}
        self.passed = False


# -----------------------------
# ABILITIES
# -----------------------------

def apply_ability(card, player, opponent):
    if card.ability == "boost_row":
        for ally in player.rows[card.row]:
            ally.power += 1

    elif card.ability == "ping_enemy":
        enemies = [u for r in opponent.rows.values() for u in r]
        if enemies:
            target = random.choice(enemies)
            target.power -= 2
            if target.power <= 0:
                for r in opponent.rows.values():
                    if target in r:
                        r.remove(target)


# -----------------------------
# TURN LOGIC
# -----------------------------

def play_turn(player, opponent):
    if player.passed:
        return

    if player.ai:
        # AI logic (imperfect on purpose)
        if random.random() < 0.25:
            player.passed = True
            print(f"{player.name} passes.")
            return

        card = random.choice(player.hand)
        player.hand.remove(card)
    else:
        print(f"\n{player.name}'s hand:")
        for i, card in enumerate(player.hand):
            print(f"{i}: {card}")

        choice = input("Play card # or 'p' to pass: ").lower()
        if choice == "p":
            player.passed = True
            return

        try:
            card = player.hand.pop(int(choice))
        except:
            print("Invalid choice.")
            return

    player.rows[card.row].append(card)
    apply_ability(card, player, opponent)
    print(f"{player.name} plays {card.name}.")


# -----------------------------
# ROUND
# -----------------------------

def play_round(p1, p2, round_num):
    print(f"\n===== ROUND {round_num} =====")
    p1.draw(1)
    p2.draw(1)

    while not (p1.passed and p2.passed):
        play_turn(p1, p2)
        play_turn(p2, p1)

        print(f"\nScore → {p1.name}: {p1.total_power()} | {p2.name}: {p2.total_power()}")

    if p1.total_power() > p2.total_power():
        p1.rounds_won += 1
        print(f"{p1.name} wins the round!")
    elif p2.total_power() > p1.total_power():
        p2.rounds_won += 1
        print(f"{p2.name} wins the round!")
    else:
        print("Round tied.")

    p1.reset_board()
    p2.reset_board()


# -----------------------------
# DECK BUILDING
# -----------------------------

def create_space_deck():
    deck = []

    for _ in range(6):
        deck.append(Card("Star Marine", 4, "front"))
        deck.append(Card("Void Sniper", 3, "back", "ping_enemy"))
        deck.append(Card("Fleet Officer", 5, "mid", "boost_row"))

    deck += [
        Card("Battle Mech", 8, "front"),
        Card("Nebula Assassin", 6, "mid", "ping_enemy"),
        Card("Orbital Cannon", 7, "back"),
        Card("Quantum General", 9, "mid", "boost_row"),
    ]

    random.shuffle(deck)
    return deck


# -----------------------------
# MULLIGAN
# -----------------------------

def mulligan(player):
    if player.ai:
        return

    print(f"\n{player.name} Mulligan (up to 2 cards)")
    for _ in range(2):
        print("Hand:")
        for i, card in enumerate(player.hand):
            print(f"{i}: {card}")

        choice = input("Replace card # or press Enter to keep: ")
        if choice == "":
            break
        try:
            idx = int(choice)
            player.deck.insert(0, player.hand.pop(idx))
            player.draw(1)
        except:
            break


# -----------------------------
# MAIN
# -----------------------------

def main():
    p1 = Player("Commander Alpha", create_space_deck())
    p2 = Player("Commander Omega", create_space_deck(), ai=True)

    p1.draw(10)
    p2.draw(10)

    mulligan(p1)
    mulligan(p2)

    round_num = 1
    while p1.rounds_won < 2 and p2.rounds_won < 2:
        play_round(p1, p2, round_num)
        round_num += 1

    winner = p1 if p1.rounds_won > p2.rounds_won else p2
    print(f"\n🏆 {winner.name} wins the match! 🏆")


if __name__ == "__main__":
    main()
