
import re

TARGET_FILE = "chapter2_lesson2.html"

def audit_file():
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex for vocab cards (supporting xl-4xl)
    vocab_pattern = re.compile(r'<span class="text-[1-4]?xl font-bold text-slate-800">([^<]+)</span>')
    
    matches = list(vocab_pattern.finditer(content))
    
    print(f"Found {len(matches)} vocabulary cards.")
    
    missing_report = {}
    
    for match in matches:
        vocab = match.group(1)
        start_idx = match.start()
        
        # Look ahead for container
        container_match = re.search(r'class="mt-[24] pt-[23] border-t border-slate-200/50 space-y-[12]">', content[start_idx:])
        
        if not container_match:
            print(f"[ERROR] Container not found for: {vocab}")
            continue
            
        container_start = start_idx + container_match.end()
        # Scan next 1000 chars roughly
        search_chunk = content[container_start:container_start+1500]
        
        missing = []
        if '构词' not in search_chunk: missing.append("Structure")
        if '词源' not in search_chunk: missing.append("Origin")
        if '记忆' not in search_chunk: missing.append("Memory")
        if '用法' not in search_chunk: missing.append("Usage")
        
        if missing:
            missing_report[vocab] = missing
            print(f"[MISSING] {vocab}: {', '.join(missing)}")
        else:
            # print(f"[OK] {vocab}")
            pass

    print("-" * 30)
    print(f"Total cards with missing sections: {len(missing_report)}")
    if not missing_report:
        print("ALL VOCAB CARDS ARE COMPLETE!")

if __name__ == "__main__":
    audit_file()
