# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a static website for "Sir Beer" (craft Swiss brewery) and "Hungry Tiger" (sauce products), originally built in Webflow and migrated to self-hosted static files. The site has been fully localized from CDN dependencies to local files stored in the `external/` directory.

**Key characteristics:**
- Static HTML site with no build process
- Webflow-generated markup and styling
- All assets (CSS, JS, images) are self-contained in `external/`
- Uses Webflow's e-commerce functionality with Stripe integration
- Dynamic code-splitting with chunk files for lazy loading

## Common Commands

### Development
```bash
# Serve the site locally (requires a local web server)
python3 -m http.server 8000

# Alternative with PHP
php -S localhost:8000

# Alternative with Node.js http-server
npx http-server -p 8000
```

### Image Utilities
```bash
# Extract WebP images from base64 data
python3 extract_webp.py <input_file> [output_file]

# Convert WebP to JPG (requires Pillow)
python3 convert_to_jpg.py <input_file> [output_file]
```

### Asset Management
```bash
# Check for missing external resources
grep -r "cdn.prod.website-files.com" . --include="*.html"
grep -r "cdn.jsdelivr.net" . --include="*.html"

# Verify external directory structure
ls -la external/css external/js external/images external/json

# Count total files in external directory
find external -type f | wc -l
```

## Architecture

### File Structure
```
sir/
├── index.html                    # Homepage with shopping cart + Stripe
├── checkout/index.html           # Checkout page with Stripe
├── about/index.html              # About page
├── contact/index.html            # Contact page
├── game/index.html               # Interactive game
├── recipes/index.html            # Recipe gallery
├── privacy-policy/index.html     # Privacy policy
├── sales-policy/index.html       # Sales policy
├── terms-of-use/index.html       # Terms of use
├── external/                     # All self-hosted assets (37 MB)
│   ├── css/                      # Main stylesheet (1 file)
│   ├── js/                       # JavaScript files (44 files)
│   │   ├── Main libraries (10)
│   │   ├── webflow.achunk.*.js (22 chunks)
│   │   └── dist/chunk-*.js (12 Finsweet chunks)
│   ├── images/                   # Images and icons (60 files)
│   └── json/                     # Lottie animations (1 file)
└── [utility scripts]             # Python image conversion tools
```

### JavaScript Architecture

**Main Libraries (loaded on all pages):**
- `jquery-3.5.1.min.js` - jQuery core
- `gsap.min.js` - Animation library
- `ScrollTrigger.min.js` - GSAP scroll-based animations
- `lenis.js` - Smooth scrolling library
- `split-type.min.js` - Text splitting for animations
- `finsweet-attributes.js` - Finsweet attribute library
- `finsweet-selectcustom.js` - Custom select functionality
- `webflow.*.js` (3 versions) - Webflow runtime

**Code Splitting:**
The site uses dynamic imports for lazy-loading features:
- **22 Webflow chunks** (`webflow.achunk.*.js`) - Different Webflow features (interactions, animations, e-commerce modules)
- **12 Finsweet chunks** (`dist/chunk-*.js`) - Finsweet attribute modules (forms, modals, accordions, etc.)

These chunks are loaded on-demand when specific features are needed, reducing initial page load time.

### Stripe Integration

Stripe is only loaded on pages that require payment functionality:
- **index.html** - Shopping cart functionality
- **checkout/index.html** - Payment processing

All other pages have Stripe removed for better performance and cleaner console output.

**Stripe Configuration:**
- Live key: `pk_live_nyPnaDuxaj8zDxRbuaPHJjip`
- Account: `acct_1RWScUKKBYfwpHY1`
- Script source: `https://js.stripe.com/v3/`

### CSS Architecture

Single minified stylesheet contains all Webflow-generated styles:
- `external/css/hungry-tiger.webflow.shared.bb04e25ad.min.css` (121 KB)

Custom inline styles in each HTML file handle:
- Scrollbar styling (invisible scrollbars)
- Platform-specific text adjustments (Mac vs Windows)
- Custom selection color (`#e0005c`)
- Page-specific pointer-event overrides

### Image Formats

The site uses multiple image formats:
- **AVIF** - Modern format for photos and graphics
- **PNG** - Icons, logos, and UI elements
- **SVG** - Vector logos and icons
- **Lottie JSON** - Animated jar illustration (15 MB)

## Important Notes

### CDN Migration
This site was migrated from external CDN dependencies to self-hosted files. All 106 external resources (CSS, JS, images, JSON) are now stored locally in the `external/` directory.

**Original CDN sources (now removed):**
- `cdn.prod.website-files.com`
- `cdn.jsdelivr.net`
- `cdnjs.cloudflare.com`
- `d3e54v103j8qbb.cloudfront.net`
- `unpkg.com`

### Content Security Policy (CSP) Warnings
If you see CSP errors on the homepage or checkout page, this is **expected behavior**:
- They originate from Stripe's iframe, not the site code
- They are security audit logs from Stripe's own CSP headers
- They do not affect functionality
- They cannot be eliminated (Stripe controls them)

See `CSP_ERRORS_FIXED.md` for detailed explanation.

### Chunk Files
If you encounter 404 errors for JavaScript chunks, verify that all chunk files are present:
- 22 Webflow chunks in `external/js/`
- 12 Finsweet chunks in `external/js/dist/`

See `CHUNKS_FIXED_REPORT.md` for details.

### Path Structure
HTML files in subdirectories use relative paths with `../` to reference external assets:
```html
<link href="../external/css/..." rel="stylesheet">
<script src="../external/js/..." type="text/javascript"></script>
```

Root-level `index.html` uses direct paths without `../`:
```html
<link href="external/css/..." rel="stylesheet">
```

### Webflow Attributes
Pages use Webflow's data attributes extensively:
- `data-wf-domain` - Domain configuration
- `data-wf-page` - Page identifier
- `data-wf-site` - Site identifier
- `data-w-id` - Element IDs for interactions

Do not modify these attributes without understanding Webflow's runtime requirements.

## Deployment Considerations

When deploying this site:

1. **Preserve directory structure** - Relative paths depend on exact directory layout
2. **Upload complete `external/` directory** - All 106 files (37 MB) are required
3. **Configure MIME types** - Ensure server can serve:
   - `.js` files as `application/javascript`
   - `.avif` files as `image/avif`
   - `.json` files as `application/json`
4. **Test all pages** - Verify chunk loading works correctly
5. **Test e-commerce flow** - Complete a test purchase on staging first

## Brand Context

The site references two product lines:
- **Sir Beer** - Swiss craft brewery (Aargau region), branding appears in meta tags
- **Hungry Tiger** - Sauce products, main site content and branding

Navigation includes sections for beer/sauce, about, recipes, game, and contact.
