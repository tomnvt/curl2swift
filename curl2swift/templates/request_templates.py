QUERY_PARAM_SETTER = """
    @discardableResult
    func setQueryParam(_ key: QueryParam, _ value: String) -> Self {
        queryParams[key.rawValue] = value
        return self
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

    enum QueryParam: String {
        <QUERY_PARAMS>
    }

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
                  queryParams: [String: String] = [:],
                  method: HTTPMethod = .get,
                  headers: [String: String] = [:],
                  params: [String: Any] = [:]) {
        super.init(baseURL: baseURL, path: path, method: method, headers: headers, params: params)
        set(.path("<PATH>"))
        <QUERY_PARAMS_INIT>
        set(.method(<METHOD>))
    }
}

extension <REQUEST_NAME>Request {

    <QUERY_PARAM_SETTER>

    <PATH_PARAM_SETTER>

    <HEADER_PARAM_SETTER>

    <BODY_PARAM_SETTER>
}
"""
