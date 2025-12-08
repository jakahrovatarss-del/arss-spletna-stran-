
with open(r'C:\Users\MojPC\.gemini\antigravity\scratch\arss-website\gospodinjstva.html', 'r', encoding='utf-8') as f:
    for line in f:
        if 'natan' in line or 'pu' in line:
            print(f"Line: {line.strip()}")
            print(f"Repr: {ascii(line.strip())}")
            try:
                # Try common fixes
                fixed = line.encode('cp1252').decode('utf-8')
                print(f"Fix cp1252: {fixed.strip()}")
            except Exception as e:
                print(f"Fix cp1252 failed: {e}")
            
            try:
                fixed = line.encode('latin1').decode('utf-8')
                print(f"Fix latin1: {fixed.strip()}")
            except Exception as e:
                print(f"Fix latin1 failed: {e}")
                
            break
