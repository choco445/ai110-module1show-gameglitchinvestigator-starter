# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
The game had a pretty basic and plain layout, with just a couple of buttons in the middle allowing the user to make guesses and see hints which would tell the user whether they should guess higher or lower. However, some bugs were there.
##1. The hint kept saying to go lower, regardless of the guess, and it didn't prevent the user from entering numbers lower than or higher than the range and also didn't give any additional warning messages. 
##2. The diffferent ranges for difficulty levels don't show in the main UI, it just says the range is 1-100.
##3. The New Game Button doesn't do anything and the game basically just freezes.
##4. Tells you that you're out of attempts when you have one attempt left
##5. Says that you have 8 attempts left when you have a total of 8 attempts, so UI number is 1 higher than what it should be

Glitch: the hint text is inverted — when your numeric guess is higher than the secret the app tells you to "Go HIGHER!" and when your guess is lower it tells you to "Go LOWER!".

Why that happens (underlying logic): in check_guess() the numeric comparison branch does return the correct outcome labels ("Too High" vs "Too Low") but the human-facing messages are swapped:

if guess > secret -> returns "Too High", "📈 Go HIGHER!" (message should say go LOWER)
else -> returns "Too Low", "📉 Go LOWER!" (message should say go HIGHER)
This is compounded by the game sometimes converting the secret to a string on even-numbered attempts (secret = str(...)), which forces the try block to raise TypeError and fall back to string comparisons. That changes the comparison semantics (lexicographic instead of numeric), producing inconsistent/wrong direction hints in addition to the inverted messages.



---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Copilot
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
When I was trying to refactor the logic into a separate file, I used Copilot Agent mode to help me with that. I asked it to refactor the check_guess function from app.py into logic_utils.py and it provided me with the correct code for that. I verified the result by running the tests that I had written for the check_guess function and they all passed successfully.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The first time I tried to fix the issues using AI, I used the regular "Ask" mode and it didn't give me code that correctly worked to pass all the tests,and had some gaps. However, after I asked more questions in the Agent mode, it was able to fix th code so it would correctly display to go higher or lower in the game and pass all the tests.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I created and ran custom test cases and checked if all of them passed.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  One of the tests I ran was to check if the check_guess function was returning the correct outcome and message for a guess that was higher than the secret number. I created a test case where the secret number was 50 and the guess was 60, and I expected the outcome to be "Too High" and the message to be "📈 Go LOWER!". I ran this test case using pytest and it passed successfully, which gave me confidence that the bug related to the hints being inverted was fixed.
- Did AI help you design or understand any tests? How?
Yes, AI helped me understand how to design tests for the check_guess function. When I was writing tests for that function, I wasn't sure how to structure my test cases and what inputs to use. I asked Copilot for suggestions on how to write tests for that function, and it provided me with examples of test cases that covered different scenarios (e.g., guess is too high, guess is too low, guess is correct). This helped me understand how to create comprehensive tests that would effectively verify the correctness of the check_guess function.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number kept changing in the original app because it was being reinitialized on every rerun of the Streamlit app. In Streamlit, every time a user interacts with the app (e.g., by making a guess or clicking a button), the entire script is rerun from top to bottom. If the secret number is generated at the top level of the script without being stored in session state, it will be regenerated on every rerun, leading to a different secret number each time.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit "reruns" refer to the fact that every time a user interacts with a Streamlit app (like clicking a button or entering input), the entire script is executed again from the beginning. This means that any variables or state that are defined at the top level of the script will be reset to their initial values on each interaction, which can lead to issues like the secret number changing unexpectedly.
- What change did you make that finally gave the game a stable secret number?
To give the game a stable secret number, I moved the logic for generating the secret number into a function that is called only when the game is initialized or reset. I also stored the secret number in Streamlit's session state, which allows it to persist across reruns of the app. This way, the secret number is generated once and remains consistent throughout the game until the user decides to start a new game, at which point it will be reinitialized.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
I would use Copilot as a tool and ask it questions, allowing it to guide me throughout my coding process. I would also use it to create test cases and copy/paste the outputs of the test cases into the Copilot chat to help me figure out how and where to fix the code so the test cases successfully pass.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
I would use the Agent mode when asking AI to make suggestions in the code for me and the regular "Ask" mode when asking AI to explain concepts to me.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project made me realize that AI-generated code can be a powerful tool for debugging and refactoring, but it's important to critically evaluate the suggestions and verify them with tests. It also highlighted the importance of understanding the underlying logic and structure of the code, rather than just relying on AI to fix issues without fully grasping the problem.
