from Bio import Entrez  # For interacting with PubMed's API
import csv  # For saving the results in CSV format
import argparse  # For parsing command-line arguments

# Set your email (replace with your own for production use)
Entrez.email = "testing7851@gmail.com"

# Function to search PubMed
def search_pubmed(query: str, max_results: int = 10):
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        return record["IdList"]
    except Exception as e:
        print(f"Error during search: {e}")
        return []

# Function to fetch article details
def fetch_details(id_list: list):
    try:
        ids = ",".join(id_list)
        handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        return records
    except Exception as e:
        print(f"Error during fetch: {e}")
        return []

# Function to extract required information
def extract_info(record) -> dict:
    try:
        pubmed_id = record.get("MedlineCitation", {}).get("PMID", "N/A")
        article = record.get("MedlineCitation", {}).get("Article", {})
        title = article.get("ArticleTitle", "N/A")
        pub_date = article.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "N/A")
        authors = article.get("AuthorList", [])

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "N/A"

        for author in authors:
            affiliation = author.get("AffiliationInfo", [{}])[0].get("Affiliation", "")
            if any(kw in affiliation.lower() for kw in ["pharma", "biotech", "inc", "ltd", "corp"]):
                name = f"{author.get('ForeName', '')} {author.get('LastName', '')}"
                non_academic_authors.append(name)
                company_affiliations.append(affiliation)
            if "@" in affiliation:
                corresponding_email = affiliation.split()[-1]

        return {
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Company Affiliation(s)": ", ".join(company_affiliations),
            "Corresponding Author Email": corresponding_email,
        }
    except Exception as e:
        print(f"Error extracting information: {e}")
        return {}

# Function to save results to CSV
def save_to_csv(data: list, filename: str = "pubmed_results.csv"):
    try:
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "PubmedID", "Title", "Publication Date", "Non-academic Author(s)",
                "Company Affiliation(s)", "Corresponding Author Email"
            ])
            writer.writeheader()
            writer.writerows(data)
            print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-m", "--max_results", type=int, default=10, help="Max number of results to fetch")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug information")

    args = parser.parse_args()

    if args.debug:
        print(f"Searching PubMed for: '{args.query}'")

    ids = search_pubmed(args.query, args.max_results)

    if args.debug:
        print(f"Found {len(ids)} articles. Fetching details...")

    if ids:
        records = fetch_details(ids)
        extracted_data = [extract_info(record) for record in records.get("PubmedArticle", [])]

        if args.file:
            save_to_csv(extracted_data, args.file)
        else:
            print(extracted_data)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
