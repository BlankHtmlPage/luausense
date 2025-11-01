"""
LuauSense - Intelligent autocompletion for Luau scripting language.

This module provides case-sensitive autocompletion for Luau keywords,
built-in functions, and language constructs.
"""

from typing import List, Final

# Luau keywords and built-in functions database
LUAU_KEYWORDS: Final[list[str]] = [
    # Language keywords
    "and", "break", "do", "else", "elseif", "end", "false", "for", "function",
    "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then",
    "true", "until", "while", "continue", "export", "type", "::",  # :: used in casts/type annotations

    # Core globals (Lua-compatible)
    "_G", "_VERSION",
    "assert", "collectgarbage", "dofile", "error", "getmetatable", "ipairs",
    "load", "loadfile", "loadstring", "next", "pairs", "pcall", "print",
    "rawequal", "rawget", "rawlen", "rawset", "require", "select",
    "setmetatable", "tonumber", "tostring", "type", "xpcall",

    # coroutine library
    "coroutine.create", "coroutine.resume", "coroutine.running",
    "coroutine.status", "coroutine.wrap", "coroutine.yield",

    # package library
    "package.config", "package.cpath", "package.path", "package.loaded",
    "package.loaders", "package.searchers", "package.searchpath", "package.preload",
    "package.loadlib",

    # string library
    "string.byte", "string.char", "string.dump", "string.find", "string.format",
    "string.gmatch", "string.gsub", "string.len", "string.lower", "string.match",
    "string.rep", "string.reverse", "string.sub", "string.upper",

    # table library
    "table.concat", "table.insert", "table.move", "table.pack", "table.remove",
    "table.sort", "table.unpack", "table.maxn",

    # math library
    "math.abs", "math.acos", "math.asin", "math.atan", "math.atan2", "math.ceil",
    "math.cos", "math.cosh", "math.deg", "math.exp", "math.floor", "math.fmod",
    "math.frexp", "math.huge", "math.ldexp", "math.log", "math.log10", "math.max",
    "math.min", "math.modf", "math.pi", "math.pow", "math.rad", "math.random",
    "math.randomseed", "math.sin", "math.sinh", "math.sqrt", "math.tan", "math.tanh",

    # io library
    "io.close", "io.flush", "io.input", "io.lines", "io.open", "io.output",
    "io.popen", "io.read", "io.tmpfile", "io.type", "io.write",

    # os library
    "os.clock", "os.date", "os.difftime", "os.execute", "os.exit", "os.getenv",
    "os.remove", "os.rename", "os.time", "os.tmpname",

    # debug library
    "debug.debug", "debug.gethook", "debug.getinfo", "debug.getlocal",
    "debug.getmetatable", "debug.getregistry", "debug.getupvalue",
    "debug.sethook", "debug.setlocal", "debug.setupvalue", "debug.traceback",

    # utf8 library
    "utf8.char", "utf8.charpattern", "utf8.codepoint", "utf8.codes",
    "utf8.len", "utf8.offset", "utf8.nfcnormalize", "utf8.normalize", "utf8.next",

    # Additional/compat globals sometimes present
    "unpack", "module", "package.loaders", "loadlib", "bit32", "bit32.band",
    "bit32.bnot", "bit32.bor", "bit32.bxor", "bit32.lshift", "bit32.rshift",
    "bit32.arshift", "bit32.extract", "bit32.replace", "bit32.test",

    # Common Lua-ecosystem helpers and deprecated/compat names
    "pairsByKeys", "table.foreach", "table.foreachi",

    # Luau-specific operators and builtin helpers
    "typeof", "typeofexport",  # typeof is a builtin; 'export' is a keyword (included above)

    # Luau standard library helpers (language/runtime-level)
    "warn", "ipairs", "pairs", "next", "tick", "time", "os", "wait", "spawn", "delay",
    "setfenv", "getfenv",  # compatibility names (may or may not be available depending on runtime)

    # Roblox-specific common globals and utility objects (commonly used in Luau on Roblox)
    "game", "workspace", "script", "shared", "workspace", "players", "player", "Players",
    "Instance", "Instance.new", "Enum", "CFrame", "Vector3", "UDim", "UDim2", "BrickColor",
    "Color3", "Ray", "Region3", "RaycastParams", "PhysicalProperties", "NumberSequence",
    "NumberSequenceKeypoint", "ColorSequence", "ColorSequenceKeypoint", "TweenInfo",
    "TweenService", "RunService", "UserInputService", "InputService", "HttpService",
    "MarketplaceService", "Debris", "CollectionService", "ReplicatedStorage", "ReplicatedFirst",
    "StarterGui", "StarterPack", "StarterPlayer", "Lighting", "Players", "SoundService",
    "TextService", "PathfindingService", "PhysicsService", "NetworkServer", "NetworkClient",
    "LocalizationService", "LogService", "MemoryStoreService", "MessagingService",

    # Roblox convenience/global functions
    "GetService", "FindFirstChild", "FindFirstChildWhichIsA", "FindFirstChildOfClass",
    "IsA", "Connect", "Wait", "Clone", "Destroy", "GetChildren", "GetDescendants",
    "BindToClose", "Kick", "LoadAnimation", "Play", "Stop", "FireAllClients", "FireClient",
    "FireServer", "OnClientEvent", "OnServerEvent", "InvokeClient", "InvokeServer",

    # Common type and reflection helpers
    "typeof", "table.freeze", "table.isfrozen", "table.clear",

    # Misc utilities and syntactic helpers that appear in Luau/Roblox docs or community code
    "Promise", "Signal", "Task", "task.defer", "task.delay", "task.spawn", "task.wait", "task.cancel",
    "HttpService:GetAsync", "HttpService:PostAsync", "HttpService:RequestAsync",
]


class TooShortRequestError(ValueError):
    """Exception raised when autocomplete query is too short."""
    
    def __init__(self, query: str, min_length: int = 2) -> None:
        self.query = query
        self.min_length = min_length
        super().__init__(
            f"Autocomplete query '{query}' is too short. "
            f"Minimum length required: {min_length}"
        )


def autocomplete(query: str) -> List[str]:
    """
    Get autocomplete suggestions for Luau keywords and built-in functions.
    
    Args:
        query: The string to autocomplete (minimum 2 characters)
        
    Returns:
        List of Luau keywords and functions that start with the query
        
    Raises:
        TooShortRequestError: If query length is less than 2 characters
    """
    if len(query) < 2:
        raise TooShortRequestError(query)
    
    # Case-sensitive prefix matching using list comprehension for O(n) performance
    matches = [keyword for keyword in _LUAU_KEYWORDS if keyword.startswith(query)]
    
    # Sort by length then alphabetically for better UX
    matches.sort(key=lambda x: (len(x), x))
    
    return matches


# Module-level exports
__all__ = ["autocomplete", "TooShortRequestError", "__version__"]
__version__ = "0.1.0"
