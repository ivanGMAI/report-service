from fastapi import UploadFile
from typing import AsyncIterator
import codecs
from infrastructure.error_handlers import FileErrorHandler


class AsyncFileReader:
    def __init__(self):
        self.error_handler = FileErrorHandler()

    async def read_lines(self, file: UploadFile) -> AsyncIterator[str]:
        raw_lines = self._read_internal(file)
        safe_lines = self.error_handler.safe_read_lines(file, raw_lines)

        async for line in safe_lines:
            yield line

    async def _read_internal(self, file: UploadFile) -> AsyncIterator[str]:
        await file.seek(0)
        remainder = b""
        decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

        while True:
            chunk = await file.read(8192)
            if not chunk:
                if remainder:
                    decoded = decoder.decode(remainder, final=True)
                    if decoded:
                        yield decoded.rstrip("\n")
                break

            decoded = decoder.decode(chunk)
            if not decoded:
                remainder += chunk
                continue

            if remainder:
                lines = decoded.split("\n")
                remainder_decoded = decoder.decode(remainder)
                lines[0] = remainder_decoded + lines[0]
                remainder = b""
            else:
                lines = decoded.split("\n")

            for line in lines[:-1]:
                if line:
                    yield line.rstrip("\n")

            last_line = lines[-1]
            if last_line:
                remainder = last_line.encode("utf-8")
            else:
                remainder = b""
