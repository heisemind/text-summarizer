from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


class TextSummarizer:
    """
    A class for generating document summaries using Langchain.

    Attributes:
    - chunk_size (int): The size of document chunks for summarization.
    - chunk_overlap (int): The overlap between document chunks.

    Methods:
    - __init__(self, chunk_size: int = 6000, chunk_overlap: int = 500): Initialize the TextSummarizer.
    - load_file(self, file: str) -> str: Load text from a file.
    - load_prompt(prompt_name: str) -> PromptTemplate: Load a prompt template.
    - digest(self, file: str) -> tuple: Generate a document summary from a file.
    - get_title(self, summary: str) -> str: Extract the title from the summary.
    """

    def __init__(self, chunk_size: int = 6000, chunk_overlap: int = 500):
        """
        Initialize the TextSummarizer.

        Parameters:
        - chunk_size (int): The size of document chunks for summarization.
        - chunk_overlap (int): The overlap between document chunks.

        Returns:
        None
        """
        load_dotenv()
        self.llm = OpenAI(temperature=0, max_tokens=2500)
        self.splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ' ', ''],
            chunk_size=chunk_size,  # counted by character
            chunk_overlap=chunk_overlap
        )

    def load_file(self, file: str) -> str:
        """
        Load text from a file.

        Parameters:
        - file (str): The path to the file.

        Returns:
        str: The content of the file as a string.
        """
        with open(file, 'r') as f:
            text = f.read()
        print(f'Loaded {self.llm.get_num_tokens(text)} tokens.')
        return text

    @staticmethod
    def load_prompt(prompt_name: str) -> PromptTemplate:
        """
        Load a prompt template.

        Parameters:
        - prompt_name (str): The name of the prompt template.

        Returns:
        PromptTemplate: The loaded prompt template.
        """
        with open(f'prompts/{prompt_name}_prompt.txt', 'r') as f:
            prompt = f.read()
        prompt_template = PromptTemplate(
            template=prompt, input_variables=['text'])
        return prompt_template

    def digest(self, file: str) -> tuple:
        """
        Generate a document summary from a file.

        Parameters:
        - file (str): The path to the file.

        Returns:
        tuple: A tuple containing the title and summary of the document.
        """
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

    def get_title(self, summary: str) -> str:
        """
        Extract the title from the summary.

        Parameters:
        - summary (str): The document summary.

        Returns:
        str: The extracted title from the summary.
        """
        prompt = self.load_prompt('title')
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)
        return llm_chain.run(summary)


if __name__ == '__main__':
    text_summarizer = TextSummarizer()
    title, summary = text_summarizer.digest('bert_guide.txt')
    print(title)
    print(summary)
