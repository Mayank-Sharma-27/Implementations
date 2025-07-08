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
       
            
        