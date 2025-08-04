from google.colab import userdata
import openai

# Set the API key
openai.api_key = userdata.get('OPENAI_API_KEY')

# Definition of system persona and message history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# Self-Consistency technique implementation
answers = []
LOOPS = 4
prompt = """Always return at the end the string 'Resultado: ' with only the result value after it, no operation or punctuation beyond the value.
Question: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars will be in the parking lot?
Answer: There are already 3 cars in the parking lot. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.
Resultado: 5
Question: Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and makes muffins for her friends every day using four more. She sells the rest for 2 dollars per egg. How much money does she make every day?
Answer:
Resultado:"""

# Append the user's prompt to the messages
messages.append({"role": "user", "content": prompt})

# Loop to ask the model the same question multiple times
for loop in range(LOOPS):
    try:
        # API call to get the model's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=1
        )

        # Extract the answer from the response
        answer = response.choices[0].message.content
        print(f"### LOOP {loop}:\n{answer}")

        # Extract the result value from the answer
        start_index = answer.find("Resultado: ")
        if start_index != -1:
            result_str = answer[start_index + len("Resultado: "):].split()[0].rstrip('.')
            try:
                result = int(result_str)
                answers.append(result)
                print(f"Answer: {result}\n------")
            except ValueError:
                print(f"Could not convert {result_str} to an integer.")
        else:
            print("The expected result format was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

print(f"Answers: {answers}")

# Determine the most frequent answer
if answers:
    most_frequent_answer = max(set(answers), key=answers.count)
    frequency = answers.count(most_frequent_answer)
    print(f"The most frequent answer is {most_frequent_answer}, which appears {frequency} times.")
else:
    print("No valid answers were obtained.")
