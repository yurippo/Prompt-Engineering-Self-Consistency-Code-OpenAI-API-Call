# Self-Consistency
# Next Activity

# Finishing this last lesson, we will teach a technique called Self-Consistency, published in the paper
# "Self-Consistency Improves Chain of Thought Reasoning in Language Models," written by Xuezhi Wang and others from Google in 2022.
# This technique is very powerful, especially when dealing with numbers, values, and facts.

# Self-Consistency can improve Chain of Thoughts, i.e., the chain of thought reasoning in language models.
# The idea is simple but very effective.

# We can assume that as language models become more powerful, the answers they provide also improve.
# Most of the time, the answer the model provides will be correct. However, it is possible that the model makes mistakes.

# Imagine you are running your system, either manually or in an automated manner using an API, and you ask a question and the model provides an answer.
# You are not sure if the answer was correct and want to verify it. For this, the Self-Consistency technique was invented,
# which basically consists of asking the model the same question multiple times, creating a list with the answers, and seeing which one was the most frequent.
# The most frequent answer is likely to be the correct answer, considering that these models are correct most of the time.

# Understanding the technique in practice
# To demonstrate this, we created a code in Google Colab. For those who don't know, Google Colab is an environment where you can program in Python without having to download anything.
# You can do this directly on the site colab.research.google.com.

# First, we need to install the OpenAI library in our Colab environment:
# pip install -q openai

# Then, we import the library and need an API to identify ourselves to OpenAI. We use an API key, which is a value that identifies who we are to OpenAI.

# We have our initial message, which defines the role of the model. In this case, the model is a helpful assistant.
# Then, we define the initial parameters of ChatGPT, which is the most basic value of most models.

from google.colab import userdata
import openai

# set the API key
openai.api_key = userdata.get('OPENAI_API_KEY')

# Definition of system persona and message history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},  # sets the model's persona, whether it will be polite, formal, sarcastic, etc.
]

# The interesting part begins when we create a variable called answers, which is initially empty.
# Let's assume we will ask the question four times, so the number of loops will be four.

# SELF-CONSISTENCY
answers = []
LOOPS = 4
prompt = """Always return at the end the string 'Resultado: ' with only the result value after it, no operation or punctuation beyond the value.
Question: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars will be in the parking lot?
Answer: There are already 3 cars in the parking lot. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.
Resultado: 5
Question: Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and makes muffins for her friends every day using four more. She sells the rest for 2 dollars per egg. How much money does she make every day?
Answer:
Resultado:"""

# We are creating our chain of thought and teaching the model to reason with the example of the cars.
# The question, the answer, and the result of the car problem are provided by us.

# Right below is the real case for which we want an answer. If Janet had 16 eggs, ate three, and used four more to make muffins, she has nine left.
# Thus, multiplying nine eggs by two dollars, we have 18 dollars.

# We leave the answer and the result blank for the model to fill in, following our Chain of Thoughts pattern.
# After defining the prompt, we put it inside a variable, and this variable will be sent within the messages to OpenAI.

# We do a for loop, which is basically a repetition. We do everything inside the loop once, then a second time, then a third time, until we reach the number we asked to stop at.

# We make the call to OpenAI, get the response, and add it to the list of answers (answers).
# At the end, we want to see what the most frequent value is and how many times it appears.

messages.append({"role": "user", "content": prompt})  # adds your question to the chat history
for loop in range(0, LOOPS):
    # API call
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        max_tokens = 200,
        temperature = 1
    )
    # Extract the answer from within the response JSON
    answer = response.choices[0].message.content
    print(f"### LOOP", loop, ':\n')
    print(answer)

    start_index = answer.find("Resultado: ") + len("Resultado: ")
    if start_index != -1:
        number_answer = answer[start_index:].split()[0].rstrip('.')
        print("Answer:", number_answer, '\n------')
        answers.append(int(number_answer))  # adds the answer to the list of answers
print(answers, '\n')

# Let's run the code and see how it works in practice. We run the code and see that the most frequent value is 18, which appears four times.
# Let's execute the same code one more time. This time, the most frequent value is 18, which appears three times.
# So, we understand how the technique works. We could do it more times, for example, 10 or 15 times, and take the most frequent value if it is something more important.

[18, 18, 24, 18]
# The most frequent value is 18, which appears 3 times.

# Based on the idea that most of the time the model will be correct, we can obtain the result.
# However, this code is not perfect because sometimes the model does not return exactly the result of two points, it returns a text,
# and in this conversion, if it takes a text it will give an error, and cannot compare text with number.

# But it already serves to explain how this Self-Consistency technique works.
# This base code will be available for you to improve and adapt to your needs.
