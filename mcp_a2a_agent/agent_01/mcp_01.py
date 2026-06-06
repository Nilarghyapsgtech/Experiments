from fastmcp import FastMCP

mcp=FastMCP("Demo")

@mcp.tool
def add_numbers(a:int,b:int):
    """Add Two Numbers"""
    return a+b

if __name__=="__main__":
    mcp.run(transport="http")