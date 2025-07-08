"""
Part 1:
You are given a string representing application IDs in the following format:

Each application ID is prefixed by its length (number of characters in the ID).
The format is: lengthOfApplicationId + APPLICATION_ID + ... + 0 (ends with a 0).
Example:
Input: 10A13414124218B124564356434567430
Output: ["A134141242", "B12456435643456743"]

Part 2:
Filter the application IDs obtained from Part 1 to return only the "whitelisted" application IDs.

Example:
Input: 10A13414124218B124564356434567430, ["A134141242"]
Output: ["A134141242"]

Question : https://leetcode.com/discuss/post/6135840/stripe-phone-interview-experience-by-ano-3rgj/

Thing to know : AST Used ast.literal_eval() to safely convert a string like "['A134141242']" into an actual Python list.

"""
import ast
class ParseApplication:
    def parse_apps(self, application_logs: str) -> list:
        application_ids = []
        length = len(application_logs)
        
        i = 0
        while i < length :
            c = application_logs[i]
            if c == "0" and i == length -1:
                return application_ids
            current_app = ""
            current_length = ""
            while c.isdigit():
                current_length += c
                i +=1
                c  = application_logs[i]
            current_length = int(current_length)
            
            current_app = application_logs[i: i + current_length]
            i = i + current_length
            
            application_ids.append(current_app)
            
        return application_ids
    
    def get_white_listed(self, application_logs: str) -> list:
        #print(application_logs.split(","))
        logs, whitelisted_str = application_logs.split(",", 1)
        whitelisted = ast.literal_eval(whitelisted_str)
        
        application_ids = self.parse_apps(logs)
        ans = []
        for id in whitelisted:
            #print(id)
            if id in application_ids:
                ans.append(id)
        return ans        
                
    
def test_parse_apps():
    service = ParseApplication()

    # Test Case 1: Basic example
    input_str = "10A13414124218B124564356434567430"
    expected = ["A134141242", "B12456435643456743"]
    assert service.parse_apps(input_str) == expected

    # Test Case 2: Only one application
    input_str = "8APP123450"
    expected = ["APP12345"]
    assert service.parse_apps(input_str) == expected

    # Test Case 3: Empty string
    input_str = ""
    expected = []
    assert service.parse_apps(input_str) == []

    # Test Case 4: Ends without 0
    input_str = "6ABCDEF"
    expected = ["ABCDEF"]
    assert service.parse_apps(input_str) == expected

    # Test Case 5: Application ID with leading zero length (should not occur normally)
    input_str = "02AB0"
    expected = ["AB"]
    assert service.parse_apps(input_str) == expected

def test_get_white_listed():
    service = ParseApplication()

    # Test Case 1: Basic whitelist filtering
    input_str = "10A13414124218B124564356434567430,['A134141242']"
    expected = ["A134141242"]
    assert service.get_white_listed(input_str) == expected

    # Test Case 2: Whitelist empty
    input_str = "10A13414124218B124564356434567430,[]"
    expected = []
    assert service.get_white_listed(input_str) == expected

    # Test Case 3: Whitelist has IDs not in logs
    input_str = "10A13414124218B124564356434567430,['X123456789']"
    expected = []
    assert service.get_white_listed(input_str) == expected

    # Test Case 4: Multiple whitelist matches
    input_str = "10A13414124218B124564356434567430,['A134141242','B12456435643456743']"
    expected = ['A134141242','B12456435643456743']
    assert service.get_white_listed(input_str) == expected

    # Test Case 5: Malformed string input
    try:
        input_str = "10A13414124218B124564356434567430,'A134141242'"  # Not a list
        service.get_white_listed(input_str)
        assert False  # Should not reach here
    except Exception:
        assert True  # Expected to raise error


if __name__ == "__main__":
    test_parse_apps()
    test_get_white_listed()
    print("All tests passed.")
           
            