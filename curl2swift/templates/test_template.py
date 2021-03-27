TEST_TEMPLATE = """
    func test<REQUEST_NAME>Request() {
        let expectation = XCTestExpectation(description: "waiting for reponse")
        <REQUEST_NAME>Request()
            .set(.baseURL("<URL>"))
            .set(.path("<PATH>"))
            <HEADER_SETTERS>
            <BODY_PARAM_SETTERS>
            .makeRxRequest()
            .mapTo(<REQUEST_NAME>Request.Response.self)
            .do(onSuccess: { _ in expectation.fulfill() },
                onError: { _ in XCTFail("The request should succeed") })
            .discardableSubscribe()
        wait(for: [expectation], timeout: 10)
    }
"""
