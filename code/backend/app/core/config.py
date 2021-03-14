from personal_data import PersonalData

class Settings:
    API_V1_STR: str = "/api/v1"
    HEADERS: dict = {
        "accept": "application/json",
        "Client-Id": PersonalData.OZON_AUTH["Client-Id"],
        "Api-Key": PersonalData.OZON_AUTH["Api-Key"],
        "Content-Type": "application/json"
    }
