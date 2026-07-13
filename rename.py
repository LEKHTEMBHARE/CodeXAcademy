import os
import re

dir_path = r"c:\Users\Lekh Tembhare\OneDrive\Desktop\CodexPracticals\CodeX_Academy"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    
    # URL encoded image names and regular names
    new_logo = "Code%20for%20Simple%20logo.png"
    new_logo_raw = "Code for Simple logo.png"
    
    # Replace old logos
    new_content = new_content.replace("nextgencoding.png", new_logo_raw)
    new_content = new_content.replace('href="/nextgencoding.png"', f'href="/{new_logo}"')
    new_content = new_content.replace('src="/nextgencoding.png"', f'src="/{new_logo}"')
    
    # Fix existing nav logo structure:
    # <div class="brand">
    #   <span class="brand-mark"></span>
    #   <span class="brand-word" aria-label="CodeX">
    #     <span class="brand-letter">CODE</span><span class="brand-x">X</span>
    #   </span>
    # </div>
    
    brand_regex = re.compile(
        r'<div class="brand">\s*<span class="brand-mark"></span>\s*<span class="brand-word" aria-label="CodeX">\s*<span class="brand-letter">CODE</span><span class="brand-x">X</span>\s*</span>\s*</div>',
        re.DOTALL
    )
    
    new_brand_html = f'''<div class="brand" style="display: flex; align-items: center; gap: 10px;">
        <img src="/{new_logo}" alt="Code For Simples Logo" style="height: 40px; width: auto;" />
        <span class="brand-word" aria-label="Code For Simples" style="font-size: 1.5rem; font-weight: bold;">
          Code For Simples
        </span>
      </div>'''
      
    new_content = brand_regex.sub(new_brand_html, new_content)
    
    # Just in case they are already replaced to Code For Simples by previous script versions
    brand_regex_2 = re.compile(
        r'<div class="brand">\s*<span class="brand-mark"></span>\s*<span class="brand-word" aria-label="Code For Simples">\s*<span class="brand-letter">CODE</span><span class="brand-x">X</span>\s*</span>\s*</div>',
        re.DOTALL
    )
    new_content = brand_regex_2.sub(new_brand_html, new_content)

    # General replacements
    new_content = new_content.replace("CodeX Academy", "Code For Simples")
    new_content = new_content.replace("CodeX", "Code For Simples")
    new_content = new_content.replace("codex", "code-for-simples")
    
    # Fix paths
    new_content = new_content.replace("Code%20For%20Simples%20logo.png", "Code%20for%20Simple%20logo.png")

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

for root, dirs, files in os.walk(dir_path):
    if ".git" in root or ".vscode" in root:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.json', '.md', '.py', '.txt')):
            file_path = os.path.join(root, file)
            if file == "rename_codex.py" or file == "rename.py":
                continue
            process_file(file_path)
