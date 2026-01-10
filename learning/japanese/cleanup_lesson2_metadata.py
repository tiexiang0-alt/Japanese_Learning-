
import re

TARGET_FILE = "chapter2_lesson2.html"

def process_file():
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all vocab cards
    vocab_pattern = re.compile(r'<span class="text-[1-4]?xl font-bold text-slate-800">([^<]+)</span>')
    matches = list(vocab_pattern.finditer(content))
    
    # We iterate backwards to avoid index shifts affecting unprocessed items
    for match in reversed(matches):
        vocab = match.group(1)
        start_idx = match.start()
        
        # Find container
        container_match = re.search(r'class="mt-[24] pt-[23] border-t border-slate-200/50 space-y-[12]">', content[start_idx:])
        
        if not container_match:
            continue
            
        container_start = start_idx + container_match.end()
        
        # Find End of Container (heuristically, look for next glass-panel or section end, or count divs?)
        # Simple heuristic: scan until next string likely to be outside card
        # Or look for closing div.
        # Since we just want to remove dupes inside the immediate block.
        # Let's verify dupes in the next 1500 chars.
        
        search_chunk = content[container_start:container_start+1500]
        
        # Check for closing div of the container to limit scope strictly
        # Count open/close divs? Too complex.
        # Just find `</div>` that aligns?
        # Let's assume the duplicate is close by.
        
        # Function to remove first occurrence if duplicate exists
        def remove_duplicate(label):
            pattern = f'<span class="font-bold .*? shrink-0">{label}</span>'
            # Find all matches in chunk
            section_matches = list(re.finditer(pattern, search_chunk))
            
            if len(section_matches) > 1:
                print(f"Found {len(section_matches)} {label} sections for {vocab}. Removing first one (presumed generic injection).")
                
                # We need to remove the whole DIV containing this span.
                # <div class="flex items-start gap-2 text-xs"> ... </div>
                
                # Locate the match
                first_match = section_matches[0]
                
                # Find start of the div containing this match
                # Search backwards from mismatch start
                div_start_rel = search_chunk.rfind('<div', 0, first_match.start())
                
                # Find end of the div
                div_end_match = re.search(r'</div>', search_chunk[first_match.end():])
                if div_end_match:
                    div_end_rel = first_match.end() + div_end_match.end()
                    
                    # Remove from content
                    # Need absolute indices
                    abs_start = container_start + div_start_rel
                    abs_end = container_start + div_end_rel
                    
                    return (abs_start, abs_end)
            return None

        # Check duplicates for Structure, Memory, Origin
        for label in ["构词", "记忆", "词源"]:
            removal = remove_duplicate(label)
            if removal:
                # remove slice
                content = content[:removal[0]] + content[removal[1]:]
                # Update loop? content changed.
                # Since we reverse iterate matches, valid for PREVIOUS items, but current item changed?
                # We are inside the vocab loop.
                # We modified `content` for THIS vocab.
                # If we modify, we should break and restart or handle offset?
                # Since we process ONE label at a time, removing one changes offsets for SUBSEQUENT labels in SAME chunk.
                # Simplest: Just run the script multipass or re-read chunk?
                # re-read chunk is hard if we modified `content`.
                # We can update `container_start`?
                # Actually, `container_start` doesn't change if we remove AFTER it. Yes.
                # But `search_chunk` is stale.
                # So we should `continue` the loop and let the script pass again?
                # Or re-fetch `search_chunk`?
                
                # Re-fetch chunk
                search_chunk = content[container_start:container_start+1500] 
                # continue to next label check

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    process_file()
