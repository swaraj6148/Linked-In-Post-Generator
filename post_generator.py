from llm_helper import llm
from few_shots import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length=="Short":
        return "1 to 5 lines"
    if length=="Medium":
        return "6 to 10 lines"
    if length=="Long":
        return "11 to 15 lines"
    

def generate_post(length,language,tag): #made for main.py
    prompt = get_prompt(length,language,tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length , language , tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''

    examples = few_shot.get_filtered_posts(length,language,tag) #here we got a dictionary

    if len(examples) > 0: #ie if similar example availiable hain apne pass in processed_post.json jisko apan search/extract kr skte hain using the logic in few_shots.py
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples): #i=0 initialised because enumerate starts indexing from 0
        if i == 2: # Use max two samples(i=0,i=1) beacuse using more will increase the prompt size very much and our llm token_usage will be wasted
            break
        prompt += f'\n\n Example_number:{i+1} \n\n {post['text']}'

    return prompt


if __name__ == "__main__":
    generated_prompt = get_prompt("Medium", "English", "JobSearch")
    print(generated_prompt)
