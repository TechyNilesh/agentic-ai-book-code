"""
Chapter 6 - Reflection and Self-Improvement
Worked example: reflecting on a failing SQL query.

The book walks through this as a trace, not full runnable code: the
agent writes a query, the executor reports a column error, the agent
reflects and fixes the column name.

This file is illustrative -- it is the two SQL listings from the
chapter plus the surrounding trace as comments, not a full program.
"""

# Task: "Show the names of students who scored above 80 in Maths."

# First attempt -- the agent writes:
FIRST_QUERY = "SELECT name FROM students WHERE marks > 80;"

# The executor runs it and reports:
#   Error: column "marks" is ambiguous; table has marks_maths, marks_science.

# The reflection step receives the SQL and the error, and writes a
# short critique: "The schema uses subject-specific columns.
# Use marks_maths." The next try:
SECOND_QUERY = "SELECT name FROM students WHERE marks_maths > 80;"

# Executor returns 14 rows. Done. Two iterations, one error message,
# one fix -- reflection at its best: a clear external signal, a local
# fix, fast convergence.

if __name__ == "__main__":
    print("Attempt 1:", FIRST_QUERY)
    print("  -> Error: column 'marks' is ambiguous")
    print("Attempt 2 (after reflection):", SECOND_QUERY)
    print("  -> 14 rows returned")
