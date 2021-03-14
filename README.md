# curl2swift

`curl2swift` is a command line tool for transforming a cURL request to Swift code. 
It takes a cURL and generates code for the request, the request's response mapping and a test. 

Note that the generated code is not yet intended for general usage, 
because it depends on some code that is specific to the project for which this tool was initially designed.

### TODOs
- Implement template configuration and customization.
- Try out various cURLs to add handling for unexpected arguments.
- Add configuration options for specifying output file. 
- Enable path param specification (e.g. using {...} to denote a path param placeholder.)

### USAGE
1. Copy a cURL into the clipboard.
2. Call `curl2swift` and pass a request name, e.g. `curl2swift TestRequest`.
3. Processed request template is printed out with a promt if user wants to copy it.
4. Processed test template is printed out with the same promt.

### OUTPUT EXAMPLE
After step 3:
```
/// Add docs
class TestRequest: RequestSpecBuilder {

    
    struct Response: Codable {
        let login : String?
        let id : Int?
        let nodeNode : String?
        let avatarAvatar : String?
        let gravatarGravatar : String?
        let url : String?
        let htmlHtml : String?
        let followersFollowers : String?
        let followingFollowing : String?
        let gistsGists : String?
        let starredStarred : String?
        let subscriptionsSubscriptions : String?
        let organizationsOrganizations : String?
        let reposRepos : String?
        let eventsEvents : String?
        let receivedReceived : String?
        let type : String?
        let siteSite : Bool?
        let name : String?
        let company : String?
        let blog : String?
        let location : String?
        let email : String?
        let hireable : String?
        let bio : String?
        let twitterTwitter : String?
        let publicPublic : Int?
        let publicPublic : Int?
        let followers : Int?
        let following : Int?
        let createdCreated : String?
        let updatedUpdated : String?

        enum CodingKeys: String, CodingKey {
            case login = "login"
            case id = "id"
            case nodeNode = "node_id"
            case avatarAvatar = "avatar_url"
            case gravatarGravatar = "gravatar_id"
            case url = "url"
            case htmlHtml = "html_url"
            case followersFollowers = "followers_url"
            case followingFollowing = "following_url"
            case gistsGists = "gists_url"
            case starredStarred = "starred_url"
            case subscriptionsSubscriptions = "subscriptions_url"
            case organizationsOrganizations = "organizations_url"
            case reposRepos = "repos_url"
            case eventsEvents = "events_url"
            case receivedReceived = "received_events_url"
            case type = "type"
            case siteSite = "site_admin"
            case name = "name"
            case company = "company"
            case blog = "blog"
            case location = "location"
            case email = "email"
            case hireable = "hireable"
            case bio = "bio"
            case twitterTwitter = "twitter_username"
            case publicPublic = "public_repos"
            case publicPublic = "public_gists"
            case followers = "followers"
            case following = "following"
            case createdCreated = "created_at"
            case updatedUpdated = "updated_at"
        }
    }


    required init(baseURL: String = "",
                  path: String = "",
                  method: HTTPMethod = .get,
                  headers: [String: String] = [:],
                  params: [String: String] = [:]) {
        super.init(baseURL: baseURL, path: path, method: method, headers: headers, params: params)
        set(.path("/users/defunkt"))
        set(.method(.get))
    }
}

extension TestRequest {
}


- - - - - - - - - - - - 
END OF GENERATED OUTPUT
- - - - - - - - - - - - 

Copy output to clipboard? [y/n]
```

Note that the extension contains setters for headers and body paramaeters, if the request has any.

After step 4:
```
- - - - - - - - 
GENERATED TEST:
- - - - - - - - 

    func testTestRequest() {
        let expectation = XCTestExpectation(description: "waiting for reponse")
        let builder = TestRequest()
            .set(.baseURL("https://api.github.com"))
            .set(.path("/users/defunkt"))
            .rx
            .makeRequest()
            .mapTo(TestRequest.Response.self)
            .do(onSuccess: { _ in expectation.fulfill() })
            .discardableSubscribe()
        wait(for: [expectation], timeout: 10)
    }


- - - - - - - - - - - - 
END OF GENERATED OUTPUT
- - - - - - - - - - - - 

Copy to clipboard? [y/n]
```