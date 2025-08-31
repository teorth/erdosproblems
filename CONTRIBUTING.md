# Contributing

Thanks for helping improve the table!

## Quickstart (editing via GitHub UI)

1. Open `data/problems.yaml`.
2. Click **Edit** and add an entry. Use the template below.  Only the "number" field is required; omit any field for which you have no information.
3. Open a Pull Request.

### Entry template

```yaml
- number: "1"
  prize: "$500"         # use "No" if no prize given
  status:
    state: "open"       # use "open", "solved", "partial", or "unknown"
    last_update: "2025-08-31"
  oeis: ["A276661"]     # "N/A" if you are *sure* there is no obvious sequence to attach
                        # to this problem
                        # "Possible" if there is potentially a sequence for this problem that
                        # is in the OEIS (but it needs to be checked)
                        # "Missing" if there is a sequence, but it is not in the OEIS
                        # If multiple OEIS sequences are related to this problem, separate
                        # the strings by commas
  formalized:
    state: "yes"        # "yes" if the problem has been formalized in
                        # https://github.com/google-deepmind/formal-conjectures
                        # "no" otherwise
    last_update: "2025-08-31"
  tags: ["number theory", "additive combinatorics"]
