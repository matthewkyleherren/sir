# AGENTS.md

Guidelines for AI coding agents working in this repository.

## Project Overview

Static website for "Sir Beer" (craft Swiss brewery) migrated from Webflow. No build process, no package manager, no TypeScript. All assets are self-hosted in `external/`.

**Stack:**
- HTML (Webflow-generated)
- CSS (Webflow minified)
- JavaScript (jQuery, GSAP, Lenis, Finsweet)
- Python (utility scripts)
- Stripe (e-commerce integration)

## Commands

### Local Development
```bash
# Start local server (pick one)
python3 -m http.server 8000
php -S localhost:8000
npx http-server -p 8000
```

### Image Utilities
```bash
# Extract WebP from base64 data URI
python3 extract_webp.py <input_file> [output_file]

# Convert WebP to JPG (requires: pip install Pillow)
python3 convert_to_jpg.py <input_file> [output_file]
```

### Verification
```bash
# Count external assets
find external -type f | wc -l

# Check for broken CDN references
grep -r "cdn.prod.website-files.com" . --include="*.html"

# Verify directory structure
ls -la external/css external/js external/images external/json
```

### No Build/Lint/Test
This project has **no automated testing, linting, or build process**. Changes are verified manually by running the local server and inspecting pages.

## File Structure

```
sir/
├── index.html                    # Homepage (with Stripe cart)
├── checkout/index.html           # Checkout (with Stripe payments)
├── about/index.html              # About page
├── contact/index.html            # Contact page
├── game/index.html               # Interactive game
├── recipes/index.html            # Recipe gallery
├── privacy-policy/index.html     # Privacy policy
├── sales-policy/index.html       # Sales policy
├── terms-of-use/index.html       # Terms of use
├── external/                     # All self-hosted assets
│   ├── css/                      # Webflow stylesheet (1 file)
│   ├── js/                       # JavaScript (44 files)
│   ├── images/                   # Images & icons (60+ files)
│   └── json/                     # Lottie animations
├── convert_to_jpg.py             # Image conversion utility
└── extract_webp.py               # WebP extraction utility
```

## Code Style Guidelines

### HTML

- Webflow-generated markup - maintain indentation consistency
- Use 4-space indentation
- Preserve Webflow data attributes:
  - `data-wf-domain` - Domain configuration
  - `data-wf-page` - Page identifier
  - `data-wf-site` - Site identifier
  - `data-w-id` - Element IDs for interactions
- Do NOT modify Webflow data attributes without understanding runtime requirements

**Path Patterns:**
```html
<!-- Root-level pages (index.html) -->
<link href="external/css/..." rel="stylesheet">
<script src="external/js/..." type="text/javascript"></script>

<!-- Subdirectory pages (about/, checkout/, etc.) -->
<link href="../external/css/..." rel="stylesheet">
<script src="../external/js/..." type="text/javascript"></script>
```

### CSS

- Main stylesheet: `external/css/hungry-tiger.webflow.shared.bb04e25ad.min.css`
- Inline styles in HTML for page-specific overrides
- Selection color: `#e0005c`
- Scrollbars are hidden via webkit pseudo-elements

### JavaScript

Libraries loaded on all pages:
- `jquery-3.5.1.min.js` - jQuery core
- `gsap.min.js` + `ScrollTrigger.min.js` - Animations
- `lenis.js` - Smooth scrolling
- `split-type.min.js` - Text splitting
- `finsweet-*.js` - Webflow enhancements
- `webflow.*.js` - Webflow runtime

**Chunk Loading:** Site uses dynamic imports. 22 Webflow chunks + 12 Finsweet chunks are lazy-loaded.

**Stripe:** Only loaded on `index.html` and `checkout/index.html`. Do not add Stripe to other pages.

### Python

```python
#!/usr/bin/env python3
"""
Module docstring describing purpose
"""

import stdlib_modules
import third_party_modules

def function_name(input_file, output_file=None):
    """
    Function docstring with description of parameters and return value.
    """
    # Implementation
    pass

if __name__ == "__main__":
    # Entry point with argument parsing
    pass
```

**Conventions:**
- Use `pathlib.Path` for file operations
- Include docstrings for modules and functions
- Use snake_case for functions and variables
- Handle errors with try/except, print user-friendly messages
- Return boolean for success/failure in utility functions

## Critical Warnings

### Do NOT

- Remove or modify Webflow `data-*` attributes
- Add CDN dependencies (all assets must be self-hosted)
- Use type error suppressions in any generated JS
- Add Stripe scripts to pages other than index/checkout
- Create broken relative paths (test with local server)

### Expected Behaviors

- **CSP warnings on homepage/checkout**: These come from Stripe's iframe and cannot be eliminated. They are expected and do not affect functionality.

- **Chunk 404 errors**: Verify all chunk files exist in `external/js/` and `external/js/dist/`.

### Stripe Configuration

```
Live key: pk_live_nyPnaDuxaj8zDxRbuaPHJjip
Account: acct_1RWScUKKBYfwpHY1
Script: https://js.stripe.com/v3/
```

Only modify Stripe integration if you understand the full e-commerce flow.

## Deployment Notes

1. **Preserve directory structure** - Relative paths are critical
2. **Upload complete `external/` directory** - All 106 files required
3. **Configure MIME types:**
   - `.js` → `application/javascript`
   - `.avif` → `image/avif`
   - `.json` → `application/json`
4. **Test all pages** after deployment

## Image Formats Used

| Format | Usage |
|--------|-------|
| AVIF | Photos and graphics |
| PNG | Icons, logos, UI elements |
| SVG | Vector logos and icons |
| Lottie JSON | Animated illustrations |

## When Editing This Project

1. **Start local server** before making changes
2. **Test in browser** after each significant change
3. **Verify relative paths** work from subdirectories
4. **Check console** for JavaScript errors
5. **Maintain self-hosting** - don't add external CDN dependencies

## Related Documentation

- `WARP.md` - Detailed project architecture
- `CHUNKS_FIXED_REPORT.md` - Chunk file troubleshooting
- `CSP_ERRORS_FIXED.md` - CSP warning explanation
- `COMPLETE_MIGRATION_REPORT.md` - CDN migration history
