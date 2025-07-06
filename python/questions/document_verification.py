from collections import defaultdict
class DocumentVerification:
    def parse_evets(self, logs: str) -> dict:
        events = []
        
        logs_tokens = logs.split("&")
        for log in logs_tokens:
            time, company_id, doc_id, status, doc_type = log.split(";")
            doc_type = doc_type.split("=")[1].strip()
            events.append({
                "time": time,
                "company_id" : company_id,
                "doc_id": doc_id,
                "status": status,
                "doc_type": doc_type
            }) 
        events = sorted(events, key=lambda e: e["time"])
        company_info = {}
        doc_status = {}
        company_application_status = {}
        
        for event in events:
            doc_type = event["doc_type"]
            company_id = event["company_id"]
            doc_id = event["doc_id"]
            status = event["status"]
            if company_info.get(company_id) is None:
                company_info[company_id] = {}
            if company_info[company_id].get(doc_type) is None:
               company_info[company_id][doc_type] = []
            company_info[company_id][doc_type].append({
                "time": time,
                "doc_id": doc_id,
                "status": status,
                "doc_type": doc_type
               })
            
            doc_status[doc_id] = status
        
               
        return {"company_info": company_info, "doc_status": doc_status}
    
    def get_doc_status(self, logs: str) -> dict:
        info = self.parse_evets(logs)
        return info["doc_status"] 
    
    def get_company_application_status(self, logs: str, required_docs :list[str]) -> dict:
        info = self.parse_evets(logs)
        company_info = info["company_info"]
        
        company_status = {}
        
            
        for company_id in company_info.keys():
            
            number_of_doc_complete = 0
            company_status[company_id] = ""
            missing_document = False
            for reqquired_doc in required_docs:
                #print(company_info[company_id])
                if company_info[company_id].get(reqquired_doc) is None:
                   missing_document = True
                   break
                    
                last_event_len = len(company_info[company_id][reqquired_doc]) -1
                if company_info[company_id][reqquired_doc][last_event_len]["status"]  == "VERIFICATION_PASSED":
                    number_of_doc_complete += 1
                   
            if number_of_doc_complete == 2:
                company_status[company_id] = "COMPLETE"
            elif missing_document:
                company_status[company_id] = "PENDING"
            else:
                company_status[company_id] = "ACTION_REQUIRED"
                    
        return company_status        
    
    def get_pending_documents(self, logs: str, required_docs :list[str]) -> dict:
        info = self.parse_evets(logs) 
        company_info = info["company_info"]
        company_pending_documents = defaultdict(list)
        for reqquired_doc in required_docs:
            for company_id in company_info.keys():
                if company_info[company_id].get(reqquired_doc) is None:
                   company_pending_documents[company_id].append({
                       "document": reqquired_doc,
                       "status": "MISSING"
                   })
                elif company_info[company_id][reqquired_doc][len(company_info[company_id][reqquired_doc]) -1] == "VERIFICATION_PASSED":
                    company_pending_documents[company_id].append({
                       "document": reqquired_doc,
                       "status": "VERIFICATION_PASSED"
                   })
                else:
                    company_pending_documents[company_id].append({
                       "document": reqquired_doc,
                       "status": "UPLOADED"
                   })
                    
        return company_pending_documents
    
    def get_detailed_breakdown(self, logs: str, required_docs :list[str])  -> dict:
        info = self.parse_evets(logs) 
        company_info = info["company_info"]
        
        company_status = self.get_company_application_status(logs, required_docs)
        summary = {}
        return {"company_info": company_info, "company_status": company_status}
                 
if __name__ == "__main__":
    # --- Test Data ---
    required_docs = ["articles_of_incorporation", "founder_agreement"]
    
    event_log = (
        # Company A: Will be COMPLETE
        "2025-02-01T10:00:00Z;comp_A;doc_1;DOC_UPLOADED;doc_type=articles_of_incorporation&"
        "2025-02-02T11:00:00Z;comp_A;doc_1;VERIFICATION_PASSED;doc_type=articles_of_incorporation&"
        "2025-02-03T09:00:00Z;comp_A;doc_2;DOC_UPLOADED;doc_type=founder_agreement&"
        "2025-02-04T14:00:00Z;comp_A;doc_2;VERIFICATION_PASSED;doc_type=founder_agreement&"

        # Company B: Will be ACTION_REQUIRED
        "2025-02-01T11:00:00Z;comp_B;doc_3;DOC_UPLOADED;doc_type=articles_of_incorporation&"
        "2025-02-02T12:00:00Z;comp_B;doc_3;VERIFICATION_PASSED;doc_type=articles_of_incorporation&"
        "2025-02-03T10:00:00Z;comp_B;doc_4;DOC_UPLOADED;doc_type=founder_agreement&"
        "2025-02-05T15:00:00Z;comp_B;doc_4;VERIFICATION_FAILED;doc_type=founder_agreement&"

        # Company C: Will be PENDING
        "2025-02-01T12:00:00Z;comp_C;doc_5;DOC_UPLOADED;doc_type=articles_of_incorporation"
    )

    # Instantiate your solution class
    service = DocumentVerification() # Replace with your class name

    # --- Part 1 ---
    print("## Part 1: Document Status ##")
    # Expected: {'doc_1': 'VERIFIED', 'doc_2': 'VERIFIED', 'doc_3': 'VERIFIED', 'doc_4': 'FAILED', 'doc_5': 'UPLOADED'}
    #print(service.get_doc_status(event_log))
    print("-" * 50)


    # --- Part 2 ---
    print("## Part 2: Company Application Status ##")
    # Expected: {'comp_A': 'COMPLETE', 'comp_B': 'ACTION_REQUIRED', 'comp_C': 'PENDING'}
    #print(service.get_company_application_status(event_log, required_docs))
    print("-" * 50)


    # --- Part 3 ---
    print("## Part 3: Missing Documents ##")
    # Expected: {'comp_B': ['founder_agreement'], 'comp_C': ['articles_of_incorporation', 'founder_agreement']}
    #print(service.get_pending_documents(event_log, required_docs))
    print("-" * 50)


    # --- Part 4 ---
    print("## Part 4: Full Company Report ##")
    # Expected: A detailed report for each company. For comp_C, it might look like:
    # {
    #   'application_status': 'PENDING',
    #   'documents': {
    #     'articles_of_incorporation': {'doc_id': 'doc_5', 'status': 'UPLOADED'},
    #     'founder_agreement': {'doc_id': None, 'status': 'MISSING'}
    #   }
    # }
    print(service.get_detailed_breakdown(event_log, required_docs))
    print("-" * 50)           
            
                                
                
                
        
             
                     
    