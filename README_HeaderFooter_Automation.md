# Header & Footer Automation for PradhiCA Website

## 🎯 Overview

This folder contains automation scripts to keep headers and footers synchronized across all HTML pages, using `index.html` as the master template.

## ✅ Current Status

**Sitewide chrome (latest / v2026.03):** Premium header & footer CSS (`header-premium.css`, `footer-premium.css`) applied across root HTML pages; counts vary as new batch pages are added.

**Historical note:** Earlier automation runs synced **92+** headers/footers to `index.html`. Re-run `update_headers_footers.py` (or your pipeline) after bulk template changes.

- ✅ **92 headers** updated with Telegram link (ti-location-arrow) *(legacy run)*
- ✅ **92 footers** updated with 2025 copyright *(legacy run)*
- ✅ Template source: `index.html`

## 🛠 Automation Solutions

### 1. Manual Sync Script

**File:** `update_headers_footers.py`

**Usage:**
```bash
python3 update_headers_footers.py
```

**Features:**
- Extracts header/footer from `index.html`
- Updates all other HTML files automatically
- Detailed logging and error handling
- Safe file handling with encoding preservation

### 2. Auto-Watch Script (Recommended)

**File:** `watch_and_sync.py`

**Installation:**
```bash
pip install watchdog
```

**Usage:**
```bash
python3 watch_and_sync.py
```

**Features:**
- Monitors `index.html` for changes in real-time
- Automatically syncs headers/footers when `index.html` is modified
- Runs in background
- Cooldown protection against rapid-fire updates

### 3. Git Hook Solution (Advanced)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 update_headers_footers.py
git add *.html
```

**Features:**
- Automatically syncs before each git commit
- Ensures consistency across version control

## 📋 Standard Template (from index.html)

### Header Template:
- Contact info: `pradhica4u@gmail.com`, `+918072653948`
- Social links: Facebook, Instagram, **Telegram** (ti-location-arrow)

### Footer Template:
- Copyright: `© 2025 PradhiCA. All rights reserved.`
- Credit: `Created and Designed by Techrethought`

## 🔄 Workflow for Future Updates

### Option A: Use Auto-Watch (Recommended)
1. Run `python3 watch_and_sync.py` in background
2. Edit `index.html` header/footer as needed
3. Save the file
4. **All other HTML files automatically update!**

### Option B: Manual Sync
1. Edit `index.html` header/footer
2. Run `python3 update_headers_footers.py`
3. All files get updated

### Option C: IDE Integration
Add to your editor's build/save commands:
```bash
python3 update_headers_footers.py
```

## 🎯 Benefits

1. **Single Source of Truth**: Only edit header/footer in `index.html`
2. **Instant Propagation**: Changes automatically apply to all pages
3. **Error Prevention**: No more inconsistent headers/footers
4. **Time Saving**: No manual copy-paste across 100+ files
5. **Future-Proof**: Works for any number of HTML files

## 🚀 Quick Start

1. **Test the sync manually:**
   ```bash
   python3 update_headers_footers.py
   ```

2. **Start auto-watching:**
   ```bash
   pip install watchdog
   python3 watch_and_sync.py
   ```

3. **Edit index.html** and watch the magic happen!

## 📝 File Patterns

The scripts look for these patterns:

**Header Pattern:**
```html
<header class="site-header bg-dark text-white-0_5">
  <!-- content -->
</header><!-- END site header-->
```

**Footer Pattern:**
```html
<p class="text-white-0_5 mb-0">&copy; YYYY PradhiCA. All rights reserved. Created and Designed by <a href="https://techrethought.com" target="_blank">Techrethought</a></p>
```

## ⚡ Pro Tips

1. **Background Running**: The watch script can run continuously in background
2. **Version Control**: Include these scripts in your git repository
3. **Backup**: Scripts preserve original files (safe operations)
4. **Logging**: Check console output for detailed sync reports

---

**Automation Setup Complete!** ✨

Now you can edit headers/footers in just one place (`index.html`) and have them automatically propagate to all 100+ HTML files!
