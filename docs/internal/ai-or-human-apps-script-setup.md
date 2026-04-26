# AI or human? — Apps Script setup

One-time setup so the difficulty ratings on /ai-or-human/ end up in a
Google Sheet you own.

## 1. Create the Sheet

1. Go to https://sheets.new
2. Title it: "AI or human — difficulty ratings"
3. In row 1, add headers: `timestamp | lang | test | rating | user_score | total_score`
4. Copy the Sheet ID from the URL (the long string between `/d/` and `/edit`).

## 2. Create the Apps Script

1. From the Sheet: Tools → Apps Script
2. Replace the default code with:

```js
const SHEET_ID = 'PASTE_SHEET_ID_HERE';

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
  sheet.appendRow([
    new Date(data.ts),
    data.lang,
    data.test,
    data.rating,
    data.userScore,
    data.totalScore
  ]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3. Replace `PASTE_SHEET_ID_HERE` with the ID you copied above.
4. Click the disk icon to save.

## 3. Deploy as Web App

1. Click **Deploy → New deployment**.
2. Click the gear icon next to "Select type" → choose **Web App**.
3. Settings:
   - Description: `AI or human ratings sink`
   - Execute as: **Me**
   - Who has access: **Anyone** (no sign-in required — the POST has no sensitive data)
4. Click **Deploy**.
5. **Authorize the script** — first time only:
   1. Click **Auktorisera åtkomst** / **Authorize access** in the popup.
   2. Pick your Google account.
   3. You'll see a red warning: **"Google hasn't verified this app"**. This is expected — Google flags every personal Apps Script that hasn't gone through Google's app-verification process. Since you wrote the script yourself and it only writes to your own Sheet, it is safe.
   4. Click **Advanced** (link in the lower left).
   5. Click the link that appears: **"Go to [project name] (unsafe)"**.
   6. On the permissions screen, click **Allow** / **Tillåt**.
6. Copy the **Web App URL** that's now displayed (it looks like `https://script.google.com/macros/s/AKfy…/exec`).

## 4. Paste the URL into the JS file

Open `assets/js/ai-or-human.js` and replace the empty string on this line:

```js
const TELEMETRY_URL = '';
```

with the URL you copied:

```js
const TELEMETRY_URL = 'https://script.google.com/macros/s/AKfy…/exec';
```

Save, commit, and deploy.

## 5. Test it

1. Open `/ai-or-human/` in a browser.
2. Complete a test and click a rating button (1–6).
3. Wait ~5 seconds, then check the Sheet — a new row should appear.

## Notes

- If you redeploy the Apps Script (e.g. to fix a bug), the Web App URL stays the same — no need to update the JS constant.
- The sheet receives: timestamp (ISO), lang (`en`/`sv`), test (`text`/`image`/`video`), rating (1–6), user_score (number or null), total_score (number or null).
- Rows accumulate indefinitely. Archive or clear old data as you see fit.
