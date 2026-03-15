from fastapi import HTTPException
import asyncio
from typing import AsyncIterator


class FileErrorHandler:
    @staticmethod
    async def safe_read_lines(file, read_gen: AsyncIterator[str]) -> AsyncIterator[str]:
        try:
            async for line in read_gen:
                yield line
        except (ConnectionError, OSError):
            raise HTTPException(status_code=500, detail="File read error occurred")
        except UnicodeDecodeError:
            await file.seek(0)
            content = await file.read()
            text = content.decode("utf-8", errors="replace")
            for line in text.split("\n"):
                line = line.rstrip("\n")
                if line:
                    yield line
        except asyncio.CancelledError:
            raise
