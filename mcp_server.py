import asyncio
import os
import subprocess
import json
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("cyber-neo-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="scan_secrets",
            description="Scan a target directory for secrets and sensitive information using Cyber Neo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_dir": {"type": "string", "description": "Absolute path to the directory to scan"}
                },
                "required": ["target_dir"]
            }
        ),
        types.Tool(
            name="check_lockfiles",
            description="Check lockfiles in a target directory for supply chain security using Cyber Neo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_dir": {"type": "string", "description": "Absolute path to the directory to check"}
                },
                "required": ["target_dir"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if not arguments or "target_dir" not in arguments:
        return [types.TextContent(type="text", text="Error: target_dir is required")]
    target_dir = arguments["target_dir"]
    
    script_path = None
    if name == "scan_secrets":
        script_path = os.path.join(os.path.dirname(__file__), "skills", "cyber-neo", "scripts", "scan_secrets.py")
    elif name == "check_lockfiles":
        script_path = os.path.join(os.path.dirname(__file__), "skills", "cyber-neo", "scripts", "check_lockfiles.py")
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    if not os.path.exists(script_path):
        return [types.TextContent(type="text", text=f"Error: Script not found at {script_path}")]
        
    try:
        cmd = ["python3", script_path, target_dir, "--json"] if name == "scan_secrets" else ["python3", script_path, target_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return [types.TextContent(type="text", text=result.stdout or result.stderr)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Execution error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cyber-neo",
                server_version="0.1.0",
                capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={})
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
