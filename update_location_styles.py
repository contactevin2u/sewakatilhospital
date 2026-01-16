import os
import re
import glob

# Mobile styles from Selangor page
MOBILE_STYLES = '''    <!-- Mobile Styles -->
    <style>
        @media (max-width: 768px) {
            /* Hero container fill screen on mobile */
            .hero-section {
                padding: 0 !important;
            }

            .hero-section > .container {
                padding: 0 !important;
                max-width: 100% !important;
            }

            .hero-container {
                border-radius: 0 !important;
                margin: 0 !important;
                padding: 30px 20px !important;
            }

            /* Reorder hero elements on mobile */
            .hero-left {
                display: flex !important;
                flex-direction: column !important;
            }

            .hero-cert-badge {
                order: 3 !important;
                margin-bottom: 0 !important;
                justify-content: center !important;
                width: 100% !important;
            }

            .hero-cert-badge .cert-icons img {
                width: 110px !important;
                height: auto !important;
            }

            .hero-cert-badge .cert-text {
                font-size: 0.85rem !important;
            }

            .hero-product-mobile {
                order: 2 !important;
            }

            .hero-buttons {
                order: 4 !important;
                justify-content: center !important;
                flex-direction: column !important;
                gap: 10px !important;
            }

            .hero-buttons a {
                padding: 14px 20px !important;
                font-size: 1rem !important;
                width: 100% !important;
                justify-content: center !important;
            }

            /* Standardize section spacing on mobile */
            section {
                padding-top: 35px !important;
                padding-bottom: 35px !important;
            }

            .hero-section {
                padding-top: 0 !important;
            }

            /* Smaller section subheadings on mobile */
            .section-header {
                margin-bottom: 20px !important;
            }

            .section-header h2 {
                margin-bottom: 8px !important;
            }

            .section-header p {
                font-size: 0.9rem !important;
                line-height: 1.4 !important;
            }

            /* FAQ section */
            .faq-preview { padding: 25px 0 35px !important; }
            .faq-item summary h3 { font-size: 0.9rem !important; }
            .faq-answer { font-size: 0.85rem !important; }

            .bantuan-content {
                grid-template-columns: 1fr !important;
            }
            .bantuan-product img {
                max-width: 250px !important;
            }

            /* Why-us section - 2x3 grid on mobile */
            .why-us-grid {
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 12px !important;
            }

            .why-us-item {
                padding: 15px !important;
                text-align: center !important;
            }

            .why-us-item .icon-circle {
                width: 40px !important;
                height: 40px !important;
                margin-bottom: 6px !important;
            }

            .why-us-item .icon-circle svg {
                width: 20px !important;
                height: 20px !important;
            }

            .why-us-item h3 {
                font-size: 0.85rem !important;
                margin-bottom: 4px !important;
            }

            .why-us-item p {
                font-size: 0.7rem !important;
                line-height: 1.3 !important;
            }

            /* Kelebihan section - single column on mobile */
            .kelebihan-grid {
                display: flex !important;
                flex-direction: column !important;
                grid-template-columns: unset !important;
                gap: 8px !important;
            }

            .kelebihan-grid > div {
                padding: 12px !important;
                gap: 10px !important;
                min-height: 80px !important;
                align-items: center !important;
            }

            .kelebihan-grid > div > div:first-child {
                width: 40px !important;
                height: 40px !important;
                min-width: 40px !important;
            }

            .kelebihan-grid > div > div:first-child svg {
                width: 20px !important;
                height: 20px !important;
            }

            .kelebihan-grid h4 {
                font-size: 0.9rem !important;
                margin-bottom: 2px !important;
            }

            .kelebihan-grid p {
                font-size: 0.8rem !important;
                line-height: 1.3 !important;
            }

            /* Hide "Siapa Yang Perlukan" on mobile */
            .who-needs-container {
                display: none !important;
            }

            /* Proof gallery - 3x4 grid on mobile */
            .proof-gallery-grid {
                grid-template-columns: repeat(3, 1fr) !important;
                gap: 8px !important;
            }

            .proof-gallery-grid img {
                height: 90px !important;
            }

            /* Location cards */
            section [style*="grid-template-columns: repeat(4"] {
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 8px !important;
            }
            section [style*="grid-template-columns: repeat(4"] a {
                padding: 12px 8px !important;
                border-radius: 8px !important;
            }
            section [style*="grid-template-columns: repeat(4"] span {
                font-size: 0.8rem !important;
            }

            /* Footer - simple 2 column, NO overlap */
            .footer {
                padding: 1rem 15px 0.8rem !important;
            }

            .footer .container {
                padding: 0 !important;
            }

            .footer-links {
                display: none !important;
            }

            .footer-grid {
                display: grid !important;
                grid-template-columns: 1fr 1fr !important;
                gap: 8px 12px !important;
                margin-bottom: 0.8rem !important;
            }

            .footer-about {
                text-align: left !important;
            }

            .footer-about > a {
                display: none !important;
            }

            .footer-about > p {
                font-size: 0.55rem !important;
                line-height: 1.35 !important;
                margin: 0 0 6px 0 !important;
            }

            .footer-social {
                display: none !important;
            }

            .footer-contact {
                text-align: right !important;
            }

            .footer-contact h3 {
                display: none !important;
            }

            .footer-contact p {
                font-size: 0.55rem !important;
                line-height: 1.35 !important;
                margin: 0 0 6px 0 !important;
            }

            .footer-contact p a {
                font-size: 0.65rem !important;
            }

            .footer-bottom {
                text-align: center !important;
                padding-top: 0.6rem !important;
                border-top: 1px solid rgba(255,255,255,0.2) !important;
            }

            .footer-bottom p {
                font-size: 0.5rem !important;
            }

            .footer-legal {
                justify-content: center !important;
                gap: 6px !important;
                margin-top: 4px !important;
            }

            .footer-legal li a {
                font-size: 0.45rem !important;
            }
        }
    </style>
</head>'''

# FAQ inline styles to add
FAQ_STYLES = '''                <style>
                    .faq-item summary { display: flex; align-items: center; justify-content: space-between; }
                    .faq-item summary::after { content: '+'; display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: #1e4a9e; color: white; border-radius: 50%; font-size: 1.2rem; font-weight: bold; flex-shrink: 0; margin-left: 16px; }
                    .faq-item[open] summary::after { content: '−'; }
                    .faq-item summary h3 { margin: 0; flex: 1; }
                </style>'''

def update_location_file(filepath):
    """Update a location file with new mobile styles and FAQ format"""

    # Skip only selangor.html (not kuala-selangor.html) as it's the reference
    if filepath.endswith('selangor.html') and 'kuala-selangor' not in filepath:
        print(f"Skipping {filepath} (reference file)")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Replace or add mobile styles before </head>
        # First, try to remove any existing mobile styles
        # Pattern to match existing mobile styles block
        mobile_pattern = r'<!--\s*Mobile Styles\s*-->.*?</style>\s*</head>'
        if re.search(mobile_pattern, content, re.DOTALL):
            content = re.sub(mobile_pattern, MOBILE_STYLES, content, flags=re.DOTALL)
        else:
            # No mobile styles found, add before </head>
            content = content.replace('</head>', MOBILE_STYLES)

        # 2. Update FAQ section class from faq-section to faq-preview
        content = re.sub(
            r'class="faq-section"',
            'class="faq-preview" aria-labelledby="faq-heading"',
            content
        )

        # 3. Remove faq-question class from summary
        content = re.sub(
            r'<summary class="faq-question">',
            '<summary>',
            content
        )

        # 4. Add FAQ styles if faq-accordion exists and styles not present
        if 'faq-accordion' in content and '.faq-item summary::after' not in content:
            content = re.sub(
                r'(<div class="faq-accordion"[^>]*>)',
                FAQ_STYLES + '\n                \\1',
                content
            )

        # 5. Update FAQ section style to match main page
        content = re.sub(
            r'<section id="faq" class="faq-preview"[^>]*style="[^"]*"[^>]*>',
            '<section id="faq" class="faq-preview" aria-labelledby="faq-heading" style="padding-top: 30px;">',
            content
        )

        # Also handle case where there's no style attribute
        content = re.sub(
            r'<section id="faq" class="faq-preview" aria-labelledby="faq-heading">(?!\s*<)',
            '<section id="faq" class="faq-preview" aria-labelledby="faq-heading" style="padding-top: 30px;">',
            content
        )

        # 6. Add id to FAQ h2 if not present
        if 'id="faq-heading"' not in content and '<section id="faq"' in content:
            # Find the h2 in the FAQ section and add id
            content = re.sub(
                r'(<section id="faq"[^>]*>.*?<h2)(?!\s+id=)',
                r'\1 id="faq-heading"',
                content,
                flags=re.DOTALL
            )

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        else:
            print(f"No changes needed: {filepath}")
            return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Get all location HTML files
    locations_dir = os.path.dirname(os.path.abspath(__file__))
    location_files = glob.glob(os.path.join(locations_dir, 'locations', '*.html'))

    print(f"Found {len(location_files)} location files")

    updated_count = 0
    for filepath in location_files:
        if update_location_file(filepath):
            updated_count += 1

    print(f"\nTotal files updated: {updated_count}")

if __name__ == '__main__':
    main()
