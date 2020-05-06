import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ratingId = req.params.get('ratingId')
    if not ratingId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ratingId = req_body.get('ratingId')
    
    # Lookup in the DB and return

    if ratingId:
        return func.HttpResponse(f"Hello, {ratingId}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a ratingId in the query string or in the request body for a personalized response.",
             status_code=200
        )
