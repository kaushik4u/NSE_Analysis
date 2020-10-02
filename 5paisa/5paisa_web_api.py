import asyncio
import json
from pyppeteer import launch

async def intercept_network_response(response):
	# In this example, we care only about responses returning JSONs
	if "application/json" in response.headers.get("content-type", ""):
		# Print some info about the responses
		print("URL:", response.url)
		print("Method:", response.request.method)
		print("Response headers:", response.headers)
		print("Request Headers:", response.request.headers)
		print("Response status:", response.status)
		# Print the content of the response
		try:
			# await response.json() returns the response as Python object
			print("Content: ", await response.json())
		except json.decoder.JSONDecodeError:
			# NOTE: Use await response.text() if you want to get raw response text
			print("Failed to decode JSON from", await response.text())

async def main():
	browser = await launch({'headless':False})
	page = await browser.newPage()
	page.on('response', intercept_network_response)
	await page.goto('https://www.5paisa.com/')
	# await page.screenshot({'path': 'example.png'})
	await page.waitForSelector('#login-btn')
	await page.click('#login-btn')
	# await.waitForSelector('#loginDiv')
	await page.
	await page.waitFor(5000)
	await browser.close()

asyncio.get_event_loop().run_until_complete(main())