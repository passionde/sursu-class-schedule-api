import pathlib

import uvicorn

from config import PORT, HOST

if __name__ == "__main__":
    cwd = pathlib.Path(__file__).parent.resolve()
    uvicorn.run(
        "api.app:app",
        host=HOST,
        log_level="info",
        port=PORT,
        workers=1,
        log_config=f"{cwd}/log.ini"
    )
