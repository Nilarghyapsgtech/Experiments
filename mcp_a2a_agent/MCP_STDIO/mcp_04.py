from fastmcp import FastMCP

mcp=FastMCP("demo")

@mcp.tool
def add(a:int,b:int):
    """Add Two numbers"""
    return a+b

@mcp.tool
def divide(a:int,b:int):
    """Divide two numbers"""
    if b==0:
        raise ValueError("divisor can't be zero")
    return a/b

if __name__=="__main__":
    mcp.run(transport="stdio")