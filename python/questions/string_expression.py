"""
Screening (1 hour)
After basic introduction from both the sides, interview started with DSA based question which I had to code on the Hackerrank link which the interviewer shared.

Question - Bracket Expansion

You are given a string expression which consists of several comma separated tokens 
enclosed within opening ('{') and closing ('}') curly braces.
The string expression might or might not have a prefix before opening curly brace('{') and
a suffix after closing curly brace ('}').
You have to return a list of strings as output for each comma separated item as shown below in the examples. 

Example 1: 
Input = "/2022/{jan,feb,march}/report"
Output = "/2022/jan/report"
		 "/2022/feb/report"
		 "/2022/march/report"
		 
Example 2: 
Input = "over{crowd,eager,bold,fond}ness"
Output = "overcrowdness"
		 "overeagerness"
		 "overboldness"
		 "overfondness"
		 
Example 3: 
Input = "read.txt{,.bak}"
Output = "read.txt"
		 "read.txt.bak"
Follow-up

If there are less than 2 tokens enclosed within curly braces or incorrect expression 
(eg. opening and closing braces not present, only opening brace present, 
closing brace present before opening brace etc) return the output same as input

Example 1:
Input: sun{mars}rotation
Output: sun{mars}rotation

Example 2:
Input: minimum{}change
Output: minimum{}change

Example 3 (Incorrect Input):
Input: hello-world
Output: hello-world

Example 4 (Incorrect Input):
Input: hello-{-world
Output: hello-{-world

Example 5 (Incorrect Input):
Input: hello-}-weird-{-world
Output: hello-}-weird-{-world


Leetcode link : https://leetcode.com/discuss/post/5341224/stripe-backend-engineer-bangalore-jun-20-w2jc/

"""

class StringExpression:
    def get_output(self, expression: str) :
        try:
            opening_bracket_index = expression.index("{")
            closing_bracket_index = expression.index("}")
        except:
            return expression
        if opening_bracket_index == -1:
            return expression
        if closing_bracket_index == -1:
            return expression
        
        if opening_bracket_index > closing_bracket_index:
            return expression
        
        substring_between_brackets = expression[opening_bracket_index + 1: closing_bracket_index]
       
        
        substring_between_brackets_tokens = substring_between_brackets.split(",")
        if len(substring_between_brackets_tokens) < 2:
            return expression
        prefx = ""
        suffix = ""
        if opening_bracket_index > 0:
            prefx = expression[0: opening_bracket_index]
        if closing_bracket_index < len(expression) -1:    
            suffix = expression[closing_bracket_index +1:]
        ans = []   
        for token in substring_between_brackets_tokens:
            s = prefx + token + suffix
            ans.append(s)
        return ans
    
def test_get_output():
    service = StringExpression()

    # Test Case 1: Regular case with folder names
    assert service.get_output("/2022/{jan,feb,march}/report") == [
        "/2022/jan/report",
        "/2022/feb/report",
        "/2022/march/report"
    ]

    # Test Case 2: Prefix and suffix wrap the tokens
    assert service.get_output("over{crowd,eager,bold,fond}ness") == [
        "overcrowdness",
        "overeagerness",
        "overboldness",
        "overfondness"
    ]

    # Test Case 3: Empty prefix or suffix
    assert service.get_output("read.txt{,.bak}") == [
        "read.txt",
        "read.txt.bak"
    ]

    # Test Case 4: Only one token in brackets — should return input
    assert service.get_output("sun{mars}rotation") == "sun{mars}rotation"

    # Test Case 5: Empty brackets — should return input
    assert service.get_output("minimum{}change") == "minimum{}change"

    # Test Case 6: No brackets at all — should return input
    assert service.get_output("hello-world") == "hello-world"

    # Test Case 7: Closing brace before opening — should return input
    assert service.get_output("hello-}-weird-{-world") == "hello-}-weird-{-world"

    # Test Case 8: Only opening brace — should return input
    assert service.get_output("hello{-world") == "hello{-world"

    # Test Case 9: Only closing brace — should return input
    assert service.get_output("hello}-world") == "hello}-world"

    # Test Case 10: Multiple token expansion with no prefix or suffix
    assert service.get_output("{a,b,c}") == ["a", "b", "c"]

    # Test Case 11: Leading or trailing commas (should still expand)
    assert service.get_output("abc{,x,y,}z") == ["abcz", "abcxz", "abcyz", "abcz"]

    print("✅ All tests passed.")

if __name__ == "__main__":
    test_get_output()
       
            
        