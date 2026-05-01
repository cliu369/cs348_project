# AI Usage

## Which AI Tools Were Used

Google Gemini.

## What Tasks the AI Assisted With
The task the LLM assisted with 
was coming up with the first draft of the 
non-database related code, essentialy
the HTML files and setup for the Flask application. 
I also used it to clarify concepts (this did not generate any output).

## How the student verified or modified the AI-generated output

The workflow I used is that I came up with the high-level ideas for the project, including (but not limited to): 
* Schema for database
* Operations on database
* Choice of isolation levels, sql injection
* GUI design 

I would then ask the LLM to generate the first draft of code 
that I regarded as "boilerplate", e.g. not related to 
the manipulation of the actual database. For example, I asked to
generate the HTML files which determined how the GUI would look. I would manually inspect and test LLM-generated code
by running it on different cases and looking up any 
code that I did not understand on the respective documentation
(for example, for HTML I used https://developer.mozilla.org/en-US/) to see if the LLM use made sense. I would then 
manually edit the code if there were parts of the code 
that I was unhappy with, such as if there were parts of the GUI that was not to my liking.

