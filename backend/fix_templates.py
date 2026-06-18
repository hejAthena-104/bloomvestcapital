#!/usr/bin/env python3
"""
Script to fix hardcoded user data in dashboard templates
"""
import os
import re

# Define template directory
TEMPLATE_DIR = '/mnt/c/Users/Emmanuel/Desktop/Projects/dynamicsdigitalasset.com/backend/templates/dashboard'

# Define replacements
REPLACEMENTS = [
    # Fix hardcoded user name and email in dropdown
    (
        r'<h4 class="mb-0">potus saint patrick</h4>\s*<p class="card-text">thebagnft@gmail\.com</p>',
        '<h4 class="mb-0">{{ user.get_full_name }}</h4>\n                                    <p class="card-text">{{ user.email }}</p>'
    ),
    # Fix welcome message
    (
        r'Welcome, potus saint patrick!',
        'Welcome, {{ user.get_full_name }}!'
    ),
]

def fix_template(filepath):
    """Fix a single template file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Apply replacements
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)

    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {os.path.basename(filepath)}")
        return True
    else:
        print(f"- Skipped: {os.path.basename(filepath)} (no changes needed)")
        return False

def main():
    """Main function"""
    print("Fixing dashboard templates...")
    print("=" * 60)

    fixed_count = 0

    # Walk through dashboard directory
    for root, dirs, files in os.walk(TEMPLATE_DIR):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                if fix_template(filepath):
                    fixed_count += 1

    print("=" * 60)
    print(f"Fixed {fixed_count} template(s)")

if __name__ == '__main__':
    main()
