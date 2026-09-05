# Formulas used in Lab 9

| Property | Database | Formula | Notes |
|---|---|---|---|
| Days Left | Projects | `dateBetween(prop("Dates").end, now(), "days")` | `.end` reads the end of a date range; negative means overdue |
| Health | Projects | `if(prop("Tasks Done") >= 0.8, "🟢 On track", if(prop("Days Left") < 7, "🔴 At risk", "🟡 Watch"))` | nested `if`; Tasks Done is a percent rollup (0–1) |
| Budget/Hour | Projects | `format(round(prop("Budget (SGD)") / prop("Total Hours")))` | `round` then `format` to text; guard division by zero with `if(prop("Total Hours") == 0, "—", …)` |
| Overdue | Tasks | `and(prop("Due") < now(), prop("Status") != "Done")` | boolean shown as a checkbox |
| Priority | Ideas (Lab 12) | `prop("Impact") - prop("Effort")` | sort descending |

## Functions in one line each
- `prop("Name")` — read a property of this row
- `if(condition, then, else)` — branch
- `dateBetween(a, b, "days")` — difference between dates
- `now()` — the current date-time
- `round(x)`, `format(x)`, `toNumber(x)` — numbers and text conversion
- `and(a, b)`, `or(a, b)`, `empty(x)` — logic
