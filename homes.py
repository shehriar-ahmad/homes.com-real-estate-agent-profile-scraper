import argparse
import csv
import time
from datetime import datetime
from lxml import html
import requests


class HomesAgentScraper:
    BASE_URL = "https://www.homes.com"

    def __init__(self, search_url):
        self.search_url = search_url

    def get_agent_urls(self, page=1):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        url = f"{self.search_url}/p{page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            agent_links = tree.cssselect('ul#agent-results-container a.agent-placard-link')
            agent_urls = [self.BASE_URL + link.get('href') for link in agent_links]
            return agent_urls
        else:
            print(f"Error accessing page {page}.")
            return []

    def extract_info(self, container, keyword):
        for element in container:
            info_bold_elements = element.cssselect('div.info-bold')
            if info_bold_elements:
                for info_bold_element in info_bold_elements:
                    if keyword.lower() in info_bold_element.text_content().lower():
                        info_light_elements = info_bold_element.cssselect('span.info-light')
                        if info_light_elements:
                            info = info_light_elements[0].text.strip()
                            return info
        return "N/A"

    def scrape_agent_profile(self, agent_url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(agent_url, headers=headers)
        if response.status_code == 200:
            tree = html.fromstring(response.content)

            # Extracting Agent Profile Details
            name_element = tree.cssselect('span.name.js-agent-name')
            name = name_element[0].text.strip() if name_element else "N/A"

            location_elements = tree.cssselect('div.location')
            location = location_elements[0].text.strip() if location_elements else "N/A"

            office_name_elements = tree.cssselect('div.office-name')
            office_name = office_name_elements[0].text.strip() if office_name_elements else "N/A"

            phone_elements = tree.cssselect('div.phone a.text-only')
            phone = phone_elements[0].text.strip() if phone_elements else "N/A"

            quick_info_container = tree.cssselect('div.quick-info-container')

            home_types = self.extract_info(quick_info_container, "Home Types:")
            languages_spoken = self.extract_info(quick_info_container, "Languages Spoken:")
            years_of_experience = self.extract_info(quick_info_container, "Years of Experience:")

            social_container = tree.cssselect('main#mainContent div.social-container')
            if social_container:
                website_element = social_container[0].cssselect('a.text-only.website-link')
                website = website_element[0].get('href') if website_element else "N/A"

                social_links = social_container[0].cssselect('a.text-only.social-link')
                social_media = {
                    "Facebook": "N/A",
                    "Instagram": "N/A",
                    "Twitter": "N/A",
                    "LinkedIn": "N/A",
                    "Tiktok": "N/A",
                    "Pinterest": "N/A"
                }
                for link in social_links:
                    aria_label = link.get('aria-label')
                    if "Facebook" in aria_label:
                        social_media["Facebook"] = link.get('href')
                    elif "Instagram" in aria_label:
                        social_media["Instagram"] = link.get('href')
                    elif "Twitter" in aria_label:
                        social_media["Twitter"] = link.get('href')
                    elif "Linked In" in aria_label:
                        social_media["LinkedIn"] = link.get('href')
                    elif "TikTok" in aria_label:
                        social_media["Tiktok"] = link.get('href')
                    elif "Pinterest" in aria_label:
                        social_media["Pinterest"] = link.get('href')
            else:
                website = "N/A"
                social_media = {
                    "Facebook": "N/A",
                    "Instagram": "N/A",
                    "Twitter": "N/A",
                    "LinkedIn": "N/A",
                    "Tiktok": "N/A",
                    "Pinterest": "N/A"
                }

            agent_details = {
                "Name": name,
                "Location": location,
                "Office Name": office_name,
                "Phone": phone,
                "Home Types": home_types,
                "Languages Spoken": languages_spoken,
                "Years of Experience": years_of_experience,
                "Website": website,
                **social_media,
                "Agent Profile URL": agent_url
            }

            return agent_details

        else:
            print("Error accessing the agent profile page.")
            return {}

    def scrape_agent_profiles(self, num_pages=20, num_results=30):
        start_time = datetime.now()
        print("Homes.com Agent Profile Scraper")
        print("Created by Shehriar Ahmad Awan")
        print("twitter.com/ahmad_shehriar")
        print("---------------------------------")
        print("Scraping started:", start_time)
        print("---------------------------------")

        with open("agent_profiles.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "Number",
                "Name",
                "Location",
                "Office Name",
                "Phone",
                "Home Types",
                "Languages Spoken",
                "Years of Experience",
                "Website",
                "Facebook",
                "Instagram",
                "Twitter",
                "LinkedIn",
                "Tiktok",
                "Pinterest",
                "Agent Profile URL"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            completed_successfully = True
            try:
                page_count = 0
                profile_count = 0

                while page_count < num_pages:
                    page_count += 1
                    agent_urls = self.get_agent_urls(page_count)
                    if not agent_urls:
                        print(f"No agent URLs found on page {page_count}.")
                        continue

                    for i, agent_url in enumerate(agent_urls, start=1):
                        if i > num_results:
                            break
                        agent_details = self.scrape_agent_profile(agent_url)
                        agent_details["Number"] = profile_count + i
                        writer.writerow(agent_details)
                        print(f"Profile {profile_count + i} on page {page_count} scraped")
                        time.sleep(0.2)

                    profile_count += len(agent_urls)

                    if profile_count >= num_results:
                        break

                    print(f"Scraping page {page_count} completed.")
                    time.sleep(1)  # Sleep for 1 second between pages

            except KeyboardInterrupt:
                end_time = datetime.now()
                elapsed_time = end_time - start_time
                print("---------------------------------")
                print("Scraping interrupted by user.")
                print("Scraping stopped:", end_time)
                print("Total elapsed time:", elapsed_time)
                print("---------------------------------")
                completed_successfully = False

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("---------------------------------")
        if completed_successfully:
            print("Scraping completed successfully.")
        else:
            print("Scraping interrupted.")
        print("Scraping stopped:", end_time)
        print("Total elapsed time:", elapsed_time)
        print("---------------------------------")


def main():
    parser = argparse.ArgumentParser(description="Homes.com Agent Scraper")
    parser.add_argument("search_url", type=str, help="URL of the search page")
    parser.add_argument("--num-pages", "-p", type=int, default=20, help="Number of pages to scrape")
    parser.add_argument("--num-results", "-r", type=int, default=30, help="Number of results to scrape per page")
    args = parser.parse_args()

    search_url = args.search_url
    num_pages = args.num_pages
    num_results = args.num_results

    scraper = HomesAgentScraper(search_url)
    scraper.scrape_agent_profiles(num_pages, num_results)


if __name__ == "__main__":
    main()
