G11 分解茶 
======================

成員：陳博煒、劉禹彤、柯逸鈞、涂穎珊


小組期末專案
=======================

## 資料取得

- [ ] crawler.py
    - 利用 Python 中的正則表達式 (re 套件)，夾取所需資訊。欄位包含「課程名稱」、「開課學期」、「授課對象」、「授課教師」、「課號」、「課程識別碼」、「班次」、「學分」、「全年/半年」、「必修/選修」、「上課時間」、「上課地點」、「備註」、「ceiba課程網站」、「課程大綱」（syllabus）、「課程大綱網址」，共 16 項。
    - 將資料儲存成 JSON 檔，命名為：original_course_data_108-1.json。
    - 註：crawler.py 為上述所提紅樓夢專案中的[爬蟲檔案](https://github.com/coding-coworking-club/dream-of-the-red-chamber)，因已有現成程式碼故不另重寫。檔案在 github 上開源，已取得原作者同意再利用。

## 資料前處理及自訂函數測試
- [ ] select_course.R
    - 選取流水號、課名、授課教師以及課程大綱這四欄作為主要資料處理對象，隨機篩選 100 筆課程，將課程列表儲存為 partial_100_course_data.csv
    
- [ ] 0104mark.rmd
    - 針對「課程大綱」這一欄，利用 JiebaR 套件斷詞
    - 利用 Quanteda 套件建立 Document-Feature Matrix，轉化為 tibble 後儲存為 dfm_course_tibble_100_0104
    - 根據 features_to_remove0102.txt 去除 Stop words
    - 建立Co-Occurence Matrix，轉化為 tibble 後儲存為 fcm_course_tibble_100_0104
    - 建立關鍵字輸入的自訂函數並測試，以用在 shinyApp 中

## 網頁呈現（shinyApp）
- [ ] app.R
    - 利用 Shiny 套件實現即時互動頁面
    - 輸入一關鍵字後，會回傳與關鍵字語意網路最為相關的課程結果
    - 結果可由頁面上之 Like 或是 Dislike 來選擇是否加入台大課程網選課名單，或是跳過繼續尋找下一門課程


