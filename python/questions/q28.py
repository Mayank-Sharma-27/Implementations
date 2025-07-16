"""
 * Part 1
 * Imagine an Airbnb-like vacation rental service, where users in different cities can exchange their apartment with another user for a week.
 * Each user compiles a wishlist of the apartments they like.
 * These wishlists are ordered, so the top apartment on a wishlist is that user's first choice for where they would like to spend a vacation.
 * You will be asked to write part of the code that will help an algorithm find pairs of users who would like to swap with each other.
 *
 * Given a set of users, each with an *ordered* wishlist of other users' apartments:
 *   a's wishlist: c d
 *   b's wishlist: d a c
 *   c's wishlist: a b
 *   d's wishlist: c a b
 * The first user in each wishlist is the user's first-choice for whose apartment they would like to swap into.
 * Write a function called has_mutual_first_choice() which takes a username and returns true if that user and another user are each other's first choice, and otherwise returns false.
 *
 * has_mutual_first_choice('a') // true (a and c)
 * has_mutual_first_choice('b') // false (b's first choice does not *mutually* consider b as their first choice)
 *
 * Then expand the base case beyond just "first" choices, to include all "mutually ranked choices".
 * Write another function which takes a username and an option called "rank" to indicate the wishlist rank to query on.
 * If given a rank of 0, you should check for a first choice pair, as before.
 * If given 1, you should check for a pair of users who are each others' second-choice.
 * Call your new function has_mutual_pair_for_rank() and when done, refactor has_mutual_first_choice() to depend on your new function.
 *
 * has_mutual_pair_for_rank('a', 0) // true (a and c)
 * has_mutual_pair_for_rank('a', 1) // true (a and d are mutually each others' second-choice)
 *
 * data = {
 *   'a': ['c', 'd'],
 *   'b': ['d', 'a', 'c'],
 *   'c': ['a', 'b'],
 *   'd': ['c', 'a', 'b'],
 * }
 *
 * Part2
 * Every wishlist entry in the network is either "mutually ranked" or "not mutually ranked" depending on the rank the other user gives that user's apartment in return.
 * The most common operation in the network is incrementing the rank of a single wishlist entry on a single user.
 * This swaps the entry with the entry above it in that user's list.
 * Imagine that, when this occurs, the system must recompute the "mutually-ranked-ness" of any pairings that may have changed.
 * Write a function that takes a username and a rank representing the entry whose rank is being bumped up.
 * Return an array of the users whose pairings with the given user *would* gain or lose mutually-ranked status as a result of the change, if it were to take place.
 * Call your function changed_pairings()
 *
 * // if d's second choice becomes their first choice, a and d will no longer be a mutually ranked pair
 * changed_pairings('d', 1) // returns ['a']
 *
 * // if b's third choice becomes their second choice, c and b will become a mutually ranked pair (mutual second-choices)
 * changed_pairings('b', 2) // returns ['c']
 *
 * // if b's second choice becomes their first choice, no mutually-ranked pairings are affected
 * changed_pairings('b', 1) // returns []

"""
import copy
class Ranking:
    
    def has_mutual_pair_for_rank(self, user: str, rank: int, data: dict) -> bool:
        if user not in data:
            return False
        if rank >= len(data[user]):
            return False 
        user_choice = data[user][rank]
        if user_choice not in data:
           return False
       
        if rank >= len(data[user_choice]):
            return False
           
       
        other_user_rank = data[user_choice][rank]
        
        return other_user_rank == user
    
    def changed_pairings(self, user: str, change_rank: int, data: dict) -> list:
        impacted_choices = []
        if user not in data:
            return []
        if change_rank >= len(data[user]):
            return []
        user_choice = data[user][change_rank]
        if user_choice not in data:
           return []
        
        if self.has_mutual_pair_for_rank(user, change_rank, data):
            impacted_choices.append(user_choice)
            
        copy_data = copy.deepcopy(data)    
            
        rank_to_change = copy_data[user][change_rank]
        previous_rank = copy_data[user][change_rank -1]
        copy_data[user][change_rank -1] = rank_to_change
        copy_data[user][change_rank] = previous_rank
        
        
        if self.has_mutual_pair_for_rank(user, change_rank -1, copy_data):
            impacted_choices.append(rank_to_change)
        if self.has_mutual_pair_for_rank(user, change_rank, copy_data):
            impacted_choices.append(previous_rank) 
        
        return impacted_choices
    
if __name__ == "__main__":
    service = Ranking()

    # --- Initial Data for Tests ---
    initial_data = {
        'a': ['c', 'd'],
        'b': ['d', 'a', 'c'],
        'c': ['a', 'b'],
        'd': ['c', 'a', 'b'],
    }

   
    # --- Additional Test Cases for has_mutual_pair_for_rank ---
    data_hmpr_ext = {
        'user1': ['user2', 'user3'],
        'user2': ['user1', 'user4'],
        'user3': ['user1', 'user5'],
        'user4': ['user2'],
        'user5': [], # Empty wishlist
        'user6': ['user7'],
        'user7': ['user6'],
        'user8': ['user9'],
        'user9': ['user10'], # user9 likes user10, user10 not in data
    }
    print("\n--- Part 2: changed_pairings ---")
    # Using the original data for problem examples
    data_cp_orig = {
        'a': ['c', 'd'],
        'b': ['d', 'a', 'c'],
        'c': ['a', 'b'],
        'd': ['c', 'a', 'b'],
    }

    # Example 1: if d's second choice ('a') becomes their first choice,
    # 'a' and 'd' will no longer be a mutually ranked pair at rank 1.
    # 'd' likes 'a' at rank 1, 'a' likes 'd' at rank 1. (Mutual)
    # After swap: 'd' likes 'a' at rank 0, 'a' likes 'c' at rank 0. (Not Mutual)
    print(f"changed_pairings('d', 1): {service.changed_pairings('d', 1, data_cp_orig)}") # Expected: ['a']

    # Example 2: if b's third choice ('c') becomes their second choice,
    # 'c' and 'b' will become a mutually ranked pair (mutual second-choices).
    # 'b' likes 'c' at rank 2, 'c' likes 'b' at rank 1. (Not Mutual)
    # After swap: 'b' likes 'c' at rank 1, 'c' likes 'b' at rank 1. (Mutual)
    print(f"changed_pairings('b', 2): {service.changed_pairings('b', 2, data_cp_orig)}") # Expected: ['c']

    # Example 3: if b's second choice ('a') becomes their first choice,
    # no mutually-ranked pairings are affected.
    # 'b' likes 'a' at rank 1, 'a' likes 'd' at rank 1. (Not Mutual)
    # After swap: 'b' likes 'a' at rank 0, 'a' likes 'c' at rank 0. (Not Mutual)
    print(f"changed_pairings('b', 1): {service.changed_pairings('b', 1, data_cp_orig)}") # Expected: []

    # --- Additional Test Cases for changed_pairings ---

    # Test Case 4: Invalid inputs
    
            
        
        
        