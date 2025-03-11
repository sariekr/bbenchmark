import azure.functions as func
import logging
import time  # Add time module for benchmarking
import re  # For User-Agent pattern matching

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.time()  # Start time for benchmark

    logging.info('Python HTTP trigger function processed a request.')

    # Get the User-Agent from the headers
    user_agent = req.headers.get('User-Agent')

    # Perform a check if the User-Agent header exists
    if user_agent:
        logging.info(f"User-Agent: {user_agent}")

        # Define a pattern for modern browsers (this is a simple check, you can expand this)
        pattern = re.compile(r"(Chrome|Firefox|Safari|Edge)/(\d+)\.(\d+)")

        match = pattern.search(user_agent)

        if match:
            browser = match.group(1)
            version = match.group(2)
            logging.info(f"Browser: {browser}, Version: {version}")

            # Check if the browser is up-to-date (for example, checking if version > 90)
            if int(version) >= 90:
                browser_status = f"{browser} is up-to-date."
            else:
                browser_status = f"{browser} version {version} is outdated."
        else:
            browser_status = "Browser not recognized or too old to identify."
    else:
        browser_status = "No User-Agent found."

    # Return the browser status and benchmark results
    end_time = time.time()  # End time for benchmark
    elapsed_time = end_time - start_time  # Calculate elapsed time for benchmark
    logging.info(f"Benchmark completed in {elapsed_time:.4f} seconds.")

    # Generate the response
    return func.HttpResponse(
        f"{browser_status} Benchmark time: {elapsed_time:.4f} seconds.",
        status_code=200
    )
