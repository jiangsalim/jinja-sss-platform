"""CORS Configuration"""

from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5000", "https://jinjasss.sc.ug"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
