# Child Story Generation Web Application #

## Overview

This web application generates customized children’s stories using a Large Language Model (LLM) provided by Mistral AI. Users can personalize stories by specifying the names of characters, story’s theme and many more. The application ensures that stories are appropriate, adhering to given preferences and includes input/output safety measures.

## Technology Stack
- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript
- **LLM:** Mistral AI (Mixtral-8x7B-Instruct-v0.1)
- **Database:** SQLite
- **Server:** Uvicorn
- **Testing:** Unittest (Python)

## Installation
1. **Clone the repository:** `git clone https://git.fim.uni-passau.de/alimzade/week-2-aie-lab.git`
2. **Navigate to the directory:** `cd week-2-aie-lab`
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Create a `.env` file:** Create a file named `.env` in the root directory of your project with the following content:

    ```plaintext
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASS=
    DB_NAME=storybook
    PORT=3001
    JWT_SECRET=adafiandasdaskdnasl
    API_URL="api_url_here"
    API_KEY="api_key_here"
    SECRET_KEY="random"
    ```
5. **Run the application:** `python -m uvicorn main:app --reload`

## Features

### Core Functionality

- **Story Customization:**
  - **Protagonist’s Name:** Specify the name of main character of the story.
  - **Protagonist’s Gender:** Specify the gender of the main character of the story.
  - **Friend’s Name:** Specify the name of main character's friend in the story.
  - **Friend’s Gender:** Specify the gender of the friend of main character of the story.
  - **Story Theme:** Provide the general idea or plot of the story.
  - **Age-Group:** Specify the targeted age group of story reader.
  - **Educational Content:** Specify the targeted age group of story reader.
  - **Story Description:** Provide brief description of story.
  - **Story Length:** Provide range for length of the story.
  - **Favorites:** Use bullet points from favorite stories for generating a new one.


- **Validation:**
    - Ensure input data is valid, with automatic rephrasing if inappropriate text is detected.
  - Ensure output data is valid.
  - Guarantee that generated stories adhere to specified name, gender, theme, length etc.

- **User Interaction:**
  - Users provide details through multiple input fields to generate customized stories.

- **Testing:**
  - Run tests: `python -m unittest discover tests`

### Enhancements

- **User Accounts:**
  - Allow users to register and log in.
  - Users can mark/unmark stories as favorites.
  - View a list of favorite stories.
  - View all past generated stories.

- **Preference Summarization:**
  - Analyze favorite stories, extract bullet points to refine system prompt for future story generations.


## Example

### Input

- **Protagonist’s Name:** Alice
- **Protagonist’s Gender:** Female
- **Friend’s Name:** Max
- **Friend’s Gender:** Male
- **Story Theme:** Adventure
- **Educational Content:** Friendship
- **Story Length:** Short (50-250 words)

### Output

 In the heart of Sunnytown, where flowers bloomed year-round, lived a brave girl named Alice, and her curious friend, Max. They were inseparable, sharing dreams, laughter, and even adventures!

One day, Alice discovered an ancient map in her grandmother's attic, hinting at a hidden waterfall nearby. Seeing this as an opportunity for a grand adventure, she shared the news with Max. Their eyes sparkled with excitement, and they agreed to explore the mysterious waterfall together.

The journey led them through dense forests and bubbling brooks. Along the way, they encountered various challenges, like a narrow bridge and a mischievous monkey. But each hurdle only strengthened their bond, as they learned the value of cooperation, communication, and trust.

At last, they arrived at the splendid waterfall, feeling a sense of accomplishment. As water droplets kissed their faces, Alice turned to Max. "We make a great team, don't we?" she asked. Max grinned, "Absolutely, Alice! Adventures are always better with a friend by your side."

Through this journey, Ada and Max not only discovered a magical waterfall but also realized that true friendship meant working together, helping one another, and celebrating shared victories. And that was the greatest adventure of all!