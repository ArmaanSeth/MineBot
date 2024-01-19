# MineBot.In

## About

The primary purpose of MineBot.In is to provide accurate and reliable information regarding mining acts, rules, and regulations in India. The project leverages advanced natural language processing techniques to understand user queries and generate contextually relevant responses. It serves as a valuable resource for individuals, businesses, and organizations seeking information on mining-related legal frameworks in India.

<img src="https://raw.githubusercontent.com/ArmaanSeth/Images/main/MineBot1.png"/>

## Implementation
MineBot.In is an NLP (Natural Language Processing) project designed to answer questions related to mining acts, rules, and regulations in India. The project is implemented using Retrieval-Augmented Generation(RAG) architecture.

It is built using open-source resources such as Google's Gemini-Pro model, Instruct Embeddings, Cassandra VectorStore using DataStax platform, streamlit and langchain.


## Installation

To set up MineBot.In locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/ArmaanSeth/MineBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dataIngestion to add new data into vectorestore from the dir ./ChatbotDataset:
   ```bash
   python dataIngestion.py
   ```

## Usage

1. Start the streamlit application.
    ```bash
    streamlit run app.py
    ```

2. Input your mining-related question in natural language.

3. Receive contextually relevant answers based on the mining acts, rules, and regulations in India.

## Contributing

If you'd like to contribute to MineBot.In, please follow the [contributing guidelines](CONTRIBUTING.md) outlined in the repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Google Gemini: https://deepmind.google/technologies/gemini/#introduction

- Instructor Embeddings: https://huggingface.co/hkunlp/instructor-xl
-DataStax: https://www.datastax.com/

Feel free to reach out for any questions or feedback!

**Happy Mining!** 🚀