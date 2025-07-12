import re
from typing import Any, Dict, List, Union
from urllib.parse import unquote
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class QueryParserMiddleware(BaseHTTPMiddleware):
    """
    Middleware that parses complex query parameters into a flat dictionary format.

    Converts URLs like:
    ?search%5Bsearch%5D=term&search%5BuserShowStatus%3Ain%5D%5B%5D=planned&search%5BuserShowStatus%3Ain%5D%5B%5D=

    Into a flat structure like:
    {
        "search": "term",
        "userShowStatus:in": ["planned", None]  # Empty values become None
    }
    """

    async def dispatch(self, request: Request, call_next):
        # Parse query parameters into a nested structure
        parsed_params = self._parse_query_params(request.query_params)

        # Add the parsed parameters to the request state
        request.state.parsed_query_params = parsed_params

        response = await call_next(request)
        return response

    def _parse_query_params(self, query_params) -> Dict[str, Any]:
        """
        Parse query parameters into a nested dictionary structure.

        Args:
            query_params: FastAPI QueryParams object

        Returns:
            Dict with nested structure based on parameter names
        """
        result = {}

        for key, value in query_params.multi_items():
            # URL decode the key and value
            decoded_key = unquote(key)
            decoded_value = unquote(value) if value else None

            # Parse the key structure (including None values for empty parameters)
            self._set_nested_value(result, decoded_key, decoded_value)

        return result

    def _set_nested_value(self, result: Dict[str, Any], key: str, value: Union[str, None]) -> None:
        """
        Set a value in a nested dictionary based on the key structure.

        Examples:
        - "search[search]" -> result["search"] = value (or None if empty)
        - "search[userShowStatus:in][]" -> result["userShowStatus:in"] = [value] (includes None for empty values)
        - "filter[category]" -> result["category"] = value (or None if empty)
        - "page" -> result["page"] = value (or None if empty)
        """
        # Pattern to match nested keys like "search[search]" or "search[userShowStatus:in][]"
        pattern = r"^[^[]+\[([^\]]*)\](\[\])?$"
        match = re.match(pattern, key)

        if match:
            # Extract the inner key from brackets
            inner_key = match.group(1)
            is_array = match.group(2) == "[]"

            # Handle array values
            if is_array:
                if inner_key not in result:
                    result[inner_key] = []
                result[inner_key].append(value)  # This will include None values
            else:
                result[inner_key] = value  # This will be None for empty values
        else:
            # Simple key-value pair
            result[key] = value  # This will be None for empty values

    def get_parsed_params(self, request: Request) -> Dict[str, Any]:
        """
        Helper method to get parsed parameters from request state.

        Args:
            request: FastAPI Request object

        Returns:
            Parsed query parameters dictionary
        """
        return getattr(request.state, "parsed_query_params", {})


def get_parsed_query_params(request: Request) -> Dict[str, Any]:
    """
    Utility function to get parsed query parameters from request.

    Args:
        request: FastAPI Request object

    Returns:
        Parsed query parameters dictionary
    """
    return getattr(request.state, "parsed_query_params", {})
