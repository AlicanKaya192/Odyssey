# Where to Go From Here

Python Fundamentals is finished. This note answers the question "what now?"

## An honest assessment first

Finishing the sections is not the same as having learned them. Can you do
these **without looking anything up**?

- Take the average of the numbers in a list
- Loop through a dictionary and add up the ones matching a condition
- Write a function that takes two values and returns one
- Read a file line by line and turn it into a dictionary
- Skip broken data with `try` / `except`
- Write a class with an `__init__` and a method

If you get stuck on any of them, go back to that section. There is nothing to
be embarrassed about — when the foundation is missing, everything built on top
of it wobbles.

## Reading error messages

This is what you will do most from now on. The method:

1. **Read the last line.** The error's type and explanation are there.
2. **Look upwards.** Find which line of which file it happened on.
3. **Focus on the lowest line that is your own code.** Lines inside a library
   are usually the result of your mistake, not its cause.
4. **Search for the error text as it is.** Removing your own variable names
   before searching improves the results.

Solving one error teaches you more than learning a new topic.

## How do you practise?

**Automate your own work.** The best exercise is something you actually need.
Examples:

- A script that tidies up the file names in a folder
- A small program that keeps your notes in a file and searches them
- A script that reads your timetable and says what is on today

**Start small and finish it.** An unfinished large project teaches you less
than a finished small one.

**Read your own code a week later.** If you do not understand it, you did not
write it clearly enough. That is the most honest feedback there is.

## What is next on the learning route?

<figure class="fig">
  <div class="flow">
    <span class="node ok"><b>Python</b><br>finished</span>
    <span class="arrow">→</span>
    <span class="node acc"><b>Data Science</b><br>next</span>
    <span class="arrow">→</span>
    <span class="node"><b>Machine Learning</b></span>
  </div>
  <figcaption>SQL, API and Docker are not tied to this order; you can start them whenever you like once Python is done.</figcaption>
</figure>

**Data Science** is the natural continuation. Which knowledge from here
connects to it:

| What you learned here | What it becomes there |
|---|---|
| A list | A NumPy array |
| A list of dictionaries | A pandas table (`DataFrame`) |
| Reading and parsing a file | `read_csv` |
| Filtering with a loop | Filtering a table |
| Reading `dict[str, list[int]]` | Understanding table columns |

**SQL** carries on from where this section started: you know `SELECT` and
`WHERE`, and `JOIN` is added to them.

For **API** work your dictionary and error-handling knowledge is essential —
API responses arrive as JSON, and JSON is a dictionary in Python.

## A common question: "Why did I learn this when libraries exist?"

pandas reads a file in one line with `read_csv`. You wrote ten. Was it wasted?

No. The difference shows up in three situations:

- **When the file contains a broken row.** `read_csv` raises an error, and
  only someone who knows how to parse by hand understands what happened.
- **When you need something the library does not do.** Then you have to write
  it yourself.
- **When reading an error message.** What `KeyError` means, why `NoneType`
  turns up — that is knowledge of the language, not of the library.

A library gives you speed; the fundamentals give you **control**.

## One piece of advice

When learning something new, work out **what it is for** before how it is
written. Syntax can be looked up; knowing when to use something cannot.

That is why every topic in these sections starts with a "what is the problem?"
part.
