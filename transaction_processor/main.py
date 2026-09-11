"""
Project 1 — Transaction Processing Engine
Difficulty: 1/10 → 2/10

We're starting deliberately below your theoretical ceiling.

The goal isn't to build something impressive. The goal is to see whether you can take a messy requirement and decompose it into a program.

Imagine you're building the core of a small financial application.

You receive transactions like:

transactions = [
    {
        "id": 1,
        "user": " Nahom ",
        "type": "income",
        "amount": "1500",
        "status": "completed",
    },
    {
        "id": 2,
        "user": " Nahom ",
        "type": "expense",
        "amount": "200",
        "status": "completed",
    },
    {
        "id": 3,
        "user": " Abel ",
        "type": "income",
        "amount": "800",
        "status": "pending",
    },
    {
        "id": 4,
        "user": " Abel ",
        "type": "expense",
        "amount": "100",
        "status": "completed",
    },
    {
        "id": 5,
        "user": " Nahom ",
        "type": "income",
        "amount": "500",
        "status": "failed",
    },
]

Your program needs to process these transactions.

Requirements

Build a small processing system that can:

1. Clean the input

User names may contain unnecessary whitespace.

Amounts arrive as strings.

Transactions may contain invalid data.

2. Validate transactions

A valid transaction must have:

an id
a user
a valid type: "income" or "expense"
a positive numerical amount
a valid status: "completed", "pending", or "failed"

Invalid transactions should not crash the entire processing operation.

3. Process only completed transactions

Pending and failed transactions shouldn't affect the financial totals.

4. Calculate per-user results

For every user, calculate:

total_income
total_expense
balance
number_of_transactions

For example, conceptually:

{
    "Nahom": {
        "total_income": 1500,
        "total_expense": 200,
        "balance": 1300,
        "number_of_transactions": 2,
    }
}
5. Produce a final report

The system should return something representing:

Processed transactions: ...
Invalid transactions: ...
Users: ...

User: Nahom
Income: ...
Expenses: ...
Balance: ...
Transactions: ...

You decide the exact structure.

But there's an important constraint

Don't immediately start writing code.

I specifically want to see your programmer thinking first.

Before touching the keyboard, answer these questions in your own words:

A. Problem decomposition

What are the separate problems hiding inside this seemingly simple requirement?

For example, don't just say:

"I need a function that processes transactions."

Think about what transformations and responsibilities actually exist.

B. Data flow

Describe how you imagine a transaction moving through the system.

Something like:

raw data
   ↓
?
   ↓
?
   ↓
?
   ↓
final report

But design your own flow.

C. Data representation

What structures would you use?

dictionaries?
lists?
tuples?
dataclasses?
classes?
closures?
something else?

There is no prescribed answer.

Explain why.

D. Functional vs OOP

This is important given what we've just studied.

Would you approach this primarily with:

functional composition,
classes/objects,
a mixture,
something else?

Again, don't choose something because we studied it. Choose based on the problem.

E. Mutation

Where, if anywhere, do you think mutation is appropriate?

Would you mutate the incoming transaction dictionaries?

Would you create new structures?

Would you use an accumulator?

Explain your reasoning.

F. Error handling

What should happen if you encounter something like:

{
    "id": 10,
    "user": "John",
    "type": "income",
    "amount": "hello",
    "status": "completed",
}

Should it raise?

Skip it?

Collect it somewhere?

Return an error?

Why?

G. Most importantly

What would your functions/components be?

Don't give me code yet.

Give me something like:

component/function 1 → responsibility
component/function 2 → responsibility
component/function 3 → responsibility
...

You are free to completely reject that approach.

One more rule

Don't try to make this a production banking system.

No FastAPI.

No database.

No Redis.

No Kafka.

No external libraries.

No design-pattern showcase.

No unnecessary abstractions.

Python standard library + your brain.

The challenge here is not:

"How much architecture can Nahom create?""""