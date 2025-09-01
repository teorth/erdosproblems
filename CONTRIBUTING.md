# Contributing

Edits and contributions to this table are very welcome, particularly with regards to the OEIS column!

## Quickstart (editing via GitHub UI)

1. Open `data/problems.yaml`.
2. Click **Edit** and add or modify an entry, as per the sample template below.  Only the **number** field is mandatory; omit any field for which you have no information.
3. Open a Pull Request.
4. If there is additional mathematical context that you could give concerning your edit, consider also adding a comment to the corresponding problem page on the [erdosproblems.com](https://www.erdosproblems.com) site.

If you are uncertain as to whether an edit is appropriate, you are welcome to open an issue on this repository to discuss it, or (if the question is mathematical in nature) use the corresponding problem page on the [erdosproblems.com](https://www.erdosproblems.com) site.

## Sample template

```yaml
- number: "17"
  prize: "no"
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

## Notes on template fields

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
  - "other": the problem is formalized, but in another location than the formal conjectures repository.  Details should appear in **comments** or in the [erdosproblems.com](https://www.erdosproblems.com) page.
- **oeis**: a list of integer sequences (stored as [OEIS](https://oeis.org/) strings) relevant to the problem, ignoring extremely well known sequences (such as the sequence of primes).  Additional strings include
  - "possible": There may be a theoretically computable sequence associated to the problem that is in the OEIS, but it needs enough values actually computed that one can cross-check with that database.
  - "submitted": A sequence associated to the problem has been generated to a satisfactory length; it was not in the OEIS, but has been submitted.  **Important note**: please adhere to all the OEIS guidelines when considering submitting a new sequence there.  For instance, one should avoid submissions that are primarily AI-generated and not reviewed carefully by a human.
  - "N/A": it does not appear that there is an obvious sequence to attach to this problem.  (This status may be updated if new developments create a previously unknown connection to an integer sequence.)

  Note that it is possible for multiple sequences to be associated to a single problem.  For instance, if the problem involves a function $r_k(N)$ of two parameters $k,N$, it may be of interest to use specific choices of one parameter, e.g., $k=1,2,3$, as examples of sequences associated to the problem.  Note also that the classification of a problem as having a "possible" OEIS sequence or not may be based on a cursory reading of the problem, and can be subject to revision.
- **comments**: Miscellaneous comments on the problem, for instance describing other names given to the problem.
- **tags**: the tags associated to the problem from the  [erdosproblems.com](https://www.erdosproblems.com) database. Stored as a list of strings.

## Linking with the OEIS

We are particularly interested in contributions regarding the integer sequences associated with the Erdos problems, and linking them to the [OEIS](https://oeis.org/).  If you would like to help out in this regard, we suggest the following.

- Navigate to the problem page of an Erdos problem for which an OEIS sequence is marked as "possible" on the table.
- The mathematical description or commentary of that problem may describe (either explicitly or implicitly) one or more integer sequences (often denoted by a function such as `f(n)` or `g(n)`).
- If you feel able to do so, see if you can compute (either by hand, by writing a program, or using AI assistance) the first few values of that sequence (typically one needs about five or six values at least to be useful).  [But see the next section regarding the use of AI tools.]
- Look up the sequence in the [On-line Encyclopedia of Integer Sequences (OEIS)](https://oeis.org/) to see if the sequence is already listed there, with a description that is functionally equivalent to the one in problem page.
- If a match is found, you can submit a pull request to update the table with that sequence (or, if you prefer, write an issue or make a comment at the problem page).
- If no match is found, you can still report your sequence as a Github issue or on the Erdos problem web page, and we can discuss whether to submit the sequence to the OEIS (at which point we would update the table accordingly).
- If the sequence matches a seemingly unrelated sequence, this could either be a coincidence, or an unexpected connection with another problem.  It would be best to debate this on the appropriate Erdos problem web page before taking further action.

## On the use of AI tools

Many of the integer sequences associated with the Erdos problems could concievably be calculated to some reasonable finite length by code generated by AI.  This is potentially a good use of AI tooling, especially if it leads to identifying a match with an existing OEIS sequence.  However, in the event that an AI-generated code produces a sequence that does not match any existing OEIS sequence, it will be important to independently verify the output of that code, in order to rule out (with reasonable confidence) the possibility that the code contained bugs or hallucinations that caused it to compute the sequence incorrectly.  In particular, new submissions to the OEIS should not come purely from AI-generated data, but be checked by humans (or against human-written code).  If in doubt, open a Github issue regarding the code.
