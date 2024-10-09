import logging
import azure.functions as func
import seek_data_processor_function.Jobs as Jobs

def main(seekDataProcessorTimer: func.TimerRequest) -> None:
    if seekDataProcessorTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    Jobs.ProcessJobsMetaData()