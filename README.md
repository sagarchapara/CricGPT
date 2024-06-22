# CricGPT
Advanced Cricket Stats with Natural Language Queries

## What It Does

CricGPT makes it easy to get advanced cricket statistics using natural language queries, leveraging [Statsguru](https://stats.espncricinfo.com/ci/engine/stats/index.html). Whether you need simple player stats or complex comparisons across countries and opponents, CricGPT has you covered. Here’s what you can do with CricGPT:

- **Planner-Based Query Handling:** Breaks down complex queries into simpler ones, executes them, and combines the results into a neat table.
- **Comparative Analysis:** Compare team or player data across different years and countries with just a simple query.
- **Multiple Player Comparisons:** Compare multiple players side by side.
- **Name Handling:** Recognizes player name variations, including misspellings and abbreviations like "SKY" (Suryakumar Yadav) and "JFM" (Jake Fraser-McGurk).
- **Extra Info:** Provides a Cricinfo link to your search query for more details or to catch any mistakes made by the model.

## Demo

https://github.com/sagarchapara/CricGPT/assets/35074365/0c204834-bc80-471c-aeac-e1c77604bab2


## Getting Started

### Client

1. **Navigate to the client directory:**
   ```sh
   cd client
   ```

2. **Install dependencies:**
   ```sh
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Run the client:**
   ```sh
   npm run dev
   # or
   yarn run dev
   # or
   pnpm dev
   ```

### Server

1. **Navigate to the server directory:**
   ```sh
   cd server
   ```

2. **Install required packages:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Create a `.env` file based on the provided `.env_sample`.
   - Update the `.env` file with your OpenAI key and endpoints.

4. **Start the server:**
   ```sh
   python -m uvicorn app:app --reload --env-file .env
   ```

## Contributing

If you like CricGPT, please give it a star! Your help in making CricGPT even better is always welcome.

- **Raise an Issue:** Spotted a bug or have a cool feature idea? [Open an issue](https://github.com/sagarchapara/CricGPT/issues).

## License

CricGPT is released under the MIT License. See the [LICENSE](LICENSE) file for more information.

## FAQ

### How do I get my OpenAI key?
You can get your OpenAI key by signing up on the [OpenAI website](https://platform.openai.com/docs/quickstart).
