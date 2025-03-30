# PubMed Research Paper Fetcher

This script fetches research papers from PubMed based on a given search query, extracts relevant details, and saves them in a CSV file.

## Features

- Searches PubMed for research papers
- Fetches details like title, publication date, and authors
- Identifies non-academic authors with company affiliations
- Extracts corresponding author email if available
- Saves results to a CSV file

## Prerequisites

- Python 3.x
- Required dependencies:
  ```sh
  pip install biopython
  ```

## Installation

Clone this repository and navigate to the project folder:

```sh
git clone https://github.com/your-repo/pubmed-fetcher.git
cd pubmed-fetcher
```

## Usage

Run the script using the command line:

```sh
python pubmed_fetch.py "your search query" -m 10 -f output.csv
```

### Arguments

- `query` (required): Search term for PubMed.
- `-m, --max_results` (optional): Maximum number of results to fetch (default: 10).
- `-f, --file` (optional): Output CSV filename.
- `-d, --debug` (optional): Enable debug information.

### Example

```sh
python pubmed_fetch.py "cancer treatment" -m 5 -f results.csv -d
```

## Output

The extracted data will be saved in the specified CSV file with the following columns:

- PubmedID
- Title
- Publication Date
- Non-academic Author(s)
- Company Affiliation(s)
- Corresponding Author Email

## Troubleshooting

- If no results are found, try a broader search query.
- Ensure you have a stable internet connection.
- Check if PubMed's API is accessible.

## License

This project is licensed under the MIT License.
