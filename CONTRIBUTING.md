# Contributing

Thanks for helping improve the table!

## Quickstart (editing via GitHub UI)

1. Open `data/problems.yaml`.
2. Click **Edit** and add an entry. Use the template below.
3. Run checks locally if you can (`scripts/validate.py`), or rely on CI.
4. Open a Pull Request. CI will validate the format and the README freshness.

### Entry template

```yaml
- id: "kissing-number-3d"          # lowercase, hyphens
  name: "Kissing Number in 3D"
  area: "Discrete geometry"
  status:
    state: "solved"
    last_update: "2025-08-31"
    note: "24 spheres; solved historically by Schütte–van der Waerden."
  statements:
    short: "Max number of unit spheres tangent to a given one in ℝ^3."
  references:
    oeis: []
    urls:
      - "https://en.wikipedia.org/wiki/Kissing_number_problem"
  tags: ["sphere packing", "geometry"]
