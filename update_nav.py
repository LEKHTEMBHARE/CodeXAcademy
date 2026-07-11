import os
import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
for file in html_files:
    if file == 'index.html': continue

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<button class="menu-toggle"' in content:
        continue
    
    # Add id to nav-links
    content = re.sub(r'<nav class="nav-links">', r'<button class="menu-toggle" id="mobile-menu-btn" aria-label="Toggle Menu">\n        <i data-lucide="menu"></i>\n      </button>\n      <nav class="nav-links" id="nav-links">', content)
    
    # Add nav-cta to the enroll now button
    content = re.sub(r'<a class="btn btn-small" href="([^"]+)">([^<]+)</a>\n    </div>\n  </header>', r'<a class="btn btn-small nav-cta" href="\1">\2</a>\n    </div>\n  </header>', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print(f'Updated {len(html_files)} files.')
