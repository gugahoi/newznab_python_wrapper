Newznab Python Wrapper
======================

Simple wrapper for NewzNab API calls.

# Usage

    from client import nnapi
    c = nnapi("my_url.com", "my_api_goes_here")
    categories = c.categories()
    c.search("my query")


