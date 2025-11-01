# LuauSense

A Python library providing intelligent autocompletion for Luau scripting language keywords and built-in functions.

## Features

- Fast, case-sensitive autocompletion for Luau keywords and functions
- Input validation with meaningful error messages
- Zero external dependencies
- Fully typed for better IDE support

## Installation

```bash
pip install luausense
```

## Usage

```python
import luausense

# Get autocomplete suggestions
try:
    suggestions = luausense.autocomplete("pri")
    print(suggestions)  # ['print', 'private']
except luausense.TooShortRequestError:
    print("Input too short - minimum 2 characters required")
```

## API

autocomplete(query: str) -> List[str]

Returns a list of Luau keywords and built-in functions that start with the given query.

· query: String to autocomplete (minimum 2 characters)
· Returns: List of matching Luau identifiers
· Raises: TooShortRequestError if query length < 2

## License

Apache-2.0
