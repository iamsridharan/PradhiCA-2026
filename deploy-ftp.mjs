/**
 * One-shot FTP deploy to Hostinger (pradhica.com).
 * Uses FTP_* from .env. Excludes secrets and local tooling.
 *
 * Usage: node deploy-ftp.mjs
 */
import 'dotenv/config';
import * as ftp from 'basic-ftp';
import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const REMOTE_ROOT = '/';

const EXCLUDE_DIRS = new Set([
  '.git',
  'node_modules',
  '.agents',
  '.cursor',
  '__pycache__',
  '.vscode',
]);

const EXCLUDE_FILES = new Set([
  '.env',
  '.DS_Store',
  'deploy.sh',
  'deploy-ftp.mjs',
  'deploy-ftp-probe.mjs',
  'sync.js',
  'download.js',
  'package.json',
  'package-lock.json',
  'skills-lock.json',
  '.gitignore',
]);

const EXCLUDE_EXT = new Set(['.zip', '.pyc']);

function shouldSkip(relPath) {
  const parts = relPath.split(path.sep);
  if (parts.some((p) => EXCLUDE_DIRS.has(p))) return true;
  const base = parts[parts.length - 1];
  if (EXCLUDE_FILES.has(base)) return true;
  if (base.startsWith('.env')) return true;
  if (EXCLUDE_EXT.has(path.extname(base))) return true;
  return false;
}

function walk(dir, base = ROOT, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const abs = path.join(dir, entry.name);
    const rel = path.relative(base, abs);
    if (shouldSkip(rel)) continue;
    if (entry.isDirectory()) walk(abs, base, out);
    else if (entry.isFile()) out.push(rel);
  }
  return out;
}

async function main() {
  const { FTP_HOST, FTP_USER, FTP_PASSWORD } = process.env;
  if (!FTP_HOST || !FTP_USER || !FTP_PASSWORD) {
    console.error('Missing FTP_HOST / FTP_USER / FTP_PASSWORD in .env');
    process.exit(1);
  }

  const files = walk(ROOT);
  console.log(`Deploying ${files.length} files to ${FTP_HOST}${REMOTE_ROOT}...`);

  const client = new ftp.Client(120_000);
  client.ftp.verbose = false;

  try {
    await client.access({
      host: FTP_HOST,
      user: FTP_USER,
      password: FTP_PASSWORD,
      secure: false,
    });

    // Hostinger FTP often lands in home; cd into public_html
    try {
      await client.cd(REMOTE_ROOT);
    } catch {
      await client.cd('/public_html');
    }
    console.log(`Remote cwd: ${client.pwd ? await client.pwd() : '(ok)'}`);

    let uploaded = 0;
    for (const rel of files) {
      const local = path.join(ROOT, rel);
      const remote = rel.split(path.sep).join('/');
      const remoteDir = path.posix.dirname(remote);
      if (remoteDir && remoteDir !== '.') {
        await client.ensureDir(remoteDir);
        // ensureDir may leave cwd nested; reset to site root each time
        await client.cd(REMOTE_ROOT).catch(async () => client.cd('/public_html'));
      }
      await client.uploadFrom(local, remote);
      uploaded += 1;
      if (uploaded % 25 === 0 || uploaded === files.length) {
        console.log(`  ${uploaded}/${files.length}`);
      }
    }

    console.log(`Done. Uploaded ${uploaded} files.`);
  } finally {
    client.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
