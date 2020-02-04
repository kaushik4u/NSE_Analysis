import asyncio
from pyppeteer import launch


async def main(datestring):
    bhavurl = 'https://www1.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date=' + datestring + '&section=EQ'
    nse_bhav = 'https://www.nseindia.com/products/content/equities/equities/archieve_eq.htm'
    browser = await launch({
        'headless': False,
        'executablePath': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        })
    page = await browser.newPage()
    print('fetching... ',bhavurl)
    await page.goto(bhavurl)
    await page.waitForSelector('a')
    # cdp = await page.target.createCDPSession()
    # await cdp.send("Page.setDownloadBehavior", {
    #     "behavior": "allow", 
    #     "downloadPath": "C:/Users/608619925/Desktop/Misc Projects/python/nse_test/NSE_Data/data/temp"
    # })
    # await page._client.send('Page.setDownloadBehavior', {
    #     'behavior': 'allow',
    #     'downloadPath': 'C:/Users/608619925/Desktop/Misc Projects/python/nse_test/NSE_Data/data/temp'
    # })
    fileName = await page.querySelectorEval(
        "a", "elem => elem.textContent"
    )
    print(fileName)
    await page.click('a')
    # await page.waitForNavigation({'waitUntil': 'networkidle2'})
    # await page.evaluate('''()=>{
    #     document.querySelector('#h_filetype').selectedIndex = 1
    #     document.querySelector('#date').value = "'''+datestring+'''"
    #     document.querySelector('.getdata-button').click()
    # }''')
    # await page.screenshot({'path': 'example.png'})
    
    await browser.close()

startDate = '01-01-2015'  # mm-dd-yyyy
asyncio.get_event_loop().run_until_complete(main(startDate))
# main(startDate)
