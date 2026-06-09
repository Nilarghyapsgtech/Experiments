from fastmcp import FastMCP

mcp=FastMCP("demo")

@mcp.tool
def sum(a:int,b:int):
    return a+b

@mcp.tool
def divide(a:int,b:int):
    if b==0:
        raise ValueError(f"b can't be 0")
    return a/b

mcp.run(transport="http")