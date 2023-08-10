import os

import openai

class WriterGPT:

    def __init__(self):

        # setting models parameters
        self.writer_model = "gpt-3.5-turbo"
        self.response_num = 1
        self.max_tokens = 256 # when 150 -> 60moji miman
        self.stop_word = None
        self.response_randomness=0.5

        # rule for prompt
        self.system_role = "Settings {You are a WRITER who writes a nice diary.}"
        self.diary_title_flag = "- タイトルは必要ありません\n"
        self.prompt_limit_word_num="- 150文字以内で書いてください\n"
        self.content_only_flag = "- 本文のみを書くこと\n"

        self.prompt = ""

        self.OPENAI_APIKEY = os.environ.get("OPENAI_APIKEY")
        openai.api_key = self.OPENAI_APIKEY
    
    def facilities2str(self, req_dict):
        s = ""
        for i in req_dict["facilities"]:
            s += f"- {i}\n"
        return s

    def facilitieslist2str(self, req_list):
        s = ""
        for i in req_list:
            s += f"- {i}\n"
        return s

    def contact_chatgpt(self, question:str):
        res = openai.ChatCompletion.create(
                model=self.writer_model,
                messages=[
                    {"role": "user", "content": question},
                ],
            )
        return {"answer": res.choices[0]["message"]["content"].strip()}
        

    def write_memories(self, facilities_json):
        facilities_str = self.facilities2str(facilities_json)
        self.prompt = f"""
        以下の条件に基づいて、お出かけの日記を書いてください\n

        # 執筆ルール\n
        {self.diary_title_flag}
        {self.prompt_limit_word_num}
        {self.content_only_flag}

        # お出かけで行った場所\n
        {facilities_str}
        """
        writer = openai.ChatCompletion.create(
                    model=self.writer_model,
                    prompt=self.prompt,
                    max_tokens=self.max_tokens,
                    n = self.response_num,
                    stop=self.stop_word,
                    temperature=self.response_randomness
                )
        response = writer.choices[0].message.content
        return response
