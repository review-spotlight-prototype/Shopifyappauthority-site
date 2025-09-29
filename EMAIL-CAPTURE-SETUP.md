# Email Capture Setup Instructions

## Overview
Your website now has a GDPR-compliant email capture system with:
- GDPR consent checkbox on all forms
- Email popup with exit intent and time delay triggers
- Google Sheets integration for storing submissions
- UTM parameter tracking
- Automatic confirmation emails

## Google Sheets Setup (REQUIRED)

### Step 1: Set Up Google Apps Script

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1V2nbkaDo8SFS-tmME2nqGLDI5UJEaLZ7RaM5FusrNME/

2. Go to **Extensions > Apps Script**

3. Delete any existing code and paste the entire contents of `google-apps-script.gs`

4. Click **Save** (💾 icon)

5. Click **Deploy > New Deployment**

6. Configure deployment:
   - Type: **Web app**
   - Description: "Email Capture API"
   - Execute as: **Me**
   - Who has access: **Anyone**

7. Click **Deploy**

8. **IMPORTANT**: Copy the Web App URL (it will look like: https://script.google.com/macros/s/AKfycb.../exec)

### Step 2: Update JavaScript with Your URL

1. Open `email-capture.js`

2. Find this line (around line 4):
   ```javascript
   this.googleSheetURL = 'YOUR_GOOGLE_APPS_SCRIPT_URL';
   ```

3. Replace `YOUR_GOOGLE_APPS_SCRIPT_URL` with the URL you copied from Google Apps Script

4. Save the file

## Features

### 1. Email Capture Forms
- Automatically adds GDPR consent to all forms
- Tracks source page and capture type
- Shows success message after submission

### 2. Email Popup
- Shows after 30 seconds OR on exit intent
- Only shows once per day
- Doesn't show if user already subscribed
- Mobile-responsive design

### 3. Data Collected
Your Google Sheet will receive these columns:
- **Timestamp**: When the email was submitted
- **Email**: User's email address
- **Source Page**: Which page they were on
- **Capture Type**: newsletter/popup
- **GDPR Consent**: Yes/No
- **IP Address**: (if available)
- **User Agent**: Browser information
- **Referrer**: Where they came from
- **UTM Source/Medium/Campaign**: Marketing attribution

### 4. Confirmation Emails
- Automatically sends welcome email to new subscribers
- Edit the email template in the Google Apps Script

## Customization Options

### Change Popup Timing
In `email-capture.js`, line ~130:
```javascript
setTimeout(() => this.showPopup(), 30000); // Change 30000 to desired milliseconds
```

### Change Popup Content
Edit the HTML in `showPopup()` function (line ~170)

### Disable Popup on Specific Pages
Add to the page's JavaScript:
```javascript
window.disableEmailPopup = true;
```

## Testing

1. Visit your website in an incognito/private browser window
2. Wait 30 seconds or move your mouse to the top of the page (exit intent)
3. The popup should appear
4. Submit an email with consent checked
5. Check your Google Sheet for the new entry
6. Check if confirmation email was sent

## Privacy Compliance

The system is GDPR-compliant with:
- ✅ Explicit consent checkbox
- ✅ Link to privacy policy
- ✅ Clear description of what users are signing up for
- ✅ Unsubscribe option in emails
- ✅ Data minimization (only collect necessary data)

## Troubleshooting

### Emails not appearing in Google Sheet
1. Check that you deployed the Google Apps Script
2. Verify the URL in email-capture.js is correct
3. Check browser console for errors
4. Test the Google Apps Script directly using the test function

### Popup not showing
1. Clear cookies/local storage
2. Check browser console for JavaScript errors
3. Verify email-capture.js is loading on the page

### Confirmation emails not sending
1. Check Google Apps Script execution logs
2. Verify MailApp quota hasn't been exceeded (100 emails/day for free accounts)
3. Check spam folder

## Next Steps

1. **Set up the Google Apps Script** (most important!)
2. Test the system thoroughly
3. Consider integrating with a proper email service (Moosend, ActiveCampaign, etc.)
4. Monitor your Google Sheet for submissions
5. Set up email automation sequences

## Alternative CRM Integrations

Instead of Google Sheets, you can modify `sendToGoogleSheets()` to send to:
- **Moosend**: Use their API
- **ActiveCampaign**: Use their API
- **Zapier**: Send to a webhook for any CRM
- **Make (Integromat)**: Send to a webhook

Contact support for help with specific CRM integrations.