"""
Part 1
In an HTTP request, the Accept-Language header describes the list of
languages that the requester would like content to be returned in. The header
takes the form of a comma-separated list of language tags. For example:
Accept-Language: en-US, fr-CA, fr-FR
means that the reader would accept:
1. English as spoken in the United States (most preferred)
2. French as spoken in Canada
3. French as spoken in France (least preferred)
We're writing a server that needs to return content in an acceptable language
for the requester, and we want to make use of this header. Our server doesn't
support every possible language that might be requested (yet!), but there is a
set of languages that we do support. Write a function that receives two arguments:
an Accept-Language header value as a string and a set of supported languages,
and returns the list of language tags that will work for the request. The
language tags should be returned in descending order of preference (the
same order as they appeared in the header).
In addition to writing this function, you should use tests to demonstrate that it's
correct, either via an existing testing system or one you create.
Examples:
parseacceptlanguage(
"en-US, fr-CA, fr-FR", # the client's Accept-Language header, a string
["fr-FR", "en-US"] # the server's supported languages, a set of strings
)
returns: ["en-US", "fr-FR"]
parseacceptlanguage("fr-CA, fr-FR", ["en-US", "fr-FR"])
returns: ["fr-FR"]
parseacceptlanguage("en-US", ["en-US", "fr-CA"])
returns: ["en-US"]***

"""
from collections import defaultdict
class HttpHeaders:
    def parse_headers(self, user_header: str, server_support: list[str]) -> list[str]:
        if not user_header or not user_header.strip():
            return []
        
        user_header_tokens = user_header.split(",")
        user_languages = {}
        rank = 0
        languages_to_return = []
        for token in user_header_tokens:
            if not token:
                continue
            token = token.strip()
            user_languages[token] = rank
            rank += 1
        for language in server_support:
            if language in user_languages:
                rank = user_languages[language]
                languages_to_return.append({
                   "language": language,
                   "rank": rank
               })
        
        languages_to_return = sorted(languages_to_return, key=lambda p: p["rank"])
        ans = []
        
        for language in languages_to_return:
            ans.append(language["language"])
        return ans    
    
if __name__ == "__main__":
     
    service = HttpHeaders()

    print(service.parse_headers("en-US", ["en-US", "fr-CA"]))
    # → ["en-US"]

    print(service.parse_headers("en-US, fr-CA", ["en-US", "fr-CA"]))
    # → ["en-US", "fr-CA"]

    print(service.parse_headers("fr-CA, fr-FR", ["en-US", "fr-FR"]))
    # → ["fr-FR"]

    print(service.parse_headers("en-US, fr-CA, fr-FR", ["fr-FR", "en-US"]))

                    