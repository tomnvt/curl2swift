CODABLE_TEMPLATE = """
    struct <MODEL_NAME>: Codable {
        <PROPERTIES>

        enum CodingKeys: String, CodingKey {
            <CODING_KEYS>
        }
    }
"""