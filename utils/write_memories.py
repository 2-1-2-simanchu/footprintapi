import os
import re
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
        self.diary_title_need = "- タイトルは必要ありません\n"
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

    def remove_space(self, sentence:str)->str:
        return sentence.replace(" ", "")

    def pickup_contents(self, sentence:str, label:str, end_flag=False)-> str:
        if end_flag == True:
            pickup_pattern = r"" + label + r"(.*)$"
        else:
            pickup_pattern = r"" + label + r"(.*)\n"

        match = re.search(pickup_pattern, sentence)
        if match:
            pickuped_sentence = match.group(1)
        else:
            pickuped_sentence = None
        return pickuped_sentence

    def write_memories(self, facilities_list):
        facilities_str = self.facilitieslist2str(facilities_list)
        self.prompt = f"""
        以下の条件に基づいて、お出かけの日記を書いてください\n

        # 執筆ルール\n
        {self.diary_title_need}
        {self.prompt_limit_word_num}
        {self.content_only_flag}

        # お出かけで行った場所\n
        {facilities_str}
        """.replace(" ", "")
        writer = openai.ChatCompletion.create(
                    model=self.writer_model,
                    messages=[
                        {"role": "system", "content": self.system_role},
                        {"role": "user", "content": self.prompt},
                    ],
                    max_tokens=self.max_tokens,
                    n = self.response_num,
                    stop=self.stop_word,
                    temperature=self.response_randomness
                )
        response = writer.choices[0].message.content
        return response

    def write_memories_with_title(self, facilities_list):
        """
        you need in main.py:
            - class DiaryWtModel(BaseModel)
                title: str
                diary: str
            
        """
        facilities_str = self.facilitieslist2str(facilities_list)
        self.prompt = f"""
        以下の条件に基づいて、お出かけの日記を書いてください\n

        # 執筆ルール\n
        - titleは30文字以内で書いてください、そして改行はしないでください
        - diaryは150文字以内で書いてください、そして改行はしないでください
        - 以下で決められた「出力形式」に従う\n

        # お出かけで行った場所\n
        {facilities_str}

        # 出力形式

        title:「#お出かけで行った場所」の要素から考えた、お出かけの素敵な概要
        diary:「#お出かけで行った場所」の内容を用いた日記

        """.replace(" ", "")

        # 「素敵な」をつけるだけで全然違う
        # title: 「お出かけで行った場所」からお出かけのタイトルを考えて[title]に設定する
        # diary: 「お出かけで行った場所」を使って、日記を考えて[diary]に設定する

        print(self.prompt)
        writer = openai.ChatCompletion.create(
                    model=self.writer_model,
                    messages=[
                        {"role": "system", "content": self.system_role},
                        {"role": "user", "content": self.prompt},
                    ],
                    max_tokens=self.max_tokens,
                    n = self.response_num,
                    stop=self.stop_word,
                    temperature=self.response_randomness
                )
        response = writer.choices[0].message.content
        response_nospace = self.remove_space(response)
        title_content = self.pickup_contents(response_nospace, "title:")
        diary_content = self.pickup_contents(response_nospace, "diary:", end_flag=True)
        return {"title": title_content, "diary": diary_content}