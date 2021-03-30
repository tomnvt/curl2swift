from ast import literal_eval
from curl2swift.processing.create_response_model import create_response_model

RESPONSE_JSON = """
{
  "coord": {
    "lon": 14.4208,
    "lat": 50.088
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01n"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 13.48,
    "feels_like": 11.15,
    "temp_min": 11.67,
    "temp_max": 15.56,
    "pressure": 1028,
    "humidity": 47
  },
  "visibility": 10000,
  "wind": {
    "speed": 1.03,
    "deg": 120
  },
  "clouds": {
    "all": 0
  },
  "dt": 1617135901,
  "sys": {
    "type": 1,
    "id": 6835,
    "country": "CZ",
    "sunrise": 1617079382,
    "sunset": 1617125412
  },
  "timezone": 7200,
  "id": 3067696,
  "name": "Prague",
  "cod": 200
}
""".strip()

EXPECTED_RESULT = """
    struct Response: Codable {
        let coord : Coord?
        let weather : [Weather]?
        let base : String?
        let main : Main?
        let visibility : Int?
        let wind : Wind?
        let clouds : Clouds?
        let dt : Int?
        let sys : Sys?
        let timezone : Int?
        let id : Int?
        let name : String?
        let cod : Int?

        enum CodingKeys: String, CodingKey {
            case coord = "coord"
            case weather = "weather"
            case base = "base"
            case main = "main"
            case visibility = "visibility"
            case wind = "wind"
            case clouds = "clouds"
            case dt = "dt"
            case sys = "sys"
            case timezone = "timezone"
            case id = "id"
            case name = "name"
            case cod = "cod"
        }
    }

    struct Sys: Codable {
        let type : Int?
        let id : Int?
        let country : String?
        let sunrise : Int?
        let sunset : Int?

        enum CodingKeys: String, CodingKey {
            case type = "type"
            case id = "id"
            case country = "country"
            case sunrise = "sunrise"
            case sunset = "sunset"
        }
    }

    struct Clouds: Codable {
        let all : Int?

        enum CodingKeys: String, CodingKey {
            case all = "all"
        }
    }

    struct Wind: Codable {
        let speed : Double?
        let deg : Int?

        enum CodingKeys: String, CodingKey {
            case speed = "speed"
            case deg = "deg"
        }
    }

    struct Main: Codable {
        let temp : Double?
        let feelsLike : Double?
        let tempMin : Double?
        let tempMax : Double?
        let pressure : Int?
        let humidity : Int?

        enum CodingKeys: String, CodingKey {
            case temp = "temp"
            case feelsLike = "feels_like"
            case tempMin = "temp_min"
            case tempMax = "temp_max"
            case pressure = "pressure"
            case humidity = "humidity"
        }
    }

    struct Weather: Codable {
        let id : Int?
        let main : String?
        let description : String?
        let icon : String?

        enum CodingKeys: String, CodingKey {
            case id = "id"
            case main = "main"
            case description = "description"
            case icon = "icon"
        }
    }

    struct Coord: Codable {
        let lon : Double?
        let lat : Double?

        enum CodingKeys: String, CodingKey {
            case lon = "lon"
            case lat = "lat"
        }
    }
"""

def test_create_response_model():
    json_dict = literal_eval(RESPONSE_JSON)
    response_model = create_response_model(json_dict)
    assert response_model.strip() == EXPECTED_RESULT.strip()
