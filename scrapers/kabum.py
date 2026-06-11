import pandas as pd
from playwright.async_api import async_playwright


async def scrape_kabum(produto: str) -> pd.DataFrame:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = f"https://www.kabum.com.br/busca/{produto.replace(' ', '-')}"
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        items = await page.query_selector_all("main a[href*='/produto/']")

        for item in items:
            try:
                title = await item.query_selector("span.text-ellipsis.line-clamp-2")
                price = await item.query_selector_all(
                    "span.text-base.font-semibold.text-gray-800"
                )
                link = await item.get_attribute("href")

                text_title = await title.inner_text() if title else "N/A"
                text_price = await price[1].inner_text() if len(price) >= 2 else "N/A"

                if text_title and text_price:
                    price_num = (
                        float(
                            text_price.strip()
                            .replace("R$", "")
                            .replace(".", "")
                            .replace(",", ".")
                            .strip()
                        )
                        if text_price
                        else None
                    )

                    results.append(
                        {
                            "title": text_title.strip(),
                            "price": price_num,
                            "Store": "Kabum",
                            "link": f"https://www.kabum.com.br{link}"
                            if link
                            else "N/A",
                        }
                    )
            except Exception:
                continue

        await browser.close()

    return pd.DataFrame(results)
