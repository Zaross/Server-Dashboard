import os
import mimetypes
import uvicorn
import database.create_database
from api import login as api

WEB_ROOT = "WebRoot"

async def WebServer(scope, receive, send):
    if scope['type'] == 'http':
        path = scope['path']
        if path == '/':
            path = '/index.html'
        
        file_path = os.path.join(WEB_ROOT, path.lstrip("/"))
        
        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            
            with open(file_path, 'rb') as f:
                content = f.read()

            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', mime_type.encode('utf-8')],
                ],
            })
            await send({
                'type': 'http.response.body',
                'body': content,
            })
        else:
            await send({
                'type': 'http.response.start',
                'status': 404,
                'headers': [
                    [b'content-type', b'text/html'],
                ],
            })
            await send({
                'type': 'http.response.body',
                'body': b"<h1>404 Not Found</h1>",
            })

if __name__ == "__main__":
    uvicorn.run("main:WebServer", port=5000, log_level="info")
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="info")
    database.create_database.init_db()
