from rest_framework.parsers import JSONParser


class VndJsonParser(JSONParser):
    media_type = "application/vnd.api+json"
