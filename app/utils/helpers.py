def infer_title_from_query(query: str, max_length: int = 30) -> str:
    """
    Infer a session title from a user query.
    
    Args:
        query: The user's query
        max_length: Maximum length of the title
        
    Returns:
        A title for the session derived from the query
    """
    # Remove whitespace for a cleaner title
    query = query.strip()
    
    # If the query is short enough, use it directly
    if len(query) <= max_length:
        return query
    
    # Otherwise, truncate it and add ellipsis
    return query[:max_length-3] + "..."