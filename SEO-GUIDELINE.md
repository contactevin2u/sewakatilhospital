# SEO Guideline - SewaKatilHospital.my

**Business:** AA Alive Sdn Bhd (1204108-D)
**Website:** https://renthospitalbed.my
**Founded:** 2016
**Last Updated:** January 2026

---

## 1. Target Keywords

### Primary Keywords (High Priority)
| Keyword | Search Intent | Target Page |
|---------|---------------|-------------|
| sewa katil hospital | Transactional | Homepage, /rental/ |
| katil hospital malaysia | Informational | Homepage |
| hospital bed rental malaysia | Transactional | Homepage, /rental/ |
| beli katil hospital | Transactional | /purchase/ |
| katil hospital 2 fungsi | Product | /products/katil-hospital-2-fungsi/ |
| katil hospital 3 fungsi | Product | /products/katil-hospital-3-fungsi/ |

### Secondary Keywords
| Keyword | Target Page |
|---------|-------------|
| sewa katil pesakit | Homepage |
| katil hospital untuk rumah | Homepage |
| harga sewa katil hospital | /rental/, FAQ |
| katil hospital murah | /purchase/ |
| katil hospital elektrik | Product pages |
| katil hospital manual | Product pages |

### Long-tail Keywords
- sewa katil hospital [lokasi] (e.g., "sewa katil hospital KL")
- katil hospital 2 fungsi vs 3 fungsi
- cara jaga pesakit bedridden di rumah
- berapa harga sewa katil hospital sebulan
- katil hospital untuk orang tua

### Location Keywords (139 locations)
- sewa katil hospital Kuala Lumpur
- sewa katil hospital Johor Bahru
- sewa katil hospital Penang
- (All 139 location pages target local keywords)

---

## 2. On-Page SEO Checklist

### Title Tag
- [ ] Length: 50-60 characters
- [ ] Include primary keyword
- [ ] Include brand or location
- [ ] Add year for freshness (2026)
- [ ] Format: `Primary Keyword | Secondary Info (Year)`

**Template:**
```
Sewa Katil Hospital [Lokasi] | RM150/Bulan, Penghantaran 4 Jam (2026)
```

### Meta Description
- [ ] Length: 150-160 characters (MAX)
- [ ] Include primary keyword
- [ ] Include call-to-action
- [ ] Include unique selling points (price, no deposit, fast delivery)

**Template:**
```
Sewa katil hospital dari RM150/bulan. Tanpa deposit, penghantaran 4 jam, servis percuma. [Location/specific benefit].
```

### Headings
- [ ] Exactly ONE H1 per page
- [ ] H1 contains main keyword
- [ ] Proper hierarchy: H1 → H2 → H3 (no skipping)
- [ ] H2 for main sections
- [ ] H3 for subsections

### Images
- [ ] All images have descriptive alt text
- [ ] Alt text includes keywords naturally
- [ ] Use WebP format for performance
- [ ] Compress images (< 100KB ideal)
- [ ] Use lazy loading for below-fold images

**Alt Text Examples:**
```
Good: "Katil hospital 2 fungsi manual untuk kegunaan rumah"
Bad: "image1" or "katil" or ""
```

### Internal Linking
- [ ] Link to related products from blog posts
- [ ] Link to blog posts from product pages
- [ ] Use descriptive anchor text (not "click here")
- [ ] Link to location pages where relevant

---

## 3. Content Guidelines

### Blog Posts
- Minimum 800 words for comprehensive coverage
- Include FAQ section with schema markup
- Add table of contents for long articles
- Use comparison tables where applicable
- Include internal links to products/services
- Add clear CTAs (WhatsApp, contact)

### Product Pages
- Detailed product specifications
- Pricing information (rental & purchase)
- High-quality images with alt text
- Customer benefits (not just features)
- FAQ section
- Related products section
- Clear CTA buttons

### Location Pages
- Unique content per location (not duplicate)
- Local landmarks/hospital references
- Specific delivery information
- Local phone number
- Google Maps embed
- Service area coverage

---

## 4. Schema Markup Reference

### Organization Schema (All Pages)
```json
{
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "SewaKatilHospital.my",
    "legalName": "AA Alive Sdn Bhd",
    "url": "https://renthospitalbed.my",
    "telephone": "+601128322492",
    "foundingDate": "2016",
    "sameAs": [
        "https://www.facebook.com/sewakatilhospital",
        "https://www.instagram.com/sewakatilhospital"
    ]
}
```

### LocalBusiness Schema (Location Pages)
```json
{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Sewa Katil Hospital [Location]",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "[City]",
        "addressRegion": "[State]",
        "addressCountry": "MY"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": "[CORRECT LAT]",
        "longitude": "[CORRECT LNG]"
    }
}
```

### Product Schema
```json
{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Katil Hospital [Type]",
    "offers": {
        "@type": "Offer",
        "price": "[PRICE]",
        "priceCurrency": "MYR"
    }
}
```

### FAQ Schema
```json
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "Question here?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Answer here."
            }
        }
    ]
}
```

### Article Schema (Blog Posts)
```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article Title",
    "datePublished": "2026-01-19",
    "author": {
        "@type": "Organization",
        "name": "SewaKatilHospital.my"
    }
}
```

---

## 5. Technical SEO

### Page Speed
- Use minified CSS/JS
- Enable GZIP compression
- Use CDN for static assets
- Lazy load images
- Preconnect to external domains

### Mobile Optimization
- Responsive design (all pages)
- Touch-friendly buttons (min 44px)
- Readable font sizes (min 16px)
- No horizontal scrolling

### Indexing
- Submit sitemap to Google Search Console
- Use canonical URLs on all pages
- No duplicate content
- Proper robots.txt configuration

### URL Structure
```
Homepage: /
Products: /products/[product-name]/
Rental: /rental/
Purchase: /purchase/
Blog: /blog/[post-slug]/
Locations: /locations/[location-name]/
```

---

## 6. Link Building Strategy

### Internal Links
| From | To | Anchor Text |
|------|-----|-------------|
| Blog posts | Product pages | "katil hospital 2 fungsi" |
| Product pages | Related blog | "baca panduan lengkap" |
| Location pages | Main rental page | "lihat harga sewa" |
| All pages | WhatsApp | "Hubungi sekarang" |

### External Links (Earn)
- Local business directories
- Healthcare blogs
- Medical equipment reviews
- Local news features

---

## 7. Content Calendar Ideas

### Blog Topics
1. Cara pilih katil hospital yang sesuai
2. Tips jaga pesakit stroke di rumah
3. Perbezaan katil manual vs elektrik
4. Checklist peralatan untuk home care
5. Kos penjagaan pesakit di rumah vs hospital
6. Bila masa sesuai sewa vs beli katil hospital
7. Cara setup bilik pesakit di rumah
8. Panduan untuk first-time caregiver

---

## 8. Monitoring & KPIs

### Track Monthly
- [ ] Organic traffic (Google Analytics)
- [ ] Keyword rankings (target top 10)
- [ ] Page load speed (< 3 seconds)
- [ ] Core Web Vitals (Google Search Console)
- [ ] Conversion rate (WhatsApp clicks)
- [ ] Bounce rate (< 60%)

### Tools
- Google Analytics: G-RQRSF7CCBH
- Google Search Console: Connected
- PageSpeed Insights: Check monthly

---

## 9. Do's and Don'ts

### DO
- Use "katil hospital" consistently (not "hospital bed" in Malay content)
- Include prices in content (RM150/bulan, RM799)
- Add year to titles for freshness
- Update content regularly
- Respond to reviews

### DON'T
- Use oxygen-related keywords (old business)
- Duplicate content across pages
- Stuff keywords unnaturally
- Use generic alt text
- Ignore mobile users

---

## 10. Brand Consistency

### Company Name
- Full: **AA Alive Sdn Bhd (1204108-D)**
- Website: **SewaKatilHospital.my**
- Domain: **renthospitalbed.my**

### Social Media
- Facebook: facebook.com/sewakatilhospital
- Instagram: instagram.com/sewakatilhospital

### Contact
- Phone: 011-2832 2492
- WhatsApp: wa.me/601128322492
- Email: contact@evin2u.com

### Founding Year
- Always use: **2016** (not 2014, 2019, or other dates)

### Certifications
- SSM Registered
- KKM Approved
- MDA Registered

---

## Quick Reference Card

```
Title: 50-60 chars | Include keyword + year
Meta: 150-160 chars | Include CTA + USP
H1: Exactly 1 per page | Include main keyword
Images: Always alt text | WebP format
Schema: Organization + Page-specific
Founding: 2016
Social: @sewakatilhospital
Phone: 011-2832 2492
```

---

*This guideline should be reviewed and updated quarterly.*
