const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 900 });

  const reportPath = "file://" + path.resolve(__dirname, "report-lab8.html");
  await page.goto(reportPath, { waitUntil: "networkidle0" });

  await page.pdf({
    path: path.resolve(__dirname, "Lab8_Report_AnasBayoumy_22p0011.pdf"),
    format: "A4",
    printBackground: true,
    margin: { top: "0mm", right: "0mm", bottom: "0mm", left: "0mm" },
  });

  await browser.close();
  console.log("PDF generated: Lab8_Report_AnasBayoumy_22p0011.pdf");
})();
