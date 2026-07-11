import os
import glob
import re

# 1. Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 2. Extract the navbar
match = re.search(r'(<header class="nav">.*?</header>)', index_content, re.DOTALL)
if not match:
    print("Could not find navbar in index.html")
    exit(1)

navbar_base = match.group(1)

# 3. Fix paths to be root-relative so they work exactly identically on all pages
navbar_fixed = navbar_base
# Replace relative paths with absolute paths starting with /
replacements = {
    'href="index.html"': 'href="/index.html"',
    'href="about.html"': 'href="/about.html"',
    'href="services.html"': 'href="/services.html"',
    'href="Courses/courses.html"': 'href="/Courses/courses.html"',
    'href="Events/events.html"': 'href="/Events/events.html"',
    'href="Team/team.html"': 'href="/Team/team.html"',
    'href="register.html"': 'href="/register.html"',
    'href="contact.html"': 'href="/contact.html"'
}

for old, new in replacements.items():
    navbar_fixed = navbar_fixed.replace(old, new)

# 4. We want to apply this exact same HTML string to ALL pages.
# Wait, for the 'active' class, ideally we want it to reflect the current page.
# "Keep the EXACT same active link styling."
# If I use the *exact* identical string, the 'active' class will always be on "Home".
# If I keep the active styling, I need to strip 'class="active"' from the base,
# and dynamically add it based on the page name.
# Let's write logic for that.

html_files = glob.glob('**/*.html', recursive=True)
updated_files = []

for file in html_files:
    file = file.replace('\\', '/')
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the existing navbar
    existing_match = re.search(r'(<header class="nav">.*?</header>)', content, re.DOTALL)
    if not existing_match:
        # Some files like 404.html might not have a header, skip them
        continue
    
    # Strip active class from our fixed base
    clean_navbar = re.sub(r'\s*class="active"', '', navbar_fixed)

    # Determine which link should have the active class
    if file == 'index.html':
        clean_navbar = clean_navbar.replace('href="/index.html"', 'href="/index.html" class="active"')
    elif file == 'about.html':
        clean_navbar = clean_navbar.replace('href="/about.html"', 'href="/about.html" class="active"')
    elif file == 'services.html':
        clean_navbar = clean_navbar.replace('href="/services.html"', 'href="/services.html" class="active"')
    elif 'courses.html' in file:
        clean_navbar = clean_navbar.replace('href="/Courses/courses.html"', 'href="/Courses/courses.html" class="active"')
    elif 'events.html' in file:
        clean_navbar = clean_navbar.replace('href="/Events/events.html"', 'href="/Events/events.html" class="active"')
    elif 'team.html' in file:
        clean_navbar = clean_navbar.replace('href="/Team/team.html"', 'href="/Team/team.html" class="active"')
    elif 'register.html' in file:
        clean_navbar = clean_navbar.replace('href="/register.html"', 'href="/register.html" class="active"')
    elif 'contact.html' in file:
        clean_navbar = clean_navbar.replace('href="/contact.html"', 'href="/contact.html" class="active"')

    new_content = content[:existing_match.start()] + clean_navbar + content[existing_match.end():]
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_files.append(file)

print(f"Updated navbars in: {', '.join(updated_files)}")
