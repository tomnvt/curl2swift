TEST_TEMPLATE = """
    func test<REQUEST_NAME>Request() {
        let expectation = XCTestExpectation(description: "waiting for reponse")
        let builder = <REQUEST_NAME>Request()
            .set(.baseURL("<URL>"))
            .set(.path("<PATH>"))
            <HEADER_SETTERS>
            <BODY_PARAM_SETTERS>
            .rx
            .makeRequest()
            .mapTo(<REQUEST_NAME>Request.Response.self)
            .do(onSuccess: { _ in expectation.fulfill() },
                onError: { _ in XCTFail("The request should succeed") })
            .discardableSubscribe()
        wait(for: [expectation], timeout: 10)
    }
"""

PATH_PARAM_SETTER = \
    """@discardableResult
    func setPathParameter(_ param: PathParameter, _ value: String) -> Self {
        let placeholder = "{" + param.rawValue + "}"
        path = path.replacingOccurrences(of: placeholder, with: value)
        return self
    }"""

HEADER_PARAM_SETTER = \
    """@discardableResult
    func setHeader(_ key: Header, _ value: String) -> Self {
        headers[key.rawValue] = value
        return self
    }
    """

BODY_PARAM_SETTER = \
    """@discardableResult
    func setBodyParameter(_ key: BodyParameter, _ value: String) -> Self {
        params[key.rawValue] = value
        return self
    }"""

REQUEST_TEMPLATE = """
/// <DESC>
class <REQUEST_NAME>Request: RequestSpecBuilder {

    <RESPONSE>

    enum PathParameter: String {
        <PATH_PARAMS>
    }

    enum Header: String {
        <HEADERS>
    }

    enum BodyParameter: String {
        <BODY_PARAMS>
    }

    required init(baseURL: String = "",
                  path: String = "",
                  method: HTTPMethod = .get,
                  headers: [String: String] = [:],
                  params: [String: String] = [:]) {
        super.init(baseURL: baseURL, path: path, method: method, headers: headers, params: params)
        set(.path("<PATH>"))
        set(.method(<METHOD>))
    }
}

extension <REQUEST_NAME>Request {

    <PATH_PARAM_SETTER>

    <HEADER_PARAM_SETTER>

    <BODY_PARAM_SETTER>
}
"""

CODABLE_TEMPLATE = """
    struct Response: Codable {
        <PROPERTIES>

        enum CodingKeys: String, CodingKey {
            <CODING_KEYS>
        }
    }
"""
