# Contributing

Thanks for helping improve the table!

## Quickstart (editing via GitHub UI)

1. Open `data/problems.yaml`.
2. Click **Edit** and add or modify an entry, as per the sample template below.  Only the **number** field is mandatory; omit any field for which you have no information.
3. Open a Pull Request.

### Sample template

```yaml
- number: "17"
  prize: "No"
  status:
    state: "open"
    last_update: "2025-08-31"
  oeis: ["A038133"]
  formalized:
    state: "yes"
    last_update: "2025-08-31"
  comments: "cluster primes"
  tags: ["number theory", "primes"]
```

### Notes on template fields

- **number**: The number of the problem in the [erdosproblems.com](https://www.erdosproblems.com) database. Stored as a string.
- **prize**: use "no" if no prize given, or the currency amount otherwise.
- **status**: the known status of the problem, as of the **last_update**.  The main values of **state** are:
  - "solved": the problem is proved, disproved, or otherwise satisfactorily resolved.
  - "falsifiable": the problem is open, but if false, can be disproven with a finitary counterexample.
  - "verifiable": the problem is open, but if true, can be proven with a finitary example.
  - "decidable": the problem is both falsifiable and verifiable, but not yet solved.
  - "open": the problem is open and is not known to be either falsifiable or verifiable.
- **formalized**: the formalization status of the problem (in a formal proof assistant such as Lean), as of the **last_update**.  The main values of **state** are:
  - "yes": the problem has been formalized in the [formal conjectures repository](https://github.com/google-deepmind/formal-conjectures)
  - "no": if no formalization exists.
  - other: the problem is formalized, but in another location than the formal conjectures repository.
- **oeis**: a list of integer sequences (stored as OEIS strings) relevant to the problem, ignoring extremely well known sequences (such as the sequence of primes).  Additional strings include
  - "possible": There may be a sequence associated to the problem that is in the OEIS, but it needs enough values computed that one can cross-check with that database.
  - "submitted": A sequence associated to the problem has been generated to a satisfactory length; it was not in the OEIS, but has been submitted.
  - "N/A": it does not appear that there is an obvious sequence to attach to this problem.  (This status may be updated if new developments create a previously unknown connection to an integer sequence.)

  Note that it is possible for multiple sequences to be associated to a single problem.  For instance, if the problem involves a function $r_k(N)$ of two parameters $k,N$, it may be of interest to use specific choices of one parameter, e.g., $k=1,2,3$, as examples of sequences associated to the problem.
- **comments**: Miscellaneous comments on the problem, for instance describing other names given to the problem.
- **tags**: the tags associated to the problem from the  [erdosproblems.com](https://www.erdosproblems.com) database. Stored as a list of strings.
