from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(
    title="MTG Proxy",
    servers=[
        {"url": "https://mtg-proxy-6ylf.onrender.com"}
    ]
)

SCRYFALL_NAMED_URL = "https://api.scryfall.com/cards/named"
SCRYFALL_CARD_URL = "https://api.scryfall.com/cards"

@app.get("/cards/search")
async def search_card(q: str):
    async with httpx.AsyncClient() as client:
        # First try exact
        resp = await client.get(SCRYFALL_NAMED_URL, params={"exact": q})

        # If exact fails, try fuzzy
        if resp.status_code != 200:
            resp = await client.get(SCRYFALL_NAMED_URL, params={"fuzzy": q})

        if resp.status_code != 200:
            raise HTTPException(status_code=404, detail="Card not found")

        data = resp.json()

        return {
            "cards": [
                {
                    "id": data["id"],
                    "name": data["name"]
                }
            ]
        }

@app.get("/cards/{card_id}")
async def get_card(card_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{SCRYFALL_CARD_URL}/{card_id}")

        if resp.status_code != 200:
            raise HTTPException(status_code=404, detail="Card not found")

        data = resp.json()

        return {
    "id": data.get("id"),
    "name": data.get("name"),
    "mana_cost": data.get("mana_cost"),
    "cmc": data.get("cmc"),
    "type_line": data.get("type_line"),
    "oracle_text": data.get("oracle_text"),
    "color_identity": data.get("color_identity", []),
    "keywords": data.get("keywords", []),
    "rarity": data.get("rarity"),
    "legalities": data.get("legalities", {})
}