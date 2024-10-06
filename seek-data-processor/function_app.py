import logging
import azure.functions as func
import Jobs

app = func.FunctionApp()

@app.function_name(name="ProcessSeekData")
@app.schedule(schedule="0 0 0 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def ProcessSeekData(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    Jobs.ProcessJobsMetaData()