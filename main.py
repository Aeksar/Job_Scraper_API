from fastapi import FastAPI
import uvicorn

from api.endpoints.parse import parse_rout

app = FastAPI(title="Job Scraper API")
app.include_router(parse_rout)

if __name__=="__main__":
    uvicorn.run(app)