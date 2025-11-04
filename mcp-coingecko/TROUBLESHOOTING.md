# Troubleshooting MCP Server Deployment

## Current Issue

The MCP server is crashing on Databricks Apps. We've tried:

1. ✅ Changed from `transport="sse"` to `transport="http"`
2. ✅ Renamed `server.py` to `app.py`
3. ✅ Added `/api/mcp` path
4. ❌ Using `mcp.run()` - FastMCP.run() doesn't support `port` parameter with HTTP transport
5. ❌ Using `mcp.get_asgi_app()` - method might not exist or wrong approach

## Error Messages

```
TypeError: FastMCP.run() got an unexpected keyword argument 'port'
```

## Potential Solutions to Try

### Option 1: Use FastMCP with stdio transport (not HTTP)
FastMCP might be designed for stdio transport, not HTTP for Databricks Apps.

### Option 2: Use official MCP Python SDK instead of FastMCP
The official `mcp` package might have better HTTP support.

### Option 3: Check FastMCP version and documentation
FastMCP API might have changed or HTTP transport might require different setup.

### Option 4: Use a different MCP framework
Consider using the examples from Databricks documentation directly.

## Next Steps

Need to research:
- Correct FastMCP HTTP transport setup for Databricks Apps
- Whether Databricks Apps requires specific MCP server framework
- Official examples from Databricks or FastMCP documentation
