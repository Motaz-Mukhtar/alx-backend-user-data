#!/usr/bin/env python

if __name__ == "__main__":
    from api.v1.auth.auth import Auth

    a = Auth()
    path = "/api/v1/us"
    paths_excluded = ["/api/v1/us*"]
    print(a.require_auth(path, paths_excluded))

    print(a.require_auth("/api/v1/users", ["/api/v1/stat*"]))

    print(a.require_auth("/api/v1/status", ["/api/v1/stat*"]))

    print(a.require_auth("/api/v1/stats", ["/api/v1/stat*"]))
