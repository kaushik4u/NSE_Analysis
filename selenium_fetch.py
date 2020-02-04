import asyncio
import sys

from arsenic import get_session, keys, browsers, services

if sys.platform.startswith('win'):
    CHROMEDRIVER_BINARY = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
else:
    CHROMEDRIVER_BINARY = '<CHROMEDRIVER_BINARY>'


async def hello_world():
    service = services.Chromedriver(binary=CHROMEDRIVER_BINARY)
    # service = services.Chromedriver()
    browser = browsers.Chrome(chromeOptions={
    'args': ['--headless', '--disable-gpu']
    })
    # service = services.Geckodriver(binary=GECKODRIVER)
    # browser = browsers.Firefox()
    async with get_session(service, browser) as session:
        await session.get('https://images.google.com/')
        search_box = await session.wait_for_element(5, 'input[name=q]')
        await search_box.send_keys('Cats')
        await search_box.send_keys(keys.ENTER)
        await asyncio.sleep(10)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello_world())


if __name__ == '__main__':
    main()
