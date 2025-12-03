import re

# Read the file
with open(r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\industrija.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the second </ul> in the "Naše reference" section (after "Komunalni vodovod")
# We'll use a targeted pattern that matches the specific structure

pattern = r'(<li>Odprava potrebe po terenskem odčitavanju</li>\s*</ul>)(\s*</div>)'
replacement = r'\1\n                        <a href="referenca-komunala.html" class="btn-secondary" style="margin-top: 1.5rem; display: inline-block;">Izvedi več →</a>\2'

# Replace
new_content = re.sub(pattern, replacement, content, count=1)

# Write back
with open(r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\industrija.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Button added successfully!")
