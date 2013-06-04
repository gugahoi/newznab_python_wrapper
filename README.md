Newznab Python Wrapper
======================

Simple wrapper for NewzNab API calls.

# Usage

    from client import wrapper
    c = wrapper("my_url.com", "my_api_goes_here")
    categories = c.categories()
    c.search(q="my query", maxage="20")


