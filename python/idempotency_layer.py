from collections import defaultdict

class IdempotentLayer:
    def parse_logs(self, logs: str) -> dict:
        if not logs:
            return ValueError("Invalid input")
        logs_token = logs.strip().split("~")
        if not logs_token:
           return ValueError("Invalid input") 
       
        idempotency_key_info = defaultdict(list)
        request_id_mapping = {}
        for token in logs_token:
            timestamp, request_id, idempotency_key, payout_details = token.split(";")
            idempotency_key_info[idempotency_key].append({
                "timestamp": timestamp,
                "payout_details": payout_details,
                "request_id": request_id
            })
            request_id_mapping[request_id] = idempotency_key
        
        return idempotency_key_info , request_id_mapping
    
    def detect_duplicates(self, logs: str) -> list:
        idempotency_key_info, request_id_mapping = self.parse_logs(logs)
        duplicates = set()
        
        for requests in idempotency_key_info.values():
            requests= requests[1:]
            
            for request in requests:
                
                request_id = request["request_id"]
                
                duplicates.add(request_id)
        
        return duplicates
    
    def get_mapping(self, logs: str) -> dict:
        idempotency_key_info, request_id_mapping = self.parse_logs(logs)
        mappings = {}
        
        for request_id, itempotent_key in request_id_mapping.items():
            if idempotency_key_info[itempotent_key][0]["request_id"] != request_id:
               mappings[request_id] = "DUPLICATE" 
            else:
               mappings[request_id] = "SUCCEEDED" 
                          
        return mappings          
if __name__ == "__main__":
                             
    # --- Test Data for Parts 1 & 2 ---
    log_p1_p2 = (
        "2025-08-01T10:00:00Z;req_A;key_1;account=acct_A&amount=1000~"
        "2025-08-01T10:01:00Z;req_B;key_2;account=acct_B&amount=2000~"
        "2025-08-01T10:02:00Z;req_C;key_1;account=acct_A&amount=1000"
    )

    # --- Test Data for Part 3 ---
    log_p3 = (
        "2025-08-01T10:00:00Z;received;req_X1;key_X;details...~"
        "2025-08-01T10:01:00Z;processing_started;req_X1;key_X;...~"
        "2025-08-01T10:02:00Z;received;req_X2;key_X;...~"  # Should be IN_FLIGHT
        "2025-08-01T10:03:00Z;processing_finished;req_X1;key_X;...~"
        "2025-08-01T10:04:00Z;received;req_X3;key_X;..."   # Should be DUPLICATE
    )

    # --- Test Data for Part 4 ---
    log_p4 = (
        "2025-08-01T10:00:00Z;received;req_Z1;key_Z;account=acct_Z&amount=1000~"
        "2025-08-01T10:01:00Z;processing_finished;req_Z1;key_Z;...~"
        "2025-08-01T10:02:00Z;received;req_Z2;key_Z;account=acct_Z&amount=9999~" # Should be MISMATCHED_REQUEST
        "2025-08-01T10:03:00Z;received;req_Z3;key_Z;account=acct_Z&amount=1000"  # Should be DUPLICATE
    )

    # Instantiate your solution class
    service = IdempotentLayer() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Simple Duplicate Detection ##")
    # Expected: ['req_C']
    print(service.detect_duplicates(log_p1_p2))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Caching Original Responses ##")
    # Expected: {'req_A': 'SUCCEEDED', 'req_B': 'SUCCEEDED', 'req_C': 'DUPLICATE'}
    print(service.get_mapping(log_p1_p2))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Handling In-Flight Requests ##")
    # Expected: {'req_X1': 'SUCCEEDED', 'req_X2': 'IN_FLIGHT', 'req_X3': 'DUPLICATE'}
    # print(service.get_outcomes_with_inflight(log_p3))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Validating Request Consistency ##")
    # Expected: {'req_Z1': 'SUCCEEDED', 'req_Z2': 'MISMATCHED_REQUEST', 'req_Z3': 'DUPLICATE'}
    # print(service.get_final_outcomes(log_p4))
    print("-" * 50)