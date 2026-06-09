from fastmcp import FastMCP

mcp=FastMCP("demo")

@mcp.tool
def get_nth_power(x,n):
    return x**n

if __name__=="__main__":
    mcp.run(transport="http",port=8000,host="127.0.0.1",path="/mcp")