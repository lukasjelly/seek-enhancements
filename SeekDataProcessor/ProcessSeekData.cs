using System;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace SeekDataProcessor
{
    public class ProcessSeekData
    {
        private readonly ILogger _logger;

        public ProcessSeekData(ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger<ProcessSeekData>();
        }

        [Function("ProcessSeekData")]
        public void Run([TimerTrigger("0 */5 * * * *")] TimerInfo myTimer)
        {
            _logger.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");
            
            if (myTimer.ScheduleStatus is not null)
            {
                _logger.LogInformation($"Next timer schedule at: {myTimer.ScheduleStatus.Next}");
            }

            // Fetch and process classification data. If any has changed, update the data in the database.

        }
    }
}
