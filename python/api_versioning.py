"""
Problem: API Version Negotiator
Stripe supports multiple versions of its API and allows clients to specify preferred versions via a custom HTTP header:

yaml
Copy
Edit
X-Stripe-Version: 2022-08-01, latest, 2022-11-01
However, real-world clients might:

Misformat version tags

Use aliases like latest or stable

Have overlapping preferences

You need to write a server-side processor that:

Parses this header

Cleans it

Resolves aliases

Returns the best set of supported versions in correct preference order

🔧 Input Format:
A string header like:
"X-Stripe-Version: 2022-08-01, latest , 2023-01-01 ,stable"

A set of supported versions:
{"2022-08-01", "2022-11-01", "2023-01-01"}

An alias map (dict):

python
Copy
Edit
{
  "latest": "2023-01-01",
  "stable": "2022-11-01"
}
🔍 Part 1: parse_version_header(header: str) -> List[str]
Extract and normalize the version list from the header string.

Input: "X-Stripe-Version: 2022-08-01, latest ,2023-01-01, stable"
Output: ["2022-08-01", "latest", "2023-01-01", "stable"]

🔍 Part 2: resolve_aliases(versions: List[str], alias_map: Dict[str, str]) -> List[str]
Replace all alias versions (latest, stable, etc.) with their actual versions using the alias map.

Input: ["2022-08-01", "latest", "2023-01-01", "stable"]
Output: ["2022-08-01", "2023-01-01", "2023-01-01", "2022-11-01"]

🔍 Part 3: get_supported_versions(versions: List[str], supported_versions: Set[str]) -> List[str]
Return only those versions that are present in the supported list, preserving input order and removing duplicates.

Input:

python
Copy
Edit
["2022-08-01", "2023-01-01", "2023-01-01", "2022-11-01"]
{"2022-08-01", "2022-11-01", "2023-01-01"}
Output: ["2022-08-01", "2023-01-01", "2022-11-01"]

🔍 Part 4: negotiate_version(header: str, supported_versions: Set[str], alias_map: Dict[str, str]) -> List[str]
End-to-end pipeline. Given the raw header string, return the final list of accepted versions.

Input:

python
Copy
Edit
header = "X-Stripe-Version: 2022-08-01, latest ,2023-01-01, stable"
supported_versions = {"2022-08-01", "2022-11-01", "2023-01-01"}
alias_map = {"latest": "2023-01-01", "stable": "2022-11-01"}
Output:
["2022-08-01", "2023-01-01", "2022-11-01"]


"""
class ApiVersioning:
    def parse_version_header(self, header: str) -> list[str]:
        header_tokens = header.split(":")
        version_tokens = header_tokens[1].split(",")
        
        ans = []
        for token in version_tokens:
            ans.append(token.strip())
        
        return ans
    
    def resolve_aliases(self, versions: list[str], alias_map : dict) -> list[str]:
        ans =[]
        for version in versions:
            if version in {"latest", "stable"}:
               ans.append(alias_map.get(version))
            else:
                ans.append(version)
        
        return ans            
                
    def get_supported_versions(self, versions: list[str], supported_version: set) -> list[str]:
        ans = set()
        for version in versions:
            if version not in supported_version:
                continue
            else:
                ans.add(version)
                
        return list(ans)
    
    def negotiate_version(self, header: str, supported_versions: set, alias_map: dict) -> list[str]:
        header_versions = self.parse_version_header(header) 
        
        ans = set()
        for header_version in header_versions:
            if header_version in {"latest", "stable"}:
                ans.add(alias_map.get(header_version))  
            elif header_version in supported_versions:
                ans.add(header_version)                 
        return list(ans)
    
if __name__ == "__main__":
    header = "X-Stripe-Version: 2022-08-01, latest ,2023-01-01, stable"
    supported_versions = {"2022-08-01", "2022-11-01", "2023-01-01"}
    alias_map = {
        "latest": "2023-01-01",
        "stable": "2022-11-01"
    }         
    apiVersioning = ApiVersioning()

    print("=== Part 1: Parsed Header ===")
    parsed = apiVersioning.parse_version_header(header)
    print(parsed)  # ["2022-08-01", "latest", "2023-01-01", "stable"]

    print("\n=== Part 2: After Alias Resolution ===")
    resolved = apiVersioning.resolve_aliases(parsed, alias_map)
    print(resolved)  # ["2022-08-01", "2023-01-01", "2023-01-01", "2022-11-01"]

    print("\n=== Part 3: Supported Versions Only ===")
    filtered = apiVersioning.get_supported_versions(resolved, supported_versions)
    print(filtered)  # ["2022-08-01", "2023-01-01", "2022-11-01"]

    print("\n=== Part 4: Full Version Negotiation ===")
    result = apiVersioning.negotiate_version(header, supported_versions, alias_map)
    print(result)  