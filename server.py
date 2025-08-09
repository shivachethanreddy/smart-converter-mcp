from fastmcp import FastMCP
from fastapi import FastAPI, UploadFile
import shutil
import os

# FastAPI app for HTTP testing
api_app = FastAPI()

# MCP server
mcp = FastMCP(name="Smart Converter MCP")

# Core logic function (callable from both MCP and HTTP)
async def process_file(file: UploadFile):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(temp_path)
    return {"status": "received", "filename": file.filename, "size_bytes": file_size}

# MCP tool
@mcp.tool()
async def convert_file(file: UploadFile):
    """MCP tool wrapper for file conversion"""
    return await process_file(file)

# HTTP endpoint for testing / webhooks
@api_app.post("/mcp/convert_file")
async def convert_file_http(file: UploadFile):
    return await process_file(file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api_app, host="0.0.0.0", port=8085)

