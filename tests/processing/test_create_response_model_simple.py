from ast import literal_eval
from curl2swift.processing.create_response_model import create_response_model

RESPONSE_JSON = """
{
  "Markets": [
    {
      "Code": "ar",
      "Locale": "ar-EG",
      "Name": "Ø§Ù„Ø¹Ø±Ø¨ÙŠØ© (Ù…ØµØ±)",
      "Language": "Ø§Ù„Ø¹Ø±Ø¨ÙŠØ©",
      "Country": "Ù…ØµØ±",
      "Currency": "EGP",
      "SocialNetworks": [],
      "Enabled": False,
      "Configuration": {
          "EverythingOnSale": True
      }
    },
    {
      "Code": "az",
      "Locale": "az-AZ",
      "Name": "AzÉ™rbaycan dili (AzÉ™rbaycan)",
      "Language": "AzÉ™rbaycan dili",
      "Country": "Azerbaijan",
      "Currency": "AZN",
      "SocialNetworks": [],
      "Enabled": True,
      "Object": {
          "EverythingOnSale": False
      }
    }
  ]
}
""".strip()

EXPECTED_RESULT = """
    struct Response: Codable {
        let markets : [Market]?

        enum CodingKeys: String, CodingKey {
            case markets = "Markets"
        }
    }

    struct Market: Codable {
        let code : String?
        let locale : String?
        let name : String?
        let language : String?
        let country : String?
        let currency : String?
        let socialNetworks : [Any]?
        let enabled : Bool?
        let configuration : Configuration?

        enum CodingKeys: String, CodingKey {
            case code = "Code"
            case locale = "Locale"
            case name = "Name"
            case language = "Language"
            case country = "Country"
            case currency = "Currency"
            case socialNetworks = "SocialNetworks"
            case enabled = "Enabled"
            case configuration = "Configuration"
        }
    }

    struct Configuration: Codable {
        let everythingOnSale : Bool?

        enum CodingKeys: String, CodingKey {
            case everythingOnSale = "EverythingOnSale"
        }
    }
"""

def test_create_response_model():
    json_dict = literal_eval(RESPONSE_JSON)
    response_model = create_response_model(json_dict)
    assert response_model.strip() == EXPECTED_RESULT.strip()
