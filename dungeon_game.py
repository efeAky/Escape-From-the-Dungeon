import random
from functools import reduce

# --- Character Class ---
class Character:
    def __init__(self, name, health, attack_power):
        # Initialize a character with a name, health, attack power, and default inventory
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.inventory = ['sword', 'poison', 'arrow']

    def take_damage(self, amount):
        # Reduce character's health by the damage amount
        self.health -= amount

    def attack(self, enemy):
        # Print an attack message (this could be expanded to actually damage enemy)
        print(f"\n⚔️ {self.name} attacks {enemy}")

    def add_item(self, item):
        # Add an item to inventory and notify player
        self.inventory.append(item)
        print(f"🎁 {self.name} picked up: {item}")

    def show_inventory(self):
        # Display inventory in uppercase for clarity
        formatted = list(map(str.upper, self.inventory))
        print(f"\n📦 {self.name}'s Inventory: {', '.join(formatted)}")

    def usable_items(self):
        # Return items that are not broken or already used
        usable_inventory = list(
            filter(lambda item: "broken" not in item.lower() and "used" not in item.lower(), self.inventory)
        )
        print(f"✅ Usable Items: {', '.join(usable_inventory)}")
        return usable_inventory


# --- Enemy Class ---
class Enemy:
    def __init__(self, name="Enemy"):
        # Initialize enemy with random health and attack power
        self.name = name
        self.health = random.randint(20, 40)
        self.attack_power = random.randint(10, 20)

    def take_damage(self, amount):
        # Reduce enemy's health and print remaining HP
        self.health -= amount
        print(f"💥 {self.name} takes {amount} damage | Remaining HP: {self.health}")

    def attack(self, character):
        # 20% chance to use a special attack (double damage)
        if random.randint(0, 100) < 20:
            damage = self.special_attack()
            print("🔥 Enemy uses a SPECIAL ATTACK!")
        else:
            damage = self.attack_power
        # Apply damage to character
        character.take_damage(damage)
        print(f"👹 {self.name} attacks {character.name} for {damage} damage! (Your HP: {character.health})")

    def special_attack(self):
        # Returns double attack power
        return self.attack_power * 2


# --- Enemy Generator ---
def generate_enemy(enemies):
    # Generates enemies one by one from the list and increases difficulty
    difficulty = 1
    while enemies:
        enemy_name = random.choice(enemies)
        enemy = Enemy(enemy_name)
        enemy.health += difficulty
        enemy.attack_power += difficulty
        print("\n==============================")
        print(f"⚔️ New Enemy Generated: {enemy.name}")
        print(f"❤️ Health: {enemy.health} | 🗡 Attack: {enemy.attack_power}")
        print("==============================")
        enemies.remove(enemy_name)
        yield enemy
        difficulty += 0.5
    else:
        # Generate a final boss after all enemies are defeated
        boss = Enemy("FINAL BOSS")
        boss.health *= 2
        boss.attack_power *= 2
        print("\n==============================")
        print("👑 FINAL BOSS APPEARS!")
        print(f"❤️ Health: {boss.health} | 🗡 Attack: {boss.attack_power}")
        print("==============================")
        yield boss


# --- Random Events ---
def random_event(hero):
    # Random events: either damage or healing
    events = [
        ("⚡ Surprise Attack!", -random.randint(10, 30)),  # Player takes damage
        ("🧪 Healing Potion!", +random.randint(20, 40)),  # Player heals
    ]
    event, effect = random.choice(events)

    print(f"\n[Random Event] {event}")

    if effect < 0:
        # Apply damage if effect is negative
        hero.take_damage(abs(effect))
        print(f"⚠️ {hero.name} took {abs(effect)} damage! | HP: {hero.health}")
    else:
        # Heal the player if effect is positive
        hero.health += effect
        print(f"✨ {hero.name} healed {effect} HP! | HP: {hero.health}")


# --- Battle Function ---
def battle(hero, enemy):
    # Conduct a fight until either hero or enemy is defeated
    print(f"\n🔥 {hero.name} enters battle with {enemy.name} (HP: {enemy.health}, Attack: {enemy.attack_power})")

    while hero.health > 0 and enemy.health > 0:
        # 20% chance to use an inventory item for extra damage
        if random.randint(0, 100) <= 20 and hero.inventory:
            damage = reduce(lambda x, y: x + y, [hero.attack_power, 25])
            item = random.choice(hero.inventory)
            print(f"\n🗡 {hero.name} used {item} and dealt {damage} damage!")
            enemy.take_damage(damage)
        else:
            # Regular attack
            print(f"\n⚔️ {hero.name} attacks for {hero.attack_power} damage")
            enemy.take_damage(hero.attack_power)

        # Break loop if enemy defeated
        if enemy.health <= 0:
            break

        # Enemy counterattacks
        enemy.attack(hero)

    if hero.health <= 0:
        # Hero defeated
        print(f"\n💀 {hero.name} was defeated...")
    else:
        # Enemy defeated, trigger random event
        print("\n✅ Enemy defeated!")
        random_event(hero)


# --- Game Loop ---
enemies = ['Goblin', 'Vampire']  # List of enemies for the hero to face
print("\n==============================")
print("🏰 [BATTLE BEGINS]")
print("==============================")

hero = Character("You", 100, 25)  # Create hero
enemy_generator = generate_enemy(enemies)  # Create generator for enemies

for enemy in enemy_generator:
    # Loop through generated enemies and battle each
    battle(hero, enemy)
    if hero.health <= 0:
        print("\n💀 YOU LOSE! Better luck next time...")
        break
else:
    # Runs if hero survives all enemies
    print("\n🏆 YOU WIN! Congratulations, all enemies defeated!")
