import logging
import azure.functions as func
import seek_data_processor_function.ProcessJobsMetaData as ProcessJobsMetaData
import seek_data_processor_function.ProcessJobDetails as ProcessJobDetails
import time

def main(seekDataProcessorTimer: func.TimerRequest) -> None:
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            if seekDataProcessorTimer.past_due:
                logging.info('The SeekDataProcessorTimer is past due!')

            logging.info('SeekDataProcessorTimer trigger function executed.')
            ProcessJobsMetaData.Start()
            ProcessJobDetails.Start()
            break  # Exit the loop if the function succeeds
        except Exception as e:
            logging.error(f'Attempt {attempt + 1} failed: {e}')
            if attempt < max_retries - 1:
                logging.info(f'Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)
            else:
                logging.error('Max retries reached. Failing the function.')
                raise