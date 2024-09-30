# Seek Enhanced Search

This project provides a set of Python scripts to fetch job listings from Seek.co.nz, extract job details, and filter jobs based on specific criteria.

## Files

- `SeekEnhancedSearch.py`: Main script containing functions to fetch job IDs, get job details, and query jobs based on specific keywords.

## Requirements

- Python 3.x
- `requests` library

You can install the required library using pip:
```sh
pip install requests
```

## Usage
### Fetch Job IDs
The getJobIds function fetches job IDs from Seek.co.nz based on predefined query parameters and saves them to output/jobIds.txt.

### Get Job Details
The getJobDetails function reads job IDs from output/jobIds.txt, fetches detailed information for each job, and saves the details to output/jobDetails.json.

### Query Jobs
The queryJobs function filters jobs based on specific keywords and saves the filtered jobs to output/foundJobs.json.

## Running the Script
You can run the script by uncommenting the desired function calls in the ```__main__ ```section of SeekEnhancedSearch.py and executing the script as follows:     
```sh
python SeekEnhancedSearch.py
```


## Logging
The script logs information to the following files:

- logging/jobIds.log: Logs related to fetching job IDs.
- logging/jobDetails.log: Logs related to fetching job details.
### Example
To fetch job IDs, get job details, and query jobs, you can modify the __main__ section as follows:
```python
if __name__ == "__main__":
    # Fetch job IDs
    # getJobIds()

    # Get job details
    # getJobDetails()

    # Query jobs
    queryJobs()
```

Then run the script:
```sh
python SeekEnhancedSearch.py
```