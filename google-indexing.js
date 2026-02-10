/**
 * Google Indexing API Submission Script
 * Uses service account to request Google to crawl/index pages
 *
 * PREREQUISITES:
 * 1. Google Indexing API enabled in Google Cloud Console
 * 2. Service account email added as OWNER in Google Search Console for renthospitalbed.my
 *
 * Usage:
 *   node google-indexing.js --all              Submit all sitemap URLs
 *   node google-indexing.js --batch 50         Submit first 50 URLs
 *   node google-indexing.js <url1> [url2] ...  Submit specific URLs
 *   node google-indexing.js --status <url>     Check indexing status
 *   node google-indexing.js --reset            Reset tracker and resubmit all
 *
 * Rate limit: 200 URLs/day
 */

const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const SERVICE_ACCOUNT_PATH = path.join(__dirname, 'service_account.json');
const TRACKER_PATH = path.join(__dirname, '.indexing-tracker.json');
const SITEMAP_PATH = path.join(__dirname, 'sitemap.xml');
const BASE_URL = 'https://renthospitalbed.my';

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

// --- JWT / OAuth2 ---

function base64url(data) {
  return Buffer.from(data).toString('base64')
    .replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

function createJwt(serviceAccount) {
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: 'RS256', typ: 'JWT' };
  const payload = {
    iss: serviceAccount.client_email,
    scope: 'https://www.googleapis.com/auth/indexing',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600,
  };

  const headerB64 = base64url(JSON.stringify(header));
  const payloadB64 = base64url(JSON.stringify(payload));
  const signInput = `${headerB64}.${payloadB64}`;

  const sign = crypto.createSign('RSA-SHA256');
  sign.update(signInput);
  const signature = sign.sign(serviceAccount.private_key, 'base64')
    .replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');

  return `${signInput}.${signature}`;
}

function getAccessToken(serviceAccount) {
  return new Promise((resolve, reject) => {
    const jwt = createJwt(serviceAccount);
    const postData = `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=${jwt}`;

    const req = https.request({
      hostname: 'oauth2.googleapis.com',
      path: '/token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(postData),
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.access_token) {
            resolve(parsed.access_token);
          } else {
            reject(new Error(`Token error: ${data}`));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// --- Indexing API ---

function submitUrl(accessToken, url, type = 'URL_UPDATED') {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({ url, type });

    const req = https.request({
      hostname: 'indexing.googleapis.com',
      path: '/v3/urlNotifications:publish',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({ status: res.statusCode, body: data, url });
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

function checkStatus(accessToken, url) {
  return new Promise((resolve, reject) => {
    const encodedUrl = encodeURIComponent(url);
    const req = https.request({
      hostname: 'indexing.googleapis.com',
      path: `/v3/urlNotifications/metadata?url=${encodedUrl}`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({ status: res.statusCode, body: data });
      });
    });
    req.on('error', reject);
    req.end();
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// --- Tracker (skip already-submitted URLs) ---

function loadTracker() {
  if (fs.existsSync(TRACKER_PATH)) {
    return JSON.parse(fs.readFileSync(TRACKER_PATH, 'utf-8'));
  }
  return {};
}

function saveTracker(tracker) {
  fs.writeFileSync(TRACKER_PATH, JSON.stringify(tracker, null, 2));
}

function filterUnsubmitted(urls, tracker) {
  return urls.filter(url => !tracker[url]);
}

// --- Main ---

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Google Indexing API - renthospitalbed.my');
    console.log('========================================');
    console.log('Usage:');
    console.log('  node google-indexing.js --all');
    console.log('  node google-indexing.js --batch <count>');
    console.log('  node google-indexing.js <url1> [url2] ...');
    console.log('  node google-indexing.js --status <url>');
    console.log('  node google-indexing.js --reset --all    (reset tracker & resubmit)');
    console.log('');
    console.log('Rate limit: 200 URLs/day');
    return;
  }

  // Load service account
  if (!fs.existsSync(SERVICE_ACCOUNT_PATH)) {
    console.error('ERROR: service_account.json not found in project root');
    console.error('');
    console.error('Setup steps:');
    console.error('1. Go to https://console.cloud.google.com/');
    console.error('2. Enable "Web Search Indexing API"');
    console.error('3. Create a Service Account > download JSON key');
    console.error('4. Save it as "service_account.json" in this folder');
    console.error('5. Add the service account email as OWNER in GSC');
    process.exit(1);
  }

  const serviceAccount = JSON.parse(fs.readFileSync(SERVICE_ACCOUNT_PATH, 'utf-8'));
  console.log(`Using service account: ${serviceAccount.client_email}`);

  // Get access token
  console.log('Authenticating...');
  const accessToken = await getAccessToken(serviceAccount);
  console.log('Authenticated successfully\n');

  // Handle --status
  if (args[0] === '--status') {
    const url = args[1];
    if (!url) {
      console.error('Please provide a URL to check');
      process.exit(1);
    }
    const result = await checkStatus(accessToken, url);
    console.log(`Status for: ${url}`);
    console.log(JSON.parse(result.body));
    return;
  }

  // Load tracker
  const tracker = loadTracker();
  const resetTracker = args.includes('--reset');
  if (resetTracker) {
    saveTracker({});
    console.log('Tracker reset. All URLs will be resubmitted.\n');
    Object.keys(tracker).forEach(k => delete tracker[k]);
  }

  // Determine URLs to submit
  let allUrls = [];

  if (args.includes('--all')) {
    allUrls = getAllUrls();
    console.log(`Found ${allUrls.length} total URLs from sitemap.xml`);
  } else if (args[0] === '--batch') {
    const count = parseInt(args[1]) || 50;
    allUrls = getAllUrls().slice(0, count);
    console.log(`Batch: first ${count} of ${getAllUrls().length} URLs`);
  } else {
    allUrls = args.filter(a => !a.startsWith('--'));
  }

  // Filter out already-submitted URLs
  let urls = filterUnsubmitted(allUrls, tracker);
  const skipped = allUrls.length - urls.length;

  if (skipped > 0) {
    console.log(`Skipping ${skipped} already-submitted URLs`);
  }

  if (urls.length === 0) {
    console.log('All URLs already submitted! Use --reset to resubmit.');
    return;
  }

  if (urls.length > 200) {
    console.log(`WARNING: ${urls.length} URLs exceeds daily limit of 200.`);
    console.log(`Only the first 200 will be submitted.\n`);
    urls = urls.slice(0, 200);
  }

  console.log(`Submitting ${urls.length} remaining URLs to Google Indexing API...\n`);

  let success = 0;
  let failed = 0;
  let quotaHit = false;

  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    try {
      const result = await submitUrl(accessToken, url);

      if (result.status === 200) {
        success++;
        tracker[url] = new Date().toISOString();
        saveTracker(tracker);
        console.log(`[${i + 1}/${urls.length}] OK  ${url}`);
      } else {
        const body = JSON.parse(result.body);
        const msg = body.error?.message || result.body;

        if (msg.includes('Quota exceeded')) {
          failed++;
          console.log(`[${i + 1}/${urls.length}] QUOTA HIT - stopping early`);
          console.log(`Remaining ${urls.length - i - 1} URLs will be submitted next run.`);
          quotaHit = true;
          break;
        }

        failed++;
        console.log(`[${i + 1}/${urls.length}] ERR ${url} - ${msg}`);
      }
    } catch (err) {
      failed++;
      console.log(`[${i + 1}/${urls.length}] ERR ${url} - ${err.message}`);
    }

    // Small delay to avoid rate limiting
    if (i < urls.length - 1) {
      await sleep(100);
    }
  }

  const totalDone = Object.keys(tracker).length;
  const totalUrls = getAllUrls().length;

  console.log(`\n========================================`);
  console.log(`This run: ${success} submitted, ${failed} failed`);
  console.log(`Progress: ${totalDone}/${totalUrls} URLs submitted total`);
  if (quotaHit) {
    console.log(`\nQuota hit! Run again tomorrow to continue.`);
  } else if (totalDone >= totalUrls) {
    console.log(`\nAll URLs submitted!`);
  }
}

main().catch(console.error);
