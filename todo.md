# TODO and hq feedback

#yk TODO items
## Nov 17, 2016

- [ ] get next road probability
 - [ ] take as input all the roads at the intersection
 - [ ] show the probability based on previous road sequence
2. need a boundary for search region
 - currently it's just marking search region
3. think about what does steps, terminal state mean?
 - can we just use # of intersections in the large search region and use it as steps?
4. can we improve value of search so that it is more than # of search counts?
5. should take into account directionality based on that think about how many steps look ahead
 - maybe this point can be resolved when 1) is resolved.


#hq feedback
## Nov 16, 2016
* essentially what we need is to decide go straight, left, or right at next intersection
* in each road segment, value representation can be a distribution
* what is the right model for the value of searches
    * taking into account who might potentially show up in the future
    * need more reference for V* - V(-i)*

## July, 2016
* need a list for search count on each street
* check boosting algorithm
* need to refine the model
* what happens if someone is staying in the same road?
    * yk: maybe check every 50 meters; keep the duplicate roads
    * still nice to keep the abstraction of hit-or-wait
        - why implementing for road specific scenario?

# yk notes:
* need better job on deciding which intersections for searches
* how do you wanna show the state?
    * what is the terminal state?
    * use intersections as state
        * how do you get intersections as state? --> what are the intersections that it has in the lost item region?
        * if a user come across the intersection we pull out the decision table
        * assume a user is in the search region
        * for each intersection in the search region, we decide whether to ping on the street the person is going or not
        * how many steps look ahead? one state?
