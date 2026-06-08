from fastmcp import FastMCP
from fastapi import FastAPI
import uvicorn

mcp=FastMCP("fastapi-connect")


@mcp.tool
def reverse_text(text:str)->str:
    """Reverse a Text"""
    return text[::-1]

@mcp.tool
def word_length(text:str):
    """Returns the count of """
    return len([word for word in text.split()])

mcp_app=mcp.http_app(path="/")                                   # MCP exposed as http
app=FastAPI(title="FASTMCP_FASTAPI",lifespan=mcp_app.lifespan)

@app.get("/health")
def get_health():
    return {"Health":"ok"}

app.mount("/mcp",mcp_app)          # All requests coming at the /mcp will be forwarded to mcp_app

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
    