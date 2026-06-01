from fastapi import APIRouter,Depends
import httpx
from app.core.config import get_settings
from app.core.deps import get_current_user

router=APIRouter(prefix="/api/ai",tags=["AI"])
settings=get_settings()
def _ok():return settings.AI_API_KEY and settings.AI_API_KEY!="sk-your-api-key-here"

@router.post("/summarize")
async def summarize(content:str,user=Depends(get_current_user)):
    if not _ok():return {"summary":"AI not configured"}
    async with httpx.AsyncClient() as c:
        r=await c.post(f"{settings.AI_BASE_URL}/chat/completions",headers={"Authorization":f"Bearer {settings.AI_API_KEY}"},json={"model":settings.AI_MODEL,"messages":[{"role":"system","content":"Generate concise summary in 100 words"},{"role":"user","content":content[:2000]}],"temperature":0.5},timeout=30)
        return {"summary":r.json()["choices"][0]["message"]["content"]}

@router.post("/tags")
async def suggest_tags(title:str,content:str,user=Depends(get_current_user)):
    if not _ok():return {"tags":[]}
    async with httpx.AsyncClient() as c:
        r=await c.post(f"{settings.AI_BASE_URL}/chat/completions",headers={"Authorization":f"Bearer {settings.AI_API_KEY}"},json={"model":settings.AI_MODEL,"messages":[{"role":"system","content":"Suggest 3-5 tags, comma-separated"},{"role":"user","content":f"Title: {title}\n{content[:1000]}"}],"temperature":0.3},timeout=30)
        return {"tags":[t.strip() for t in r.json()["choices"][0]["message"]["content"].split(",")]}
