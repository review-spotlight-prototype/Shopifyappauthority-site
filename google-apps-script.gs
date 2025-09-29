// Google Apps Script Code
// Copy this code to your Google Apps Script project

// IMPORTANT: After deploying this script:
// 1. Go to Extensions > Apps Script in your Google Sheet
// 2. Copy and paste this code
// 3. Click Deploy > New Deployment
// 4. Choose "Web app" as type
// 5. Set "Execute as" to "Me"
// 6. Set "Who has access" to "Anyone"
// 7. Click Deploy and copy the Web App URL
// 8. Replace YOUR_GOOGLE_APPS_SCRIPT_URL in email-capture.js with this URL

function doPost(e) {
  try {
    // Parse the incoming data
    const data = JSON.parse(e.postData.contents);

    // Open your specific spreadsheet
    const sheet = SpreadsheetApp.openById('1V2nbkaDo8SFS-tmME2nqGLDI5UJEaLZ7RaM5FusrNME').getActiveSheet();

    // Get headers from the first row
    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

    // If headers don't exist, create them
    if (headers[0] === '' || headers.length === 0) {
      const newHeaders = ['Timestamp', 'Email', 'Source Page', 'Capture Type', 'GDPR Consent', 'IP Address', 'User Agent', 'Referrer', 'UTM Source', 'UTM Medium', 'UTM Campaign'];
      sheet.getRange(1, 1, 1, newHeaders.length).setValues([newHeaders]);

      // Format header row
      const headerRange = sheet.getRange(1, 1, 1, newHeaders.length);
      headerRange.setFontWeight('bold');
      headerRange.setBackground('#f0f0f0');
    }

    // Prepare row data
    const rowData = [
      data.timestamp || new Date().toISOString(),
      data.email || '',
      data.source || '',
      data.type || 'newsletter',
      data.consent ? 'Yes' : 'No',
      data.ip || '',
      data.userAgent || '',
      data.referrer || '',
      data.utm_source || '',
      data.utm_medium || '',
      data.utm_campaign || ''
    ];

    // Append the data
    sheet.appendRow(rowData);

    // Optional: Send confirmation email to subscriber
    if (data.email && data.consent) {
      sendConfirmationEmail(data.email);
    }

    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        'result': 'success',
        'message': 'Email captured successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        'result': 'error',
        'error': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function sendConfirmationEmail(email) {
  try {
    const subject = 'Welcome to ShopifyAppAuthority Newsletter!';
    const htmlBody = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #95bf47;">Welcome to ShopifyAppAuthority!</h2>

        <p>Thank you for subscribing to our newsletter. You'll receive:</p>

        <ul>
          <li>Weekly recommendations for the best Shopify apps</li>
          <li>Exclusive discounts and deals</li>
          <li>Growth strategies for your ecommerce store</li>
          <li>Early access to new reviews and guides</li>
        </ul>

        <p>If you didn't subscribe, you can safely ignore this email or <a href="https://shopifyappauthority.com/unsubscribe">unsubscribe here</a>.</p>

        <p>Best regards,<br>
        The ShopifyAppAuthority Team</p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

        <p style="font-size: 12px; color: #666;">
          ShopifyAppAuthority.com<br>
          <a href="https://shopifyappauthority.com/privacy-policy/">Privacy Policy</a> |
          <a href="https://shopifyappauthority.com/unsubscribe">Unsubscribe</a>
        </p>
      </div>
    `;

    MailApp.sendEmail({
      to: email,
      subject: subject,
      htmlBody: htmlBody
    });
  } catch (error) {
    console.error('Error sending confirmation email:', error);
  }
}

// Test function to verify sheet connection
function testSheetConnection() {
  const sheet = SpreadsheetApp.openById('1V2nbkaDo8SFS-tmME2nqGLDI5UJEaLZ7RaM5FusrNME').getActiveSheet();
  console.log('Sheet name:', sheet.getName());
  console.log('Last row:', sheet.getLastRow());
  console.log('Last column:', sheet.getLastColumn());
}