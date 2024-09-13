# pptGEN - Generating Lecture Slides on-the-fly!

An open-source project initiated during a research fellowship on Lecture Presentation Understanding at IIIT Hyderabad.

![Demo GIF](https://raw.githubusercontent.com/NerdyVisky/pptGEN-dev/main/teaser.gif)

## Overview

**pptGEN** is an executable application designed to generate lecture slides within 15 seconds, synchronizing with live speech from the professor. This project utilizes advanced technologies such as Large Language Models (LLMs) to craft coherent multimodal content, automatically assigns appropriate slide layouts, and preserves the overall presentation style across the generated slides.

### Key Features:
- **Real-time Slide Generation:** Produces lecture slides on-the-fly as the speaker presents.
- **Modular Pipeline:** A lightweight and modular architecture for efficient content generation and slide layout assignment.
- **Style Preservation:** Ensures that each slide maintains a consistent design and layout.
  
### Technologies Used:
- `python-pptx` (for slide generation)
- `Deepgram API` (for real-time speech-to-text transcription)
- `OpenAI Embeddings` (for generating relevant content from transcriptions)
- `Python`, `Bash` (core logic and automation)

## Installation Guide

Follow these steps to set up the project on your local machine:

### Prerequisites
- Python 3.7 or above
- Windows OS
- Microsoft Office (Atleast PowerPoint)
- `pip` for package management (>19.x)

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/pptGEN-dev.git
   cd pptGEN-dev
   ```
2. **Make a Python Virtual Environment (Optional)**
   ```bash
   python3 -m venv pptgen
   path/to/env/Scripts/Activate.bat
   ```
3. **Install the Dependencies using the requirements.txt file**
   ```bash
   pip install -r requirements.txt
   ```
4. **Make a .env file and add your API keys (Copy the following for reference)**
   ```python
   DEEPGRAM_API_KEY=<insert-your-deepgram-key-here>
   OPENAI_API_KEY=<insert-your-api-key-here>
   ```
   (BONUS: You can adjust the Deepgram and OpenAI models from transcripter.py and content_generator.py files respectively)
5. **Run the following script in Powershell**
   ```bash
   .\run.ps1 -slide <slide-number> [-topic <topic-name>]
   ```
   \[] Denotes optional argument
6. **WOHOO! YOU ARE ALL SET! Get creative and generate your presentations!**

## Contributing

We welcome contributions from the community to help improve **pptGEN**! Here’s how you can get involved:

1. **Fork the repository:**
   - Click the 'Fork' button at the top-right corner of this repository's page.
   - Clone your forked repository locally:
     ```bash
     git clone https://github.com/your-username/pptGEN.git
     ```

2. **Create a new branch:**
   - Use a descriptive name for your branch that summarizes the changes you plan to make:
     ```bash
     git checkout -b feature/your-feature-name
     ```

3. **Make changes:**
   - Implement your feature or fix the bug. Make sure your code is clean and adheres to the project style guide.

4. **Commit and push:**
   - After testing your changes, commit them:
     ```bash
     git commit -m "Descriptive message about your changes"
     ```
   - Push your branch to your forked repository:
     ```bash
     git push origin feature/your-feature-name
     ```

5. **Open a pull request:**
   - Go to the original repository and click 'New Pull Request.' Submit a pull request with a detailed description of your changes. We’ll review and provide feedback.

## Code of Conduct

We aim to create a welcoming and inclusive community. To that end, please:

- Be respectful and considerate in all discussions.
- Avoid offensive language, harassment, or discrimination based on gender, race, or background.
- Provide constructive feedback in code reviews and avoid personal attacks.
- Respect differing viewpoints and understand that collaboration is key to project success.

By contributing, you agree to follow these guidelines and foster a positive environment for all contributors.

## License

This project is licensed under the **GNU Affero General Public License v3.0**. The full license text is in the [LICENSE](https://www.gnu.org/licenses/agpl-3.0.en.html#license-text) file.

The AGPLv3 license ensures that any modifications to this project deployed in a network environment must be shared with the community under the same license, fostering collaboration and improvement across the ecosystem.



