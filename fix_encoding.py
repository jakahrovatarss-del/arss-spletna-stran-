
import os

files = [
    r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\gospodinjstva.html',
    r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\industrija.html',
    r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\merjenje.html',
    r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\referenca-vecstanovanjski.html',
    r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\referenca-komunala.html'
]

def fix_text(text):
    result = []
    byte_buffer = bytearray()
    
    for char in text:
        b = None
        try:
            b = char.encode('cp1252')
        except UnicodeEncodeError:
            try:
                b = char.encode('latin-1')
            except UnicodeEncodeError:
                b = None
        
        if b is not None:
            byte_buffer.extend(b)
        else:
            if byte_buffer:
                try:
                    fixed = byte_buffer.decode('utf-8')
                    result.append(fixed)
                except UnicodeDecodeError:
                    # If not valid utf-8, keep original chars?
                    # This is tricky because we have bytes now, not chars.
                    # We need to reconstruct the original chars from bytes.
                    # But we mixed cp1252 and latin-1.
                    # Actually, if we just decode as cp1252 (or latin-1), we might get close?
                    # But we don't know which one was used for which byte.
                    # However, since we are fixing *corruption*, the goal is to get UTF-8.
                    # If it's NOT UTF-8, it probably wasn't corrupted in this way.
                    # But we can't easily revert to original chars from the byte buffer 
                    # if we don't track which encoding was used.
                    # Simpler: just append the "latin-1" decoded version of bytes?
                    # No, that might be wrong for cp1252 chars.
                    
                    # Let's try to be safe: if decode fails, we assume it wasn't a UTF-8 sequence.
                    # But we need to output *something*.
                    # Let's try to decode as cp1252 as a fallback (most chars are cp1252).
                    try:
                        result.append(byte_buffer.decode('cp1252'))
                    except:
                         result.append(byte_buffer.decode('latin-1', errors='replace'))
                byte_buffer = bytearray()
            result.append(char)
    
    if byte_buffer:
        try:
            fixed = byte_buffer.decode('utf-8')
            result.append(fixed)
        except UnicodeDecodeError:
             try:
                result.append(byte_buffer.decode('cp1252'))
             except:
                result.append(byte_buffer.decode('latin-1', errors='replace'))
            
    return "".join(result)

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (not found)")
        continue
        
    try:
        # Read with utf-8-sig to handle BOM if present
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        fixed_content = fix_text(content)
        
        # Write back as utf-8 (no BOM usually preferred, or standard utf-8)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        print(f"Fixed {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
