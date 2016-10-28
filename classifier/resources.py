import requests
from flask import current_app
from flask_jwt import jwt_required
from flask_restful import Resource

import reqparsers
from helpers import process_web_page
from classifier.extensions import clf


class QueryResource(Resource):
    @jwt_required()
    def get(self):
        args = reqparsers.url_parser.parse_args()

        headers = {
            "User-Agent": current_app.config["USER_AGENT"]
        }

        response = requests.get(
            args.url,
            verify=current_app.config["VERIFY_SSL"],
            timeout=current_app.config["REQUEST_TIMEOUT"],
            headers=headers
        )

        if response.status_code != 200:
            return {
                "error": "invalid response status code",
                "status_code": response.status_code,
                "url": args.url
            }

        contents = process_web_page(response.text)

        classification_response = clf.classify(contents)

        return {
            "url": args.url,
            "result": classification_response,
            "status_code": response.status_code
        }

    @jwt_required()
    def post(self):
        args = reqparsers.classification_request.parse_args()

        contents = process_web_page(args.content)

        classification_response = clf.classify(contents)

        return {
            "result": classification_response
        }