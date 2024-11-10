from googleapiclient.discovery import build
from functools import lru_cache
import yfinance


def authenticate_api(api_key: int) -> 'CustomSearchEngine' | None: # type: ignore
    """Authenticates the Google Custom Search API."""
    service = build("customsearch", "v1", developerKey=api_key)
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        return service.cse()
    except Exception as e:
        print(f"Error authenticating API: {e}")
        return None

@lru_cache(maxsize=256)
def google_search() -> list[dict]| None:
    """
        Generates the articles according to the stock ticker, the dateRestriction, number of articles
        Uses the custom search engine created by GoogleAPI
    """
    service = authenticate_api(input_result("What is your API key? "))
    search_engine_id = "x"
    if not service:
        return []
    stock_ticker = input_result("What stock ticker would you like to search up?: ")
    search_engine = service.list(
        cx=search_engine_id,
        q=f"g{stock_ticker} stock analysis",
        dateRestrict=input_result("How many days before today would you like to look at? -> dateRestrict (answer as an integer): "),
        sort="date",
        num=input_result("What is the number of articles would you like analyzed? (answer as an integer): "),
        start=1
    )
    try:
        response = search_engine.execute()
        return response["items"]
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return []
    
def input_result(question) -> int | str:
    """
        Input function with error handling :0
        Validates date range, number of articles
    """
    while True:
        response = input(question)

        # Validate date range
        if "dateRestrict" in question:
            try:
                int_response = int(response)
                if int_response <= 0:
                    raise ValueError
                return int_response
            except ValueError:
                print("Please enter a positive integer for the date range.")

        # Validate number of articles
        elif "number of articles" in question:
            try:
                int_response = int(response)
                if int_response <= 0:
                    raise ValueError
                return int_response
            except ValueError:
                print("Please enter a positive integer for the number of articles.")

        # For other inputs, return directly
        else:
            if is_valid_ticker(response):
                return response
            else:
                print(f"Ticker - {response}, is not a valid ticker symbol.")
                
        
def is_valid_ticker(ticker):
  try:
    yfinance.Ticker(ticker).info
    return True
  except Exception as e:
    print(f"Error fetching ticker info: {e}")
    return False
    