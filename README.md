# Overview
This repo contains pthyon scriprs that simulate  multi-step workflows.

1. Run generator_randon_events.py -  creates transaction with random numver of steps.  Data includes: id, seq, date.
2. Run analyze_sequences.py -  creats a table of unique paths and the counts of records the use those paths.
3. Run analyze_sequences_paths.py -  creats a table of unique hops and the counts and duration of records the use those hops.

# Paths and Hops
- path A > B > C 
- hops AB, BC

## 20250425 Meeting Notes
### PATHS
- Frequency of Paths
- Hope that N400 has common paths (type)
- Each office could have their own path (office)

### Durations Hop
- Avg, std, min, max path
- Events (bad event)

### ML Models
 - Predictive how long start tp finish
 - Revaluate hop to end
 - Predict the time to complete the hop
 - Predict the time to get to a specific hop. 

 TEST