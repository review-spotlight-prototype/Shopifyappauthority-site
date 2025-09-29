// Simplified Google Apps Script (No Email Sending)
// This version only saves to sheets, no email permissions needed

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

// Test function to verify sheet connection
function testSheetConnection() {
  const sheet = SpreadsheetApp.openById('1V2nbkaDo8SFS-tmME2nqGLDI5UJEaLZ7RaM5FusrNME').getActiveSheet();
  console.log('Sheet name:', sheet.getName());
  console.log('Last row:', sheet.getLastRow());
  console.log('Last column:', sheet.getLastColumn());

  // Test adding a row
  sheet.appendRow(['Test', 'test@example.com', '/test', 'test', 'Yes', '', '', '', '', '', '']);
  console.log('Test row added successfully!');
}