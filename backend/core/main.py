import os
from dotenv import load_dotenv
load_dotenv()

import pypandoc
import sentry_sdk
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from logger import get_logger
from middlewares.cors import add_cors_middleware
from routes.api_key_routes import api_key_router
from routes.brain_routes import brain_router
from routes.chat_routes import chat_router
from routes.crawl_routes import crawl_router
from routes.explore_routes import explore_router
from routes.misc_routes import misc_router
from routes.prompt_routes import prompt_router
from routes.subscription_routes import subscription_router
from routes.upload_routes import upload_router
from routes.user_routes import user_router
from routes.personality_routes import personality_router

import uvicorn

logger = get_logger(__name__)


# ## GPTCache
# from gptcache import Cache
# from gptcache.manager.factory import manager_factory
# from gptcache.adapter.api import init_similar_cache
# from gptcache.processor.pre import get_prompt
# from langchain.cache import GPTCache
# import hashlib
# import langchain
# import time
# from langchain.llms import OpenAI
# from gptcache.adapter.langchain_models import LangChainLLMs


# def get_hashed_name(name):
#     return hashlib.sha256(name.encode()).hexdigest()


# def init_gptcache(cache_obj: Cache, llm: str):
#     hashed_llm = get_hashed_name(llm)
#     # init_similar_cache(cache_obj=cache_obj, data_dir=f"similar_cache_{hashed_llm}")
#     cache_obj.init(
#         pre_embedding_func=get_prompt,
#         data_manager=manager_factory()
#     )

# langchain.llm_cache = GPTCache(init_gptcache)

sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
    )

app = FastAPI()

add_cors_middleware(app)


@app.on_event("startup")
async def startup_event():
    if not os.path.exists(pypandoc.get_pandoc_path()):
        pypandoc.download_pandoc()


app.include_router(brain_router)
app.include_router(chat_router)
app.include_router(crawl_router)
app.include_router(explore_router)
app.include_router(misc_router)
app.include_router(upload_router)
app.include_router(user_router)
app.include_router(api_key_router)
app.include_router(subscription_router)
app.include_router(prompt_router)
app.include_router(personality_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# log more details about validation errors (422)
def handle_request_validation_error(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.error(request, exc_str)
        content = {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": exc_str,
            "data": None,
        }
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


handle_request_validation_error(app)

if __name__ == '__main__':
    # load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=5050)