# little-dino · 小小恐龍探險家

適合 4–7 歲孩子的恐龍圖鑑 PWA，使用繁體中文與台灣注音。

- 20 種恐龍；中文名、直排注音與右側聲調、英文名。
- 中文／英文發音、慢速朗讀、整篇或分段朗讀。
- 每種恐龍四段介紹、年代、全長估計、化石發現地及觀察問答。
- 聽名字選恐龍、看特徵猜恐龍；入門與挑戰模式。
- 搜尋、食性篩選、收藏、離線快取。

## 正式網站

- Cloudflare：https://little-dino.pmebruce.workers.dev/
- GitHub Pages：https://pmebruce.github.io/little-dino/

## 發布

本專案不需要建置；靜態網頁檔案位於程式庫根目錄。

GitHub Pages：Settings → Pages → Deploy from a branch → main → / (root)。

Cloudflare Pages：連接此程式庫，Framework preset 選 None，Build command 留空，Build output directory 填 `.`。

若使用 Cloudflare Workers 靜態資源部署，執行 `npx wrangler deploy`，使用本專案的 `wrangler.jsonc`。

## iPhone 安裝

用 Safari 開啟網站，按「分享」→「加入主畫面」。首次連線載入完成後，可離線瀏覽。離線朗讀需要裝置已下載對應語音；音色及英文學名發音依裝置而異。

## 圖片與資料

照片與復原模型的作者、原始來源、授權皆列於 `photos.json` 及 App 圖說。圖片各自依標示的 Creative Commons 或公有領域條件提供，程式庫未為第三方圖片另行變更授權。

內容主要參考英國自然史博物館 Dino Directory，補充法國國立自然史博物館。各恐龍的原始連結列於 `profiles.json`。

模型配色及部分姿勢是復原推測，並不代表恐龍真實色彩或已確定的行為。化石展示可能包含原始化石、複製件與補配骨骼。

## 更新快取

更新 CSS 或 JS 時，同步提高 `index.html` 的資源版本與 `sw.js` 的快取版本；修改恐龍資料時更新 `data.js` 和 `profiles.json`。

## Phaser 互動關卡

首頁新增 `adventure.html` 入口；使用本機隨附 Phaser 3.90.0 Arcade build（MIT），不依賴 CDN。每回合五個不重複任務，兩個難度提供 2／3 個不同答案；支援觸控拖曳及等價大按鈕，答錯可重試，答對鎖定防止重複計分，減少動態效果設定生效。引擎動畫與新玩法不改寫既有題目／適性學習邏輯。新關卡紀錄存在裝置；英語與注音答對星星也加入原 App 星星總數。

`node --test tests/phaser-rounds.test.mjs` 檢查回合與選項唯一性、重試／計分鎖定及打包資產。語音使用裝置語音，中文限台灣中文；沒有適合語音時提供文字提示與陪讀訊息。未在真實 iPhone/iPad 完成操作驗證。

化石挖掘關使用原有 8 種博物館骨架展示照片；來源、作者、授權與展示說明逐題顯示，沒有新增或重製化石照片。刷開 6 格後才能作答；難度只改答案數量，不冒稱照片裡每塊骨骼均為原始化石。
