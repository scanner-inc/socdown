#!/usr/bin/env python3
"""
SOC Investigation Codename Generator

Generates unique, memorable codenames for security investigations using
large word lists and collision avoidance.

Usage:
    python codename_generator.py                    # Generate single codename
    python codename_generator.py --check existing   # Check if codename exists
    python codename_generator.py --bulk 10          # Generate 10 codenames
"""

import random
import argparse
import os
import glob
from pathlib import Path

# Large adjective list for maximum variety
ADJECTIVES = [
    # Technical/Security themed
    "encrypted", "secure", "stealthy", "phantom", "shadow", "cyber", "digital",
    "quantum", "binary", "neural", "atomic", "photon", "laser", "plasma",
    "turbo", "ultra", "mega", "super", "hyper", "nano", "micro", "macro",
    
    # Colors
    "crimson", "azure", "emerald", "golden", "silver", "copper", "bronze",
    "violet", "scarlet", "amber", "jade", "ruby", "sapphire", "onyx",
    "pearl", "coral", "ivory", "obsidian", "chrome", "titanium",
    
    # Weather/Nature
    "stormy", "misty", "frosty", "blazing", "arctic", "volcanic", "solar",
    "lunar", "stellar", "cosmic", "oceanic", "alpine", "desert", "tropical",
    "tundra", "glacier", "thunder", "lightning", "tornado", "hurricane",
    
    # Characteristics - Positive
    "swift", "agile", "precise", "sharp", "keen", "bright", "clever", "wise",
    "bold", "brave", "fierce", "strong", "mighty", "powerful", "robust",
    "sleek", "smooth", "graceful", "elegant", "refined", "polished",
    
    # Characteristics - Neutral/Technical
    "silent", "hidden", "masked", "cloaked", "veiled", "covert", "discrete",
    "subtle", "quiet", "calm", "steady", "stable", "solid", "dense",
    "compact", "minimal", "clean", "pure", "pristine", "perfect",
    
    # Size/Scale
    "giant", "massive", "huge", "enormous", "colossal", "vast", "immense",
    "tiny", "mini", "small", "petite", "slim", "narrow", "wide", "broad",
    "tall", "short", "long", "deep", "shallow", "thick", "thin",
    
    # Texture/Surface
    "smooth", "rough", "jagged", "curved", "angular", "spiral", "twisted",
    "straight", "bent", "flat", "round", "square", "sharp", "blunt",
    "crystalline", "metallic", "ceramic", "plastic", "wooden", "stone",
    
    # Movement/Speed
    "rapid", "slow", "fast", "quick", "speedy", "hasty", "gradual",
    "sudden", "instant", "delayed", "steady", "erratic", "flowing",
    "rushing", "creeping", "sliding", "rolling", "spinning", "orbiting",
    
    # Temperature
    "hot", "cold", "warm", "cool", "freezing", "boiling", "scorching",
    "chilled", "heated", "temperate", "mild", "extreme", "moderate",
    
    # Light/Dark
    "bright", "dim", "glowing", "radiant", "luminous", "brilliant", "dazzling",
    "dark", "shadowy", "murky", "clear", "transparent", "opaque", "translucent",
    
    # Abstract Qualities
    "mysterious", "enigmatic", "puzzling", "complex", "simple", "basic",
    "advanced", "sophisticated", "primitive", "modern", "ancient", "futuristic",
    "classic", "vintage", "retro", "contemporary", "traditional", "innovative"
]

# Large noun list with security/tech theme
NOUNS = [
    # Animals - Predators/Strong
    "tiger", "lion", "eagle", "hawk", "falcon", "wolf", "bear", "shark",
    "panther", "leopard", "cheetah", "jaguar", "cobra", "viper", "python",
    "dragon", "phoenix", "griffin", "sphinx", "hydra", "kraken", "leviathan",
    
    # Animals - Tech/Cyber themed
    "spider", "octopus", "mantis", "scorpion", "wasp", "hornet", "beetle",
    "ant", "termite", "locust", "cicada", "firefly", "moth", "butterfly",
    "dragonfly", "mosquito", "bee", "drone", "swarm", "hive",
    
    # Animals - Swift/Agile
    "rabbit", "hare", "deer", "gazelle", "antelope", "mustang", "stallion",
    "mare", "colt", "foal", "zebra", "unicorn", "pegasus", "centaur",
    
    # Animals - Aquatic
    "dolphin", "whale", "orca", "seal", "walrus", "penguin", "albatross",
    "pelican", "seagull", "cormorant", "turtle", "tortoise", "crab", "lobster",
    "shrimp", "jellyfish", "starfish", "seahorse", "swordfish", "marlin",
    
    # Technology/Computing
    "processor", "circuit", "matrix", "algorithm", "protocol", "interface",
    "terminal", "console", "server", "client", "daemon", "kernel", "shell",
    "compiler", "debugger", "parser", "lexer", "tokenizer", "encoder",
    "decoder", "cipher", "hash", "key", "token", "session", "thread",
    
    # Weapons/Military
    "sword", "blade", "dagger", "spear", "lance", "arrow", "bow", "shield",
    "armor", "helmet", "cannon", "rifle", "pistol", "missile", "torpedo",
    "grenade", "bomb", "mine", "trap", "snare", "net", "hook", "anchor",
    
    # Space/Celestial
    "star", "planet", "moon", "comet", "meteor", "asteroid", "nebula",
    "galaxy", "constellation", "orbit", "satellite", "probe", "rocket",
    "shuttle", "station", "portal", "wormhole", "blackhole", "quasar",
    "pulsar", "supernova", "cosmos", "universe", "dimension", "void",
    
    # Natural Features
    "mountain", "volcano", "glacier", "canyon", "valley", "plateau", "cliff",
    "cave", "cavern", "chasm", "crater", "gorge", "ravine", "ridge",
    "peak", "summit", "slope", "ledge", "outcrop", "boulder", "stone",
    
    # Weather/Natural Forces
    "storm", "tempest", "hurricane", "tornado", "cyclone", "typhoon",
    "thunder", "lightning", "blizzard", "avalanche", "earthquake", "tsunami",
    "flood", "drought", "wildfire", "inferno", "geyser", "rapids", "cascade",
    
    # Precious Materials
    "diamond", "emerald", "ruby", "sapphire", "topaz", "amethyst", "opal",
    "pearl", "coral", "amber", "crystal", "quartz", "granite", "marble",
    "gold", "silver", "platinum", "copper", "bronze", "steel", "iron",
    "titanium", "aluminum", "chromium", "cobalt", "nickel", "zinc",
    
    # Structures/Architecture
    "tower", "fortress", "castle", "citadel", "stronghold", "bastion",
    "rampart", "wall", "gate", "bridge", "arch", "dome", "spire", "pillar",
    "column", "beam", "girder", "foundation", "scaffold", "framework",
    
    # Energy/Power
    "dynamo", "generator", "reactor", "engine", "motor", "turbine", "rotor",
    "propeller", "gear", "spring", "lever", "pulley", "piston", "valve",
    "pump", "compressor", "capacitor", "resistor", "transistor", "diode",
    
    # Abstract Concepts
    "nexus", "vertex", "apex", "zenith", "nadir", "equilibrium", "paradox",
    "anomaly", "singularity", "infinity", "eternity", "destiny", "legacy",
    "heritage", "tradition", "innovation", "revolution", "evolution",
    
    # Mythological/Fantasy
    "titan", "giant", "colossus", "golem", "elemental", "wraith", "specter",
    "phantom", "ghost", "spirit", "essence", "soul", "avatar", "guardian",
    "sentinel", "warden", "keeper", "protector", "defender", "champion"
]

def generate_codename():
    """Generate a random codename with format: adjective-adjective-noun"""
    adj1 = random.choice(ADJECTIVES)
    adj2 = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    
    # Ensure the two adjectives are different
    while adj2 == adj1:
        adj2 = random.choice(ADJECTIVES)
    
    return f"{adj1}-{adj2}-{noun}"

def check_codename_exists(codename, base_path="investigations"):
    """Check if a codename already exists in any investigation file"""
    if not os.path.exists(base_path):
        return False
    
    # Search for any .md file containing this codename
    pattern = os.path.join(base_path, "**", f"*.{codename}.md")
    matches = glob.glob(pattern, recursive=True)
    return len(matches) > 0

def generate_unique_codename(base_path="investigations", max_attempts=1000):
    """Generate a unique codename that doesn't exist in the investigation files"""
    for attempt in range(max_attempts):
        codename = generate_codename()
        if not check_codename_exists(codename, base_path):
            return codename
    
    # If we can't find a unique one after many attempts, just return one
    # (this is extremely unlikely with our large word lists)
    print(f"Warning: Could not find unique codename after {max_attempts} attempts")
    return generate_codename()

def get_word_stats():
    """Return statistics about the word lists"""
    adj_count = len(ADJECTIVES)
    noun_count = len(NOUNS)
    total_combinations = adj_count * (adj_count - 1) * noun_count  # -1 because adj1 != adj2
    
    return {
        "adjectives": adj_count,
        "nouns": noun_count,
        "total_combinations": total_combinations
    }

def main():
    parser = argparse.ArgumentParser(description="Generate SOC investigation codenames")
    parser.add_argument("--check", help="Check if a specific codename exists")
    parser.add_argument("--bulk", type=int, help="Generate multiple codenames")
    parser.add_argument("--stats", action="store_true", help="Show word list statistics")
    parser.add_argument("--path", default="investigations", help="Base path for investigations")
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_word_stats()
        print(f"Word List Statistics:")
        print(f"  Adjectives: {stats['adjectives']:,}")
        print(f"  Nouns: {stats['nouns']:,}")
        print(f"  Total possible combinations: {stats['total_combinations']:,}")
        return
    
    if args.check:
        exists = check_codename_exists(args.check, args.path)
        print(f"Codename '{args.check}' {'exists' if exists else 'does not exist'}")
        return
    
    if args.bulk:
        print(f"Generating {args.bulk} unique codenames:")
        for i in range(args.bulk):
            codename = generate_unique_codename(args.path)
            print(f"{i+1:2d}. {codename}")
        return
    
    # Default: generate single unique codename
    codename = generate_unique_codename(args.path)
    print(codename)

if __name__ == "__main__":
    main()