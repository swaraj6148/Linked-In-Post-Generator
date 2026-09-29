import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_posts(raw_file_path , processed_file_path="data/processed_posts.json"):
    enriched_posts =[]
    with open(raw_file_path,encoding='utf-8') as file:
        posts=json.load(file)
        #print(posts)
        for post in  posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
            #post contains text,engagement
            #metadata contains linecount,language,tags
            #we pipe them togheer using | pipe operator
           #ie now our json has 5keys

        with open(processed_file_path, "w", encoding="utf-8" , errors="surrogatepass") as file:
            json.dump(enriched_posts, file, ensure_ascii=False, indent=4)

        print(enriched_posts[0])



def extract_metadata(post):
    #these will be done by an LLM,
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''
    prompt = PromptTemplate.from_template(template)
    parser = JsonOutputParser()
    chain = prompt | llm | parser


    return chain.invoke({"post":post})



if __name__ == "__main__":
    process_posts("data/raw_posts.json" , "data/processed_posts.json")
                                                                                                                                                                   