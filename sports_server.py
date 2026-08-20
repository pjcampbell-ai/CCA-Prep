"""
Minimal MCP server exposing one Premier League tool.
"""

import httpx
from fastmcp import FastMCP

mcp = FastMCP("sports-info")


@mcp.tool()
def get_premier_league_table() -> str:
    """Get the current English Premier League table with team positions, played, won, drawn, lost, and points."""
    
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        standings = data["standings"][0]["table"]
        
        lines = ["Premier League — Current Standings\n"]
        lines.append(f"{'Pos':<4} {'Team':<25} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'Pts':<4}")
        lines.append("-" * 60)
        
        for team in standings:
            lines.append(
                f"{team['position']:<4} "
                f"{team['team']['name'][:24]:<25} "
                f"{team['playedGames']:<4} "
                f"{team['won']:<4} "
                f"{team['draw']:<4} "
                f"{team['lost']:<4} "
                f"{team['points']:<4}"
            )
        
        return "\n".join(lines)
    
    except httpx.HTTPError as e:
        return f"Error fetching Premier League table: {str(e)}"
    except (KeyError, IndexError):
        return "Error: unexpected response format from football-data.org"


if __name__ == "__main__":
    mcp.run()