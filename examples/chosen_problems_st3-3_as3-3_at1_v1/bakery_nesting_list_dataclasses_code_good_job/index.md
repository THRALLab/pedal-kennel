The dataclass `Job` is defined below with the fields `title` (str), `salary` (int), `available` (boolean), and `company` (str).

Define a function `best_job` that consumes a list of jobs and returns the `Job` with the highest `salary` that is `available`. If no jobs are available, then return the default `UNEMPLOYED` job instead.

You will need to unit test your code a sufficient number of times.

**HINT**: Define a helper function to filter out the unavailable jobs BEFORE you determine the highest salary `Job`. An `if` statement used as a Defensive Guard will be very effective for returning the appropriate value in the case where there are no available guards. Having two helper functions (one to filter available jobs, and one to determine the highest salary) in addition to the main `best_job` function makes this a lot easier to keep track of everything.