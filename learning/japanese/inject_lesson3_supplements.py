
import os
import re

def inject_content():
    base_dir = '/Users/hardentie/Downloads/vscode/learning/japanese'
    supplements_path = os.path.join(base_dir, 'lesson3_supplements.html')
    target_path = os.path.join(base_dir, 'chapter2_lesson3.html')

    with open(supplements_path, 'r', encoding='utf-8') as f:
        supplements_html = f.read()

    # Extract sections
    vocab_match = re.search(r'<!-- VOCAB START -->\s*(.*?)\s*<!-- VOCAB END -->', supplements_html, re.DOTALL)
    grammar_match = re.search(r'<!-- GRAMMAR START -->\s*(.*?)\s*<!-- GRAMMAR END -->', supplements_html, re.DOTALL)
    culture_match = re.search(r'<!-- CULTURE START -->\s*(.*?)\s*<!-- CULTURE END -->', supplements_html, re.DOTALL)

    if not vocab_match or not grammar_match or not culture_match:
        print("Error: Could not extract all sections from supplements file.")
        return

    vocab_content = vocab_match.group(1)
    grammar_content = grammar_match.group(1)
    culture_content = culture_match.group(1)

    with open(target_path, 'r', encoding='utf-8') as f:
        target_html = f.read()

    # 1. Inject Vocab
    # Find the '国' card and the closing div of the grid
    # We look for the comment <!-- 国 --> and then the closing </div> of the grid container content
    # The grid ends with </div> followed by </section> usually, or just look for the last card's closing.
    # A safer marker is finding the "Number Pronunciation Variations" section start, and inserting before the preceding section close.
    # Marker: <!-- Number Pronunciation Variations -->
    # The structure before it is:
    # </div> (grid close)
    # </div> (container close?)
    # </section> (Additional Vocab section close)
    
    # Let's try to insert at the end of the "Additional Vocabulary" grid.
    # We know the last card is "国" (Kuni).
    # We search for that and then find the closing div of the grid.
    
    marker_vocab = '<!-- 国 -->'
    if marker_vocab not in target_html:
        print("Error: Vocab marker '<!-- 国 -->' not found.")
        return
        
    # Find the position of the marker
    idx_vocab = target_html.find(marker_vocab)
    # Find the closing tag of the grid. The grid is <div class="grid ..."> ... </div>
    # The "国" card is inside the grid.
    # We can assume the first </div> after the card content closes the card, and the second one closes the grid?
    # No, cards have nested divs.
    # Let's count indentations or just look for the known closing sequence.
    # In step 2609, we saw:
    # 2254:                     </div>
    # 2255: 
    # 2256:                 </div>
    # 2257:             </section>
    # 2258: 
    # 2259: 
    # 2260:             <!-- Number Pronunciation Variations -->
    
    # So we can search for `<!-- Number Pronunciation Variations -->` and back up to find `</section>` then `</div>`.
    # And insert BEFORE that `</div>`.
    
    marker_num_variations = '<!-- Number Pronunciation Variations -->'
    parts_vocab = target_html.split(marker_num_variations)
    if len(parts_vocab) != 2:
         print("Error: Unique marker '<!-- Number Pronunciation Variations -->' not found or duplicated.")
         return
         
    pre_vocab = parts_vocab[0]
    post_vocab = parts_vocab[1]
    
    # Find the last </div> inside pre_vocab (which should be the grid closing)
    # Actually, pre_vocab ends with:
    # </div>
    # </section>
    # \n\n
    
    # Let's use regex to find the insertion point relative to the end of pre_vocab
    # We want to insert inside the grid, so before the `</div>` that is before `</section>`.
    
    # Regex to find the last </div> before </section> at the end of the string
    # Note: We need to be careful about not matching too much.
    
    # Simpler approach: replace `</div>\s*</section>\s*$` of pre_vocab section? No.
    
    # Start searching from the end of pre_vocab
    idx_section_close = pre_vocab.rfind('</section>')
    if idx_section_close == -1:
        print("Error: </section> not found before Number Variations.")
        return
        
    # Search backwards for </div> from section close
    idx_grid_close = pre_vocab.rfind('</div>', 0, idx_section_close)
    if idx_grid_close == -1:
        print("Error: </div> not found before vocab section close.")
        return
        
    # Insert vocab content
    new_pre_vocab = pre_vocab[:idx_grid_close] + '\n' + vocab_content + '\n' + pre_vocab[idx_grid_close:]
    
    target_html = new_pre_vocab + marker_num_variations + post_vocab
    
    # 2. Inject Grammar
    # Marker: <!-- 4. Culture Section -->
    marker_culture_section = '<!-- 4. Culture Section -->'
    if marker_culture_section not in target_html:
        print("Error: Marker '<!-- 4. Culture Section -->' not found.")
        return
    
    parts_grammar = target_html.split(marker_culture_section)
    pre_grammar = parts_grammar[0]
    post_grammar = parts_grammar[1]
    
    # Find the last </div> in pre_grammar (which closes content-grammar)
    idx_grammar_div_close = pre_grammar.rfind('</div>')
    if idx_grammar_div_close == -1:
         print("Error: </div> not found before Culture Section.")
         return
         
    # Insert grammar content before the div close
    # But wait, grammar_content is a list of blocks. It should be inside the main grammar container.
    # The last existing block is a grammar point.
    # Inserting before the last </div> puts it inside the container. Correct.
    
    new_pre_grammar = pre_grammar[:idx_grammar_div_close] + '\n' + grammar_content + '\n' + pre_grammar[idx_grammar_div_close:]
    target_html = new_pre_grammar + marker_culture_section + post_grammar
    
    # 3. Inject Culture
    # Marker: <!-- 5. Practice Section -->
    marker_practice_section = '<!-- 5. Practice Section -->'
    if marker_practice_section not in target_html:
         # Fallback to id if comments are different
         marker_practice_section = '<div id="content-practice"'
         if marker_practice_section not in target_html:
             print("Error: Marker for Practice Section not found.")
             return
             
    parts_culture = target_html.split(marker_practice_section)
    pre_culture = parts_culture[0]
    post_culture = parts_culture[1]
    
    # Find the last </div> in pre_culture (closes content-culture)
    idx_culture_div_close = pre_culture.rfind('</div>')
    if idx_culture_div_close == -1:
        print("Error: </div> not found before Practice Section.")
        return
        
    new_pre_culture = pre_culture[:idx_culture_div_close] + '\n' + culture_content + '\n' + pre_culture[idx_culture_div_close:]
    
    target_html = new_pre_culture + marker_practice_section + post_culture
    
    # Write back
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(target_html)
        
    print("Successfully injected all content.")

if __name__ == '__main__':
    inject_content()
