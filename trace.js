const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  page.on('request', request => {
    if (request.url().includes('hot51') || request.url().includes('api')) {
      console.log('REQUEST:', request.method(), request.url());
    }
  });

  page.on('response', async response => {
    if (response.url().includes('hot51') || response.url().includes('api')) {
      console.log('RESPONSE:', response.url());
      if (response.url().includes('room') || response.url().includes('live')) {
        try {
          const body = await response.text();
          console.log('BODY:', response.url(), body.substring(0, 500));
        } catch (e) {}
      }
    }
  });

  await page.goto('https://www.hot51.living/liveCountry?areaCode=ID&name=Indonesia', { waitUntil: 'networkidle2' });
  await browser.close();
})();