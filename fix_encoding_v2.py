
import os

# Map of common Mojibake (Windows-1252/Latin-1 interpretation of UTF-8) to correct UTF-8 characters
REPLACEMENTS = {
    "ÄŒ": "Č",
    "Ä‚": "č", # potentially "Ä" followed by something else
    "Ä": "č",   # fallback if followed by specific char, but risky. Better:
    "Å¾": "ž",
    "Å½": "Ž",
    "Å¡": "š",
    "ÅŠ": "Š",
    "Ä‡": "ć",
    "Ä†": "Ć",
    "â‚¬": "€",
    # Specific sequences often seen
    "puÅ¡Äanje": "puščanje",
    "reÅ¡itev": "rešitev",
    "ReÅ¡itev": "Rešitev",
    "raÄun": "račun",
    "kotliÄek": "kotliček",
    "prihranijo": "prihranijo", # usually fine but check context
    "natanÄnost": "natančnost",
    "NatanÄnost": "Natančnost",
    "Å½ivljenjska": "Življenjska",
    "Å½ivljenska": "Življenjska",
    "GrafiÄni": "Grafični",
    "nenavadno": "nenavadno",
    "vzdrÅ¾evanje": "vzdrževanje",
    "zanesljivost": "zanesljivost",
    "naÄrtovanje": "načrtovanje",
    "obÄina": "občina"
}

# More generic byte-sequence replacements if the above specific words miss
# UTF-8 'č' is \xc4\x8d. In cp1252, \xc4 is 'Ä' and \x8d is undefined/control or '' depending on variant.
# UTF-8 'š' is \xc5\xa1. In cp1252, \xc5 is 'Å', \xa1 is '¡'. So 'Å¡' -> 'š'.
# UTF-8 'ž' is \xc5\xbe. In cp1252, \xc5 is 'Å', \xbe is '¾'. So 'Å¾' -> 'ž'.

GENERIC_MAP = {
    "Å¡": "š",
    "ÅŠ": "Š",
    "Å¾": "ž",
    "Å½": "Ž",
    "Ä": "č",  # Warning: partial match for Č/č/ć. 
    # Use context or more specific maps. 
    # 'č' -> c4 8d -> Ä <control>
    # 'Č' -> c4 8c -> Ä <control>
    # 'ć' -> c4 87 -> Ä ‡
    # 'Ć' -> c4 86 -> Ä †
    
    # Common ones
    "Ä‡": "ć",
    "Ä†": "Ć",
    "Ã—": "×",
    "â‚¬": "€",
}

def fix_file(filepath):
    print(f"Checking {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='cp1252') as f:
                content = f.read()
        except Exception as e:
            print(f"Failed to read {filepath}: {e}")
            return

    new_content = content
    
    # Phase 1: Specific words (safer)
    for bad, good in REPLACEMENTS.items():
        if bad in new_content:
            new_content = new_content.replace(bad, good)
            # print(f"  Fixed specific: {bad} -> {good}") # Commented out to avoid console encoding errors

    # Phase 2: Generic patterns for remaining (less safe, check carefully)
    # Only do safe ones first
    safe_generics = {
        "Å¡": "š", "ÅŠ": "Š", "Å¾": "ž", "Å½": "Ž", "Ä‡": "ć", "Ä†": "Ć", "â‚¬": "€"
    }
    for bad, good in safe_generics.items():
        if bad in new_content:
            new_content = new_content.replace(bad, good)
            # print(f"  Fixed generic: {bad} -> {good}") # Commented out

    # Phase 3: The tricky 'č' and 'Č'. 
    # In mojibake involving utf-8 viewed as cp1252, 'č' becomes 'Ä' followed by a control char (0x8D).
    # Python might read this control char or just 'Ä' if stripped. 
    # Often 'Ä' appears alone if the next byte was swallowed or displayed as block.
    # We will replace 'Ä' plus the next char if it looks like the pattern.
    
    # Actually, simplest is to just look for common "Ä" patterns in Slovenian words if possible,
    # or replace "Ä" with "č" if it seems right.
    # Let's try text based replacement for 'Ä' where it is likely 'č'.
    
    if "Ä" in new_content:
        # Common suffixes/prefixes involves c
        # Manual patches for what we saw in screenshots:
        # "NatanÄnost" -> c4 8d is č
        # "NatanÄ" -> likely Natanč
        
        # NOTE: Be careful not to replace valid weird chars if any.
        pass

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Saved changes to {filepath}")
    else:
        print("  No changes needed.")

def main():
    folder = "C:\\Users\\MojPC\\.gemini\\antigravity\\scratch\\arss-website"
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            fix_file(os.path.join(folder, filename))

if __name__ == "__main__":
    main()
