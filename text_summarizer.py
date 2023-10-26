from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


class TextSummarizer:
    def __init__(self, chunk_size=6000, chunk_overlap=500):
        load_dotenv()
        self.llm = OpenAI(temperature=0, max_tokens=2500)
        self.splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ' ', ''],
            chunk_size=chunk_size,  # counted by character
            chunk_overlap=chunk_overlap
        )

    def load_file(self, file):
        with open(file, 'r') as f:
            text = f.read()
        print(f'Loaded {self.llm.get_num_tokens(text)} tokens.')
        return text

    @staticmethod
    def load_prompt(prompt_name):
        with open(f'prompts/{prompt_name}_prompt.txt', 'r') as f:
            prompt = f.read()
        prompt_template = PromptTemplate(
            template=prompt, input_variables=['text'])
        return prompt_template

    def digest(self, file):
        text = self.load_file(file)
        docs = self.splitter.create_documents([text])

        summary_chain = load_summarize_chain(llm=self.llm,
                                             chain_type='map_reduce',
                                             combine_prompt=self.load_prompt(
                                                 'combine'),
                                             map_prompt=self.load_prompt(
                                                 'map'),
                                             verbose=True)

        summary = summary_chain.run(docs)
        title = self.get_title(summary)
        return title, summary

    def get_title(self, summary):
        prompt = self.load_prompt('title')
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)
        return llm_chain.run(summary)


if __name__ == '__main__':
    text_summarizer = TextSummarizer()
    title, summary = text_summarizer.digest('bert_guide.txt')
    print(title)
    print(summary)
