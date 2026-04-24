import asyncio
import uvicorn

from app import create_app

app = create_app()


async def main() -> None:
    config = uvicorn.Config(
        "main:app", host="0.0.0.0", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    asyncio.run(main())
