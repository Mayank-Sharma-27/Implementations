"""
/***
 * Throughout this interview, we'll write code to analyze a simple server process uptime log.
 * These logs are much simplified, and are just strings of space separated 0's and 1's.
 * The log is a string of binary digits (e.g. "0 0 1 0").
 * Each digit corresponds to 1 hour of the server running:
 *   "1" = <crashed>, "down" // server process crashed during the hour
 *   "0" = <didn't crash>, "up" // server process did not crash during the hour
 *
 * EXAMPLE:
 *   A server with log "0 0 1 0" ran for 4 hours and its process crashed during hour #3
 *   hour: |1|2|3|4|
 *   log : |0|0|1|0|
 *              ^
 *              |
 *              down during hour #3
 *
 * We can *permanently remove* a server at the beginning of any hour during its operation.
 * A server is on the network until it is removed.
 * Note that a server stays POWERED ON after removal, it's just not on the network.
 * We'd like to understand the best times to remove a server.
 * So let's introduce an aggregate metric called a "penalty" for removing a server at a bad time.
 *
 * EXAMPLE:
 *   Remove a server with log "0 0 1 0"
 *   hour : | 1 | 2 | 3 | 4 |
 *   log  : | 0 | 0 | 1 | 0 |
 *   remove_at: 0 1 2 3 4 // remove_at being `x` means "server removed before hour `x+1`"
 *              ^     ^
 *   before hour #1   after hour #4
 *
 * We define our penalty like this:
 *   +1 penalty for each DOWN hour when a server is on the network
 *   +1 penalty for each UP hour after a server has been removed
 *
 * Further Examples:
 *   hour : 1 2 3 4 // total penalty = 3 (3 server-up hours after remove)
 *   log  : 0 0 1 0
 *          ^
 *          |
 *          remove_at = 0
 *
 *   hour : 1 2 3 4 // total penalty = 1 (1 server-down hour before remove)
 *   log  : 0 0 1 0
 *              ^
 *              |
 *              remove_at = 4
 *
 * Note that for a server log of length `n` hours, the remove_at variable can range from 0, meaning "before the first hour" to n, meaning "after the final hour".
 *
 * 1a) Write a function: compute_penalty, that computes the total penalty, given a server log (as a string) AND a time at which we removed the server from the network (call that variable remove_at).
 * In addition to writing this function, you should use tests to demonstrate that it's correct.
 *
 * Examples
 *   compute_penalty("0 0 1 0", 0) should return 3
 *   compute_penalty("0 0 1 0", 4) should return 1
 *
 * 1b) Use your answer for compute_penalty to write another function: find_best_removal_time, that returns the best remove_at hour, given a server log.
 * Again, you should use tests to demonstrate that it's correct.
 *
 * Example
 *   find_best_removal_time("0 0 1 1") should return 2
 *
 * 2a) Now that we're able to analyze single server logs, let's analyze some aggregate logs.
 * Aggregate logs are text files that contain lots of logs.
 * The files contain only BEGIN, END, 1, 0, spaces and newlines.
 * Aggregate logs include some servers that aren’t actually finished, so we might have some BEGINs scattered throughout.
 * We'll only consider inner BEGINs and ENDs to be valid log sequences.
 * Put another way, any sequence of 0s and 1s surrounded by BEGIN and END forms a valid sequence.
 * For example, the sequence "BEGIN BEGIN BEGIN 1 1 BEGIN 0 0 END 1 1 BEGIN" has only one valid sequence "BEGIN 0 0 END".
 * Write a function get_best_removal_times, that takes the file's contents as a parameter, and returns an array of best removal hours for every valid server log in that file.
 * Note: that logs can span 1 or many lines.
 * Again, you should use tests to demonstrate that your solution is correct.
 *
 * Example
 *   get_best_removal_times("BEGIN BEGIN \nBEGIN 1 1 BEGIN 0 0\n END 1 1 BEGIN") should return an array: [2]
 */

"""

class ServerPenalties:
    
    def compute_penalty(self, log: str, remove_time: int) -> int:
        log_tokens = log.split("|")[1:-1]
        penalty = 0
        #print(log_tokens)
        for i in range (remove_time):
            
            if  i < len(log_tokens) and log_tokens[i].strip() == "1":
                
                penalty +=1
        
        for i in range (remove_time, len(log_tokens)):
            if log_tokens[i].strip()  == "0":
                penalty += 1
                
        return penalty
    
    def find_best_removal_time(self, log: str) -> int:
        log_tokens = log.split("|")[1: -1]
        
        min_penalty =  float('inf')
        best_time_to_remove = 0
        for i in (0, len(log_tokens) + 1):
            penalty = self.compute_penalty(log, i)
            if min_penalty > penalty:
                min_penalty = min(min_penalty, penalty)
                best_time_to_remove = i
        return best_time_to_remove
    
    def get_best_removal_times(self, server_logs: str) -> list:
        tokens = server_logs.replace("\n", " ").split()
        results = []
        
        in_log = False
        current_log = []
        
        for token in tokens:
            if token == "BEGIN":
                if in_log:
                    current_log = []
                in_log = True
            elif token == "END":
                if in_log and current_log:
                   joined_log = "|" + "|".join(current_log) + "|"
                   
                   results.append(self.find_best_removal_time(joined_log))
                in_log = False
                current_log = []
            else:
                if token in {"0", "1"}:
                    current_log.append(token)
        return results                   
                   
                            
        

if __name__ == "__main__":
    log = "| 1 | 0 | 0 | 0 |"
    service =  ServerPenalties()
    
    print(service.compute_penalty(log,1))
    
    print("Part 2")
    
    print(service.find_best_removal_time(log)) 
    log_text = "BEGIN BEGIN \nBEGIN 1 1 BEGIN 0 0\n END 1 1 BEGIN"
    print(service.get_best_removal_times(log_text))          
                
        
                        

