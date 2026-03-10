/**
 * Прием данных от n8n для Книги Учета Благ
 */
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("КУБ_Данные");
  var data = JSON.parse(e.postData.contents);
  
  // Добавление строки: Дата | Суть | Категория | Статус ПСЗ | Анализ FDL
  sheet.appendRow([
    new Date(), 
    data.issue, 
    data.category, 
    "Инициация", 
    data.fdl_analysis
  ]);
  
  return ContentService.createTextOutput("Синхронизировано с НОВЕЯ").setMimeType(ContentService.MimeType.TEXT);
}
