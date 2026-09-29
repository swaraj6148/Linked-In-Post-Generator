
import json
import pandas as pd

class FewShotPosts:

    def __init__(self,file_path="data/processed_posts.json"):
        self.df= None
        self.unique_tags=None
        self.load_posts(file_path)

    
    def load_posts(self,file_path):
        with open(file_path,encoding="utf-8") as file:
            posts=json.load(file)  #converts the json to a python object
            #print(type(posts)) its a list
            #print(posts[0])  every dictionary is a element in the list 

            self.df = pd.json_normalize(posts)  #returns us a pandas Dataframe (python object -> dataframe)
            #print(type(self.df))  its a pandas dataframe therfore we can do all operations on it as that on pandas dataframe
            #print(self.df)  similar to df.head() 


            self.df['length']=self.df['line_count'].apply(self.cate_length)
            #we made a new column named "length" in the dataframe 
            all_tags = self.df['tags'].apply(lambda x:x).sum()
            #print(type(all_tags)) #list
            #print(all_tags) #list

            self.unique_tags = set(all_tags) 
            #print(self.unique_tags)
            #print(len(self.unique_tags))
            #print(self.df.shape)
            #print(self.unique_tags)
    

    def cate_length(self,line_count):
        if line_count < 5:
            return "Short"
        elif 5<= line_count<=10:
            return "Medium"
        else:
            return "Long"


    def get_tags(self):
        return self.unique_tags
    

    def get_filtered_posts(self,length,language,tag):

        df_filtered=self.df[
            (self.df['language']==language) &
            (self.df['length']==length) &
            (self.df['tags'].apply(lambda tags:tag.lower() in [t.lower() for t in tags]))
        ]

        return df_filtered.to_dict(orient="records")
    


if __name__ == "__main__":
    fs=FewShotPosts()
    posts = fs.get_filtered_posts("Medium" , "English" , "JobSearch")
    #remaining functions in the FewShotPosts class are for its internal working 
    print(posts)


