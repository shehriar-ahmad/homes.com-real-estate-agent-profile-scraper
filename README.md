# Homes.com Agent Scraper
Scrape Real Estate Agent Profiles with 15 Data Attributes from Homes.com using a search URL only

The **Homes.com Agent Scraper** is a Python script that allows you to extract valuable information about real estate agents listed on Homes.com. It automates the process of visiting agent profiles, extracting relevant details, and saving the data in a CSV file for further analysis or use.

## Data Attributes Scraped

The scraper extracts the following data attributes from each agent's profile:

- **Name:** The name of the real estate agent.
- **Location:** The location or area of operation of the agent.
- **Office Name:** The name of the real estate office the agent is affiliated with.
- **Phone:** The contact phone number of the agent.
- **Home Types:** The types of homes or properties the agent specializes in.
- **Languages Spoken:** The languages spoken by the agent.
- **Years of Experience:** The number of years of experience the agent has in the real estate industry.
- **Website:** The agent's website (if available).
- **Social Media Links:** Links to the agent's social media profiles on platforms like Facebook, Instagram, Twitter, LinkedIn, TikTok, and Pinterest.
- **Agent Profile URL:** The URL of the agent's profile on Homes.com.

## Prerequisites and Requirements

Before using the scraper, make sure you have the following prerequisites and requirements set up:

1. **Python:** The script requires Python 3 to be installed on your system.

2. **Libraries:** Install the required libraries by running the following command:
   ```
   pip install argparse csv lxml requests
  
   ```

## How to Use the Script

Follow the steps below to use the Homes.com Agent Scraper:

1. Clone the repository to your local machine or download the `homes.py` file.

2. Open your terminal or command prompt and navigate to the directory containing the `homes.py` file.

3. Run the scraper using the following command:
   ```
   python homes.py <search_url>
   ```
   
   - Replace `<search_url>` with the URL of the Homes.com search page for real estate agents in your desired location.
   - Optionally, you can specify the number of pages to scrape using the `--num-pages` or `-p` flag. The default value is 20. You can also specify number of results to scrape per page using the `--num-results` or `-r` flag.
   - Example Usage:
     ```
     python homes.py https://www.homes.com/real-estate-agents/houston-tx
     ```
     ```
     python homes.py https://www.homes.com/real-estate-agents/houston-tx -p 10 -r 15
     ```

5. The script will start scraping the agent profiles and save the data in a CSV file named `agent_profiles.csv`.

## Ethical Usage Disclaimer

This script is intended for educational and research purposes only. Scraping websites may raise legal and ethical concerns. Before using the script, ensure that you have the right to access and extract data from the targeted website. Respect the website's terms of service, robots.txt file, and any applicable laws and regulations.

The developer and contributors of this script are not responsible for any misuse or illegal activities performed with the scraper.

## Free and Open Source

The Homes.com Agent Scraper is free and open-source software released under the [MIT License](LICENSE). You are free to use, distribute, and modify this script according to the terms of the license.

---

Feel free to customize this content as per your project requirements. Make sure to update the `<search_url>` placeholder with an actual URL where users can provide the search parameters. Additionally, include any specific instructions for using or contributing to the project if needed.
