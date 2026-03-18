"""
Draegtile Text-Based RPG Game Engine
======================================
A fully playable text-based open-world RPG with exploration, combat,
inventory, quests and NPC dialogue — all running entirely in the terminal.

Inspired by:
  - guides/Guide contents.txt (RPG game design outline)
  - guides/Basic Example using Chat gpt for fixing errors during implementation for beginners.txt
"""

import random
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data definitions
# ---------------------------------------------------------------------------

WORLD: Dict[str, Dict[str, Any]] = {
    "village": {
        "description": (
            "You are in a small, peaceful village. Smoke rises from chimneys, "
            "and you can hear the distant sound of a blacksmith at work."
        ),
        "exits": {"north": "forest", "east": "market", "south": "plains"},
        "enemies": [],
        "items": ["healing_potion"],
        "npc": "Elder Mira",
    },
    "market": {
        "description": (
            "The bustling market is full of merchants selling wares. "
            "Strange artefacts gleam on the nearest stall."
        ),
        "exits": {"west": "village"},
        "enemies": [],
        "items": ["iron_sword", "leather_armour"],
        "npc": "Merchant Tobias",
    },
    "forest": {
        "description": (
            "Ancient trees loom around you. Shadows move between the trunks, "
            "and an eerie silence fills the air."
        ),
        "exits": {"south": "village", "north": "cave"},
        "enemies": ["wolf", "goblin"],
        "items": ["stick"],
        "npc": None,
    },
    "plains": {
        "description": (
            "Vast open plains stretch to the horizon. A cool breeze carries "
            "the scent of wild flowers."
        ),
        "exits": {"north": "village", "east": "ruins"},
        "enemies": ["bandit"],
        "items": [],
        "npc": None,
    },
    "cave": {
        "description": (
            "A damp, torch-lit cave. Stalactites drip overhead and your "
            "footsteps echo into the darkness."
        ),
        "exits": {"south": "forest"},
        "enemies": ["cave_troll", "skeleton"],
        "items": ["ancient_rune", "gold_coin"],
        "npc": None,
    },
    "ruins": {
        "description": (
            "Crumbling stone walls are all that remain of an ancient city. "
            "Power seems to pulse from the centre of the ruins."
        ),
        "exits": {"west": "plains"},
        "enemies": ["dark_mage"],
        "items": ["spellbook"],
        "npc": "Spirit of Aranthos",
    },
}

ENEMIES: Dict[str, Dict[str, Any]] = {
    "wolf":       {"hp": 20, "attack": 4,  "xp": 10, "gold": 2},
    "goblin":     {"hp": 15, "attack": 3,  "xp": 8,  "gold": 5},
    "bandit":     {"hp": 25, "attack": 6,  "xp": 15, "gold": 12},
    "cave_troll": {"hp": 40, "attack": 8,  "xp": 30, "gold": 20},
    "skeleton":   {"hp": 18, "attack": 5,  "xp": 12, "gold": 3},
    "dark_mage":  {"hp": 50, "attack": 10, "xp": 50, "gold": 40},
}

ITEMS: Dict[str, Dict[str, Any]] = {
    "healing_potion": {"type": "consumable", "effect": "heal",   "value": 20, "desc": "Restores 20 HP."},
    "iron_sword":     {"type": "weapon",     "effect": "attack",  "value": 5,  "desc": "+5 attack power."},
    "leather_armour": {"type": "armour",     "effect": "defence", "value": 3,  "desc": "+3 defence."},
    "stick":          {"type": "weapon",     "effect": "attack",  "value": 2,  "desc": "+2 attack power (barely useful)."},
    "ancient_rune":   {"type": "key",        "effect": None,      "value": 0,  "desc": "A mysterious glowing rune."},
    "gold_coin":      {"type": "currency",   "effect": None,      "value": 1,  "desc": "A shiny gold coin."},
    "spellbook":      {"type": "weapon",     "effect": "attack",  "value": 8,  "desc": "+8 magic attack."},
}

NPC_DIALOGUE: Dict[str, List[str]] = {
    "Elder Mira": [
        "Welcome, traveller. The forest to the north is dangerous — beware the wolves.",
        "Legend has it a powerful relic lies in the ruins to the east.",
        "Seek the Spirit of Aranthos if you wish to understand the ancient magic.",
    ],
    "Merchant Tobias": [
        "Fine weapons and armour, at the best prices in the land!",
        "I hear the cave trolls have been getting bolder lately.",
        "If you find gold coins, bring them to me — I'll give you a fair trade.",
    ],
    "Spirit of Aranthos": [
        "You carry the ancient rune… the prophecy is upon us.",
        "Defeat the dark mage and bring peace to these ruins.",
        "Your courage will be remembered in the stars.",
    ],
}

QUESTS = [
    {
        "id": "slay_wolf",
        "title": "Pest Control",
        "description": "Slay a wolf terrorising the village.",
        "target_enemy": "wolf",
        "count": 1,
        "reward_xp": 25,
        "reward_gold": 15,
        "completed": False,
        "progress": 0,
    },
    {
        "id": "find_rune",
        "title": "The Ancient Rune",
        "description": "Find the ancient rune hidden in the cave.",
        "target_item": "ancient_rune",
        "reward_xp": 40,
        "reward_gold": 0,
        "completed": False,
        "progress": 0,
    },
]


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------

class Player:
    BASE_ATTACK = 5
    BASE_DEFENCE = 2

    def __init__(self, name: str, char_class: str = "Warrior") -> None:
        self.name = name
        self.char_class = char_class
        self.hp = 100
        self.max_hp = 100
        self.attack = self.BASE_ATTACK
        self.defence = self.BASE_DEFENCE
        self.level = 1
        self.xp = 0
        self.xp_to_level = 50
        self.gold = 10
        self.location = "village"
        self.inventory: List[str] = []
        self.quests: List[Dict[str, Any]] = [dict(q) for q in QUESTS]

    # ------------------------------------------------------------------

    def status(self) -> str:
        return (
            f"\n--- {self.name} [{self.char_class}] ---\n"
            f"  HP: {self.hp}/{self.max_hp}  |  Level: {self.level}  "
            f"|  XP: {self.xp}/{self.xp_to_level}\n"
            f"  Attack: {self.attack}  |  Defence: {self.defence}  "
            f"|  Gold: {self.gold}\n"
            f"  Location: {self.location.title()}\n"
        )

    def gain_xp(self, amount: int) -> str:
        self.xp += amount
        msg = f"  +{amount} XP"
        while self.xp >= self.xp_to_level:
            self.xp -= self.xp_to_level
            self.level += 1
            self.xp_to_level = int(self.xp_to_level * 1.5)
            self.max_hp += 10
            self.hp = self.max_hp
            self.attack += 2
            self.defence += 1
            msg += f"\n  *** LEVEL UP! You are now level {self.level}! ***"
        return msg

    def use_item(self, item_name: str) -> str:
        if item_name not in self.inventory:
            return f"  You don't have '{item_name}'."
        item = ITEMS.get(item_name)
        if item is None:
            return f"  Unknown item: {item_name}."
        if item["type"] == "consumable" and item["effect"] == "heal":
            healed = min(item["value"], self.max_hp - self.hp)
            self.hp += healed
            self.inventory.remove(item_name)
            return f"  You used {item_name} and recovered {healed} HP."
        if item["type"] == "weapon":
            self.attack = self.BASE_ATTACK + item["value"]
            return f"  You equipped {item_name}. Attack is now {self.attack}."
        if item["type"] == "armour":
            self.defence = self.BASE_DEFENCE + item["value"]
            return f"  You equipped {item_name}. Defence is now {self.defence}."
        return f"  You examine the {item_name}: {item['desc']}"

    def _check_quests(self, event: str, detail: str) -> str:
        msgs = []
        for quest in self.quests:
            if quest["completed"]:
                continue
            if event == "kill" and quest.get("target_enemy") == detail:
                quest["progress"] += 1
                if quest["progress"] >= quest.get("count", 1):
                    quest["completed"] = True
                    self.xp += quest["reward_xp"]
                    self.gold += quest["reward_gold"]
                    msgs.append(
                        f"\n  *** Quest Complete: '{quest['title']}' ***\n"
                        f"  Reward: {quest['reward_xp']} XP, {quest['reward_gold']} gold"
                    )
            if event == "pickup" and quest.get("target_item") == detail:
                quest["completed"] = True
                self.xp += quest["reward_xp"]
                self.gold += quest["reward_gold"]
                msgs.append(
                    f"\n  *** Quest Complete: '{quest['title']}' ***\n"
                    f"  Reward: {quest['reward_xp']} XP"
                )
        return "\n".join(msgs)


# ---------------------------------------------------------------------------
# RPG Game Engine
# ---------------------------------------------------------------------------

class RPGGame:
    """
    Text-based RPG game engine.

    Usage::

        game = RPGGame()
        game.start()          # Interactive REPL
        # or
        output = game.command("go north")
    """

    HELP_TEXT = """
Available commands:
  look              – describe your surroundings
  go <direction>    – move (north, south, east, west)
  status            – show your character stats
  inventory         – list your items
  pick <item>       – pick up an item
  use <item>        – use an item from your inventory
  talk              – speak with a nearby NPC
  quests            – show active quests
  help              – show this help
  quit              – exit the game
"""

    def __init__(self) -> None:
        self.player: Optional[Player] = None
        self.running = False

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def new_game(self, name: str = "Hero", char_class: str = "Warrior") -> str:
        self.player = Player(name, char_class)
        self.running = True
        return (
            f"\nWelcome, {name} the {char_class}!\n"
            + self._describe_location()
        )

    def command(self, raw: str) -> str:
        """Process a single player command and return the narrative response."""
        if self.player is None:
            return "No active game. Call new_game() first."
        parts = raw.strip().lower().split()
        if not parts:
            return "  (nothing happens)"
        cmd, *args = parts

        if cmd in ("look", "l"):
            return self._describe_location()
        if cmd == "go":
            return self._move(" ".join(args))
        if cmd == "status":
            return self.player.status()
        if cmd in ("inventory", "inv", "i"):
            return self._show_inventory()
        if cmd == "pick":
            return self._pick_item(" ".join(args))
        if cmd == "use":
            return self.player.use_item(" ".join(args))
        if cmd == "talk":
            return self._talk()
        if cmd in ("quests", "q"):
            return self._show_quests()
        if cmd in ("help", "?"):
            return self.HELP_TEXT
        if cmd == "quit":
            self.running = False
            return "  Farewell, brave adventurer. The world will remember your deeds."
        return f"  Unknown command: '{raw}'. Type 'help' for options."

    def start(self) -> None:
        """Launch the interactive REPL."""
        print("\n" + "=" * 50)
        print("   DRAEGTILE CHRONICLES — Open World RPG")
        print("=" * 50)
        name = input("Enter your character's name: ").strip() or "Hero"
        print("Choose a class: [1] Warrior  [2] Mage  [3] Rogue")
        choice = input("Your choice (1-3): ").strip()
        classes = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
        char_class = classes.get(choice, "Warrior")
        print(self.new_game(name, char_class))
        while self.running:
            try:
                raw = input("\n> ")
            except (KeyboardInterrupt, EOFError):
                print("\n  (game interrupted)")
                break
            response = self.command(raw)
            print(response)
            # Trigger random encounter
            encounter = self._random_encounter()
            if encounter:
                print(encounter)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _describe_location(self) -> str:
        p = self.player
        loc = WORLD[p.location]
        exits = ", ".join(loc["exits"].keys())
        items = ", ".join(loc["items"]) if loc["items"] else "nothing"
        npc_line = f"  NPC: {loc['npc']}" if loc["npc"] else ""
        return (
            f"\n{p.location.title()}\n"
            f"  {loc['description']}\n"
            f"  Exits: {exits}\n"
            f"  Items here: {items}"
            + (f"\n{npc_line}" if npc_line else "")
        )

    def _move(self, direction: str) -> str:
        p = self.player
        loc = WORLD[p.location]
        if direction not in loc["exits"]:
            return f"  You can't go {direction} from here."
        p.location = loc["exits"][direction]
        return f"  You head {direction}.\n" + self._describe_location()

    def _show_inventory(self) -> str:
        p = self.player
        if not p.inventory:
            return "  Your inventory is empty."
        lines = [f"  - {item}: {ITEMS[item]['desc']}" for item in p.inventory if item in ITEMS]
        return "  Inventory:\n" + "\n".join(lines)

    def _pick_item(self, item_name: str) -> str:
        p = self.player
        loc = WORLD[p.location]
        if item_name not in loc["items"]:
            return f"  There is no '{item_name}' here."
        loc["items"].remove(item_name)
        p.inventory.append(item_name)
        quest_msg = p._check_quests("pickup", item_name)
        return f"  You picked up {item_name}." + (f"\n{quest_msg}" if quest_msg else "")

    def _talk(self) -> str:
        p = self.player
        npc = WORLD[p.location].get("npc")
        if not npc:
            return "  There is no one here to talk to."
        lines = NPC_DIALOGUE.get(npc, ["..."])
        return f"  {npc}: \"{random.choice(lines)}\""

    def _show_quests(self) -> str:
        p = self.player
        lines = []
        for q in p.quests:
            status = "✔" if q["completed"] else "○"
            lines.append(f"  [{status}] {q['title']}: {q['description']}")
        return "  Quests:\n" + "\n".join(lines)

    def _random_encounter(self) -> Optional[str]:
        p = self.player
        if not self.running:
            return None
        loc = WORLD[p.location]
        if not loc["enemies"]:
            return None
        if random.random() > 0.25:
            return None
        enemy_name = random.choice(loc["enemies"])
        enemy = dict(ENEMIES[enemy_name])
        return self._run_combat(enemy_name, enemy)

    def _run_combat(self, enemy_name: str, enemy: Dict[str, Any]) -> str:
        p = self.player
        lines = [f"\n  *** A {enemy_name} appears! ***"]
        while enemy["hp"] > 0 and p.hp > 0:
            # Player attacks
            player_dmg = max(1, p.attack - random.randint(0, 2))
            enemy["hp"] -= player_dmg
            lines.append(f"  You attack the {enemy_name} for {player_dmg} damage.")
            if enemy["hp"] <= 0:
                break
            # Enemy attacks
            enemy_dmg = max(0, enemy["attack"] - p.defence + random.randint(-1, 1))
            p.hp -= enemy_dmg
            lines.append(f"  The {enemy_name} hits you for {enemy_dmg} damage. (HP: {p.hp}/{p.max_hp})")

        if p.hp <= 0:
            p.hp = 1
            self.running = False
            lines.append(
                f"\n  *** You have been defeated! ***\n"
                f"  The world grows dark... Game Over.\n"
                f"  Final level: {p.level}"
            )
        else:
            xp_msg = p.gain_xp(enemy["xp"])
            p.gold += enemy["gold"]
            quest_msg = p._check_quests("kill", enemy_name)
            lines.append(
                f"  You defeated the {enemy_name}!\n"
                + xp_msg
                + f"\n  +{enemy['gold']} gold"
                + (f"\n{quest_msg}" if quest_msg else "")
            )
        return "\n".join(lines)
