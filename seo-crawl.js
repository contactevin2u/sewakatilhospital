/**
 * SEO Technical Audit Crawler for renthospitalbed.my
 * Full-featured CLI SEO crawler with link discovery and broken link detection
 *
 * Usage:
 *   node seo-crawl.js                   Crawl all sitemap URLs + discovered links
 *   node seo-crawl.js --quick            Crawl first 20 URLs only
 *   node seo-crawl.js --url <url>        Crawl single URL
 *   node seo-crawl.js --csv              Export CSV report
 *   node seo-crawl.js --no-discover      Skip link discovery (sitemap only)
 *   node seo-crawl.js --summary          Show summary only (no warnings list)
 *
 * Features:
 * - HTTP status codes (2xx, 3xx, 4xx, 5xx)
 * - Title tag analysis (missing, too long/short, duplicates)
 * - Meta description analysis (missing, too long/short, duplicates)
 * - H1 tag detection (handles inner HTML like <br/>, <span>)
 * - Multiple H1 detection
 * - Heading hierarchy check (H2, H3 structure)
 * - robots.txt parsing and enforcement
 * - noindex directives (meta robots + X-Robots-Tag header)
 * - Canonical tag validation
 * - Broken internal link detection
 * - Link discovery (finds pages not in sitemap)
 * - Image alt text audit
 * - Open Graph tag check
 * - Word count / thin content detection
 * - Response time monitoring
 * - Internal link count per page
 * - Duplicate title/description detection
 * - CSV export
 * - JSON report export
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const BASE_URL = 'https://renthospitalbed.my';
const SITEMAP_PATH = path.join(__dirname, 'sitemap.xml');
const CONCURRENCY = 5;
const TIMEOUT_MS = 15000;

// --- URL Extraction from sitemap.xml ---

function getAllUrls() {
  if (!fs.existsSync(SITEMAP_PATH)) {
    console.error('ERROR: sitemap.xml not found');
    process.exit(1);
  }

  const xml = fs.readFileSync(SITEMAP_PATH, 'utf-8');
  const urls = [];
  const locMatches = xml.matchAll(/<loc>\s*(https?:\/\/[^<\s]+)\s*<\/loc>/gi);

  for (const match of locMatches) {
    urls.push(match[1].trim());
  }

  return urls;
}

// --- robots.txt Parser ---

function parseRobotsTxt(robotsTxt) {
  const rules = { allow: [], disallow: [] };
  let inUserAgentAll = false;

  for (const line of robotsTxt.split('\n')) {
    const trimmed = line.trim();
    if (trimmed.startsWith('#') || trimmed === '') continue;

    const [directive, ...valueParts] = trimmed.split(':');
    const value = valueParts.join(':').trim();

    if (directive.toLowerCase() === 'user-agent') {
      inUserAgentAll = (value === '*');
    } else if (inUserAgentAll) {
      if (directive.toLowerCase() === 'disallow' && value) {
        rules.disallow.push(value);
      } else if (directive.toLowerCase() === 'allow' && value) {
        rules.allow.push(value);
      }
    }
  }

  return rules;
}

function isBlockedByRobots(urlPath, rules) {
  for (const pattern of rules.allow) {
    if (urlPath.startsWith(pattern)) return false;
  }
  for (const pattern of rules.disallow) {
    if (urlPath.startsWith(pattern)) return true;
  }
  return false;
}

async function fetchRobotsTxt(baseUrl) {
  try {
    const result = await fetchUrl(`${baseUrl}/robots.txt`);
    if (result.statusCode === 200) {
      return parseRobotsTxt(result.body);
    }
  } catch (e) { /* ignore */ }
  return { allow: [], disallow: [] };
}

// --- HTTP Fetch ---

function fetchUrl(url) {
  return new Promise((resolve) => {
    const start = Date.now();
    const client = url.startsWith('https') ? https : http;

    const req = client.get(url, { timeout: TIMEOUT_MS, headers: { 'User-Agent': 'SEO-Crawler/1.0' } }, (res) => {
      let body = '';
      const headers = res.headers;

      res.on('data', chunk => { body += chunk; });
      res.on('end', () => {
        resolve({
          url,
          statusCode: res.statusCode,
          headers,
          body,
          responseTime: Date.now() - start,
          redirectUrl: headers.location || null,
        });
      });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({ url, statusCode: 0, headers: {}, body: '', responseTime: TIMEOUT_MS, error: 'TIMEOUT' });
    });

    req.on('error', (err) => {
      resolve({ url, statusCode: 0, headers: {}, body: '', responseTime: Date.now() - start, error: err.message });
    });
  });
}

// --- Link Extraction ---

function extractInternalLinks(body, pageUrl) {
  const links = new Set();
  const baseUrlObj = new URL(BASE_URL);

  const hrefMatches = body.matchAll(/href=["']([^"'#]+?)["']/gi);
  for (const match of hrefMatches) {
    let href = match[1].trim();

    if (/\.(css|js|png|jpg|jpeg|gif|svg|webp|ico|woff2?|ttf|eot|pdf|zip|xml)$/i.test(href)) continue;
    if (href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) continue;

    try {
      let fullUrl;
      if (href.startsWith('http://') || href.startsWith('https://')) {
        fullUrl = new URL(href);
      } else if (href.startsWith('/')) {
        fullUrl = new URL(href, BASE_URL);
      } else {
        fullUrl = new URL(href, pageUrl);
      }

      if (fullUrl.hostname === baseUrlObj.hostname) {
        let normalized = fullUrl.origin + fullUrl.pathname;
        if (normalized.endsWith('/') && normalized !== BASE_URL + '/') {
          normalized = normalized.slice(0, -1);
        }
        links.add(normalized);
      }
    } catch (e) { /* invalid URL, skip */ }
  }

  return [...links];
}

// --- Image Alt Text Extraction ---

function extractImages(body) {
  const images = [];
  const imgMatches = body.matchAll(/<img\s[^>]*?(?:>|\/?>)/gi);
  for (const match of imgMatches) {
    const tag = match[0];
    const src = tag.match(/src=["']([^"']+)["']/i);
    const alt = tag.match(/alt=["']([^"']*)["']/i);
    if (src) {
      images.push({
        src: src[1],
        alt: alt ? alt[1] : null,
        hasAlt: alt !== null,
      });
    }
  }
  return images;
}

// --- HTML Analysis ---

function analyzePage(result, robotsRules) {
  const { url, statusCode, headers, body, responseTime, redirectUrl, error } = result;
  const issues = [];
  const info = { url, statusCode, responseTime };

  if (error) {
    issues.push({ severity: 'critical', issue: `Connection error: ${error}` });
    return { ...info, issues, title: null, description: null, h1: null, wordCount: 0, canonical: null, internalLinksFound: [], images: [] };
  }

  // robots.txt check
  try {
    const urlPath = new URL(url).pathname;
    if (robotsRules && isBlockedByRobots(urlPath, robotsRules)) {
      issues.push({ severity: 'critical', issue: `Blocked by robots.txt (path: ${urlPath})` });
    }
  } catch (e) { /* ignore */ }

  // Status code
  if (statusCode >= 500) issues.push({ severity: 'critical', issue: `Server error (${statusCode})` });
  else if (statusCode === 404) issues.push({ severity: 'critical', issue: 'Page not found (404)' });
  else if (statusCode >= 300 && statusCode < 400) {
    issues.push({ severity: 'warning', issue: `Redirect (${statusCode}) -> ${redirectUrl}` });
    return { ...info, issues, title: null, description: null, h1: null, wordCount: 0, canonical: redirectUrl, internalLinksFound: [], images: [] };
  }

  // Title
  const titleMatch = body.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1].replace(/<[^>]+>/g, '').trim() : null;
  info.title = title;
  if (!title) issues.push({ severity: 'critical', issue: 'Missing <title> tag' });
  else if (title.length > 60) issues.push({ severity: 'warning', issue: `Title too long (${title.length} chars, max 60)` });
  else if (title.length < 20) issues.push({ severity: 'warning', issue: `Title too short (${title.length} chars)` });

  // Meta description
  const descMatch = body.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i)
    || body.match(/<meta\s+content=["']([^"']+)["']\s+name=["']description["']/i);
  const description = descMatch ? descMatch[1].trim() : null;
  info.description = description;
  if (!description) issues.push({ severity: 'critical', issue: 'Missing meta description' });
  else if (description.length > 160) issues.push({ severity: 'warning', issue: `Meta description too long (${description.length} chars, max 160)` });
  else if (description.length < 50) issues.push({ severity: 'warning', issue: `Meta description too short (${description.length} chars)` });

  // Noindex check
  const robotsMeta = body.match(/<meta\s+name=["']robots["']\s+content=["']([^"']+)["']/i)
    || body.match(/<meta\s+content=["']([^"']+)["']\s+name=["']robots["']/i);
  if (robotsMeta && robotsMeta[1].toLowerCase().includes('noindex')) {
    issues.push({ severity: 'critical', issue: 'Page has noindex directive in meta robots' });
  }
  const xRobotsTag = headers['x-robots-tag'];
  if (xRobotsTag && xRobotsTag.toLowerCase().includes('noindex')) {
    issues.push({ severity: 'critical', issue: 'Page has noindex in X-Robots-Tag header' });
  }

  // Canonical
  const canonicalMatch = body.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i)
    || body.match(/<link\s+href=["']([^"']+)["']\s+rel=["']canonical["']/i);
  const canonical = canonicalMatch ? canonicalMatch[1] : null;
  info.canonical = canonical;
  if (!canonical) {
    issues.push({ severity: 'warning', issue: 'Missing canonical tag' });
  } else if (canonical !== url && canonical !== url + '/') {
    issues.push({ severity: 'warning', issue: `Canonical points elsewhere: ${canonical}` });
  }

  // H1
  const h1Match = body.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const h1Raw = h1Match ? h1Match[1] : null;
  const h1 = h1Raw ? h1Raw.replace(/<[^>]+>/g, '').trim() : null;
  info.h1 = h1;
  if (!h1) issues.push({ severity: 'warning', issue: 'Missing H1 tag' });

  // Multiple H1s
  const h1Count = (body.match(/<h1[^>]*>/gi) || []).length;
  if (h1Count > 1) issues.push({ severity: 'warning', issue: `Multiple H1 tags (${h1Count})` });

  // Heading hierarchy
  const headings = [...body.matchAll(/<(h[1-6])[^>]*>/gi)].map(m => parseInt(m[1][1]));
  info.headingStructure = headings;
  if (headings.length > 0) {
    if (headings[0] !== 1) {
      issues.push({ severity: 'info', issue: `First heading is H${headings[0]}, expected H1` });
    }
    for (let i = 1; i < headings.length; i++) {
      if (headings[i] > headings[i - 1] + 1) {
        issues.push({ severity: 'info', issue: `Heading level skipped: H${headings[i - 1]} -> H${headings[i]}` });
        break;
      }
    }
  }

  // Word count
  const textContent = body.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const wordCount = textContent.split(/\s+/).filter(w => w.length > 1).length;
  info.wordCount = wordCount;
  if (wordCount < 100) issues.push({ severity: 'critical', issue: `Thin content (${wordCount} words, min 100)` });
  else if (wordCount < 300) issues.push({ severity: 'warning', issue: `Low word count (${wordCount} words, aim for 300+)` });

  // Response time
  if (responseTime > 5000) issues.push({ severity: 'critical', issue: `Very slow response (${responseTime}ms)` });
  else if (responseTime > 3000) issues.push({ severity: 'warning', issue: `Slow response (${responseTime}ms)` });

  // Open Graph tags
  const ogTitle = body.match(/<meta\s+property=["']og:title["']/i);
  const ogDesc = body.match(/<meta\s+property=["']og:description["']/i);
  const ogImage = body.match(/<meta\s+property=["']og:image["']/i);
  if (!ogTitle) issues.push({ severity: 'info', issue: 'Missing og:title' });
  if (!ogDesc) issues.push({ severity: 'info', issue: 'Missing og:description' });
  if (!ogImage) issues.push({ severity: 'info', issue: 'Missing og:image' });

  // Hreflang
  const hreflang = body.match(/<link[^>]*hreflang/i);
  info.hasHreflang = !!hreflang;

  // Image alt text audit
  const images = extractImages(body);
  info.images = images;
  const imagesWithoutAlt = images.filter(img => !img.hasAlt);
  if (imagesWithoutAlt.length > 0) {
    issues.push({ severity: 'warning', issue: `${imagesWithoutAlt.length} image(s) missing alt text` });
  }

  // Internal links
  const internalLinksFound = extractInternalLinks(body, url);
  info.internalLinksFound = internalLinksFound;
  info.internalLinks = internalLinksFound.length;
  if (internalLinksFound.length < 3) issues.push({ severity: 'warning', issue: `Few internal links (${internalLinksFound.length})` });

  return { ...info, issues };
}

// --- Concurrent crawler with link discovery ---

async function crawlAll(sitemapUrls, concurrency, discover = true) {
  const results = [];
  const crawled = new Set();
  const queue = [...sitemapUrls];
  const sitemapSet = new Set(sitemapUrls);
  const discoveredUrls = new Set();
  let index = 0;

  process.stdout.write('  Fetching robots.txt...\r');
  const robotsRules = await fetchRobotsTxt(BASE_URL);
  process.stdout.write('  robots.txt loaded (' + robotsRules.disallow.length + ' disallow rules)\n');

  async function worker() {
    while (true) {
      let url;
      while (index < queue.length) {
        const candidate = queue[index++];
        if (!crawled.has(candidate)) {
          url = candidate;
          break;
        }
      }
      if (!url) break;

      crawled.add(url);
      const num = crawled.size;
      process.stdout.write(`\r  Crawling ${num}/${queue.length}...`);

      const response = await fetchUrl(url);
      const analysis = analyzePage(response, robotsRules);
      analysis.fromSitemap = sitemapSet.has(url);
      results.push(analysis);

      if (discover && analysis.internalLinksFound) {
        for (const link of analysis.internalLinksFound) {
          if (!crawled.has(link) && !sitemapSet.has(link)) {
            const normalized = link.endsWith('/') && link !== BASE_URL + '/' ? link.slice(0, -1) : link;
            if (!crawled.has(normalized) && !discoveredUrls.has(normalized)) {
              discoveredUrls.add(normalized);
              queue.push(normalized);
            }
          }
        }
      }
    }
  }

  const workers = Array.from({ length: Math.min(concurrency, queue.length) }, () => worker());
  await Promise.all(workers);
  process.stdout.write('\r' + ' '.repeat(50) + '\r');

  return { results, discoveredUrls: [...discoveredUrls], robotsRules };
}

// --- Broken Link Detection ---

function findBrokenLinks(results) {
  const brokenLinks = [];
  const urlStatusMap = new Map();

  for (const page of results) {
    urlStatusMap.set(page.url, page.statusCode);
  }

  for (const page of results) {
    if (!page.internalLinksFound) continue;
    for (const link of page.internalLinksFound) {
      const status = urlStatusMap.get(link);
      if (status && (status >= 400 || status === 0)) {
        brokenLinks.push({
          sourceUrl: page.url,
          targetUrl: link,
          statusCode: status,
        });
      }
    }
  }

  return brokenLinks;
}

// --- CSV Export ---

function exportCsv(results, brokenLinks, filepath) {
  const headers = [
    'URL', 'Status', 'Title', 'Title Length', 'Description', 'Desc Length',
    'H1', 'Word Count', 'Canonical', 'Response Time (ms)',
    'Internal Links', 'Images Without Alt', 'From Sitemap', 'Issues'
  ];

  const rows = results.map(r => [
    r.url,
    r.statusCode,
    (r.title || '').replace(/"/g, '""'),
    r.title ? r.title.length : 0,
    (r.description || '').replace(/"/g, '""'),
    r.description ? r.description.length : 0,
    (r.h1 || '').replace(/"/g, '""'),
    r.wordCount || 0,
    r.canonical || '',
    r.responseTime,
    r.internalLinks || 0,
    r.images ? r.images.filter(i => !i.hasAlt).length : 0,
    r.fromSitemap ? 'Yes' : 'Discovered',
    r.issues.map(i => `[${i.severity}] ${i.issue}`).join('; '),
  ]);

  let csv = headers.map(h => `"${h}"`).join(',') + '\n';
  for (const row of rows) {
    csv += row.map(v => `"${v}"`).join(',') + '\n';
  }

  if (brokenLinks.length > 0) {
    csv += '\n"--- BROKEN LINKS ---"\n';
    csv += '"Source URL","Target URL","Status Code"\n';
    for (const bl of brokenLinks) {
      csv += `"${bl.sourceUrl}","${bl.targetUrl}","${bl.statusCode}"\n`;
    }
  }

  fs.writeFileSync(filepath, csv);
  return filepath;
}

// --- Report ---

function generateReport(results, discoveredUrls, brokenLinks, robotsRules, summaryOnly = false) {
  const critical = [];
  const warnings = [];
  const info = [];
  const titles = new Map();
  const descriptions = new Map();

  for (const page of results) {
    if (page.title) {
      if (!titles.has(page.title)) titles.set(page.title, []);
      titles.get(page.title).push(page.url);
    }
    if (page.description) {
      if (!descriptions.has(page.description)) descriptions.set(page.description, []);
      descriptions.get(page.description).push(page.url);
    }

    for (const issue of page.issues) {
      const entry = { url: page.url, ...issue };
      if (issue.severity === 'critical') critical.push(entry);
      else if (issue.severity === 'warning') warnings.push(entry);
      else info.push(entry);
    }
  }

  // Duplicate titles/descriptions
  for (const [title, urls] of titles) {
    if (urls.length > 1) {
      for (const url of urls) {
        warnings.push({ url, severity: 'warning', issue: `Duplicate title shared with ${urls.length - 1} other page(s)` });
      }
    }
  }
  for (const [desc, urls] of descriptions) {
    if (urls.length > 1) {
      for (const url of urls) {
        warnings.push({ url, severity: 'warning', issue: `Duplicate meta description shared with ${urls.length - 1} other page(s)` });
      }
    }
  }

  // Stats
  const avgResponseTime = Math.round(results.reduce((s, r) => s + r.responseTime, 0) / results.length);
  const avgWordCount = Math.round(results.reduce((s, r) => s + (r.wordCount || 0), 0) / results.length);
  const pagesWithNoindex = results.filter(r => r.issues.some(i => i.issue.includes('noindex'))).length;
  const blockedByRobots = results.filter(r => r.issues.some(i => i.issue.includes('Blocked by robots'))).length;
  const thinPages = results.filter(r => r.wordCount < 100).length;
  const slowPages = results.filter(r => r.responseTime > 3000).length;
  const missingCanonical = results.filter(r => r.issues.some(i => i.issue.includes('Missing canonical'))).length;
  const missingTitle = results.filter(r => !r.title).length;
  const missingDesc = results.filter(r => !r.description).length;
  const totalImgNoAlt = results.reduce((s, r) => s + (r.images ? r.images.filter(i => !i.hasAlt).length : 0), 0);

  console.log('\n==========================================');
  console.log('     SEO TECHNICAL AUDIT REPORT');
  console.log('     renthospitalbed.my');
  console.log('==========================================\n');

  console.log(`Pages crawled:        ${results.length}`);
  console.log(`  From sitemap:       ${results.filter(r => r.fromSitemap).length}`);
  console.log(`  Discovered:         ${discoveredUrls.length}`);
  console.log(`Avg response time:    ${avgResponseTime}ms`);
  console.log(`Avg word count:       ${avgWordCount}`);
  console.log('');
  console.log(`Critical issues:      ${critical.length}`);
  console.log(`Warnings:             ${warnings.length}`);
  console.log(`Info:                 ${info.length}`);
  console.log('');

  console.log('--- SUMMARY ---');
  console.log(`robots.txt rules:     ${robotsRules.disallow.length} disallow`);
  console.log(`Blocked by robots:    ${blockedByRobots}`);
  console.log(`Noindex pages:        ${pagesWithNoindex}`);
  console.log(`Broken links:         ${brokenLinks.length}`);
  console.log(`Thin content (<100w): ${thinPages}`);
  console.log(`Slow pages (>3s):     ${slowPages}`);
  console.log(`Missing canonical:    ${missingCanonical}`);
  console.log(`Missing title:        ${missingTitle}`);
  console.log(`Missing description:  ${missingDesc}`);
  console.log(`Images without alt:   ${totalImgNoAlt}`);
  console.log(`Duplicate titles:     ${[...titles.values()].filter(u => u.length > 1).length} groups`);
  console.log(`Duplicate descs:      ${[...descriptions.values()].filter(u => u.length > 1).length} groups`);

  if (brokenLinks.length > 0) {
    console.log('\n--- BROKEN LINKS ---');
    for (const bl of brokenLinks.slice(0, 20)) {
      console.log(`  [${bl.statusCode}] ${bl.targetUrl}`);
      console.log(`    Found on: ${bl.sourceUrl}`);
    }
    if (brokenLinks.length > 20) {
      console.log(`  ... and ${brokenLinks.length - 20} more (see JSON/CSV report)`);
    }
  }

  if (discoveredUrls.length > 0) {
    console.log('\n--- DISCOVERED URLs (not in sitemap) ---');
    for (const u of discoveredUrls.slice(0, 20)) {
      console.log(`  ${u}`);
    }
    if (discoveredUrls.length > 20) {
      console.log(`  ... and ${discoveredUrls.length - 20} more`);
    }
  }

  if (!summaryOnly) {
    if (critical.length > 0) {
      console.log('\n--- CRITICAL ISSUES ---');
      for (const c of critical) {
        console.log(`  ${c.issue}`);
        console.log(`    ${c.url}`);
      }
    }

    if (warnings.length > 0) {
      console.log('\n--- WARNINGS (first 30) ---');
      const shown = warnings.slice(0, 30);
      for (const w of shown) {
        console.log(`  ${w.issue}`);
        console.log(`    ${w.url}`);
      }
      if (warnings.length > 30) {
        console.log(`  ... and ${warnings.length - 30} more warnings (see JSON report)`);
      }
    }
  }

  // Save full report as JSON
  const reportPath = path.join(__dirname, 'seo-audit-report.json');
  const fullReport = {
    crawledAt: new Date().toISOString(),
    summary: {
      pagesCrawled: results.length,
      fromSitemap: results.filter(r => r.fromSitemap).length,
      discovered: discoveredUrls.length,
      avgResponseTime,
      avgWordCount,
      criticalIssues: critical.length,
      warnings: warnings.length,
      brokenLinks: brokenLinks.length,
      blockedByRobots,
      noindexPages: pagesWithNoindex,
      thinContent: thinPages,
      slowPages,
      missingCanonical,
      missingTitle,
      missingDesc,
      imagesWithoutAlt: totalImgNoAlt,
      duplicateTitles: [...titles.entries()].filter(([, u]) => u.length > 1),
      duplicateDescriptions: [...descriptions.entries()].filter(([, u]) => u.length > 1),
    },
    robotsRules,
    brokenLinks,
    discoveredUrls,
    critical,
    warnings,
    info,
    pages: results.map(r => ({
      url: r.url,
      statusCode: r.statusCode,
      responseTime: r.responseTime,
      title: r.title,
      titleLength: r.title ? r.title.length : 0,
      description: r.description,
      descriptionLength: r.description ? r.description.length : 0,
      h1: r.h1,
      wordCount: r.wordCount,
      canonical: r.canonical,
      internalLinks: r.internalLinks,
      imagesTotal: r.images ? r.images.length : 0,
      imagesWithoutAlt: r.images ? r.images.filter(i => !i.hasAlt).length : 0,
      fromSitemap: r.fromSitemap,
      issueCount: r.issues.length,
    })),
  };

  fs.writeFileSync(reportPath, JSON.stringify(fullReport, null, 2));
  console.log(`\nFull report saved to: seo-audit-report.json`);

  return { critical, warnings, info, brokenLinks };
}

// --- Main ---

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--url')) {
    const urlIdx = args.indexOf('--url');
    const url = args[urlIdx + 1];
    if (!url) { console.error('Provide a URL'); process.exit(1); }
    console.log(`Crawling single URL: ${url}`);
    const robotsRules = await fetchRobotsTxt(BASE_URL);
    const response = await fetchUrl(url);
    const result = analyzePage(response, robotsRules);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  let urls = getAllUrls();
  const discover = !args.includes('--no-discover');
  const summaryOnly = args.includes('--summary');
  const exportAsCsv = args.includes('--csv');

  if (args.includes('--quick')) {
    urls = urls.slice(0, 20);
    console.log(`Quick mode: crawling first ${urls.length} URLs\n`);
  } else {
    console.log(`Crawling ${urls.length} sitemap URLs${discover ? ' + link discovery' : ''}...\n`);
  }

  const { results, discoveredUrls, robotsRules } = await crawlAll(urls, CONCURRENCY, discover);
  const brokenLinks = findBrokenLinks(results);
  generateReport(results, discoveredUrls, brokenLinks, robotsRules, summaryOnly);

  if (exportAsCsv) {
    const csvPath = path.join(__dirname, 'seo-audit-report.csv');
    exportCsv(results, brokenLinks, csvPath);
    console.log(`CSV report saved to: seo-audit-report.csv`);
  }
}

main().catch(console.error);
