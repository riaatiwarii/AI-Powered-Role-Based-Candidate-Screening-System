"""
Backend application entry point.
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import get_settings

    settings = get_settings()

    uvicorn.run(
        app,
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
    )
