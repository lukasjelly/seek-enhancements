using System;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace SeekDataProcessor
{
    public class ProcessSeekData
    {
        private readonly ILogger _logger;
        private readonly SeekDataService _seekDataService;

        public ProcessSeekData(ILoggerFactory loggerFactory, SeekDataService seekDataService)
        {
            _logger = loggerFactory.CreateLogger<ProcessSeekData>();
            _seekDataService = seekDataService;
        }

        // ProcessSeekData function is triggered every day at midnight.
        [Function("ProcessSeekData")]
        public async Task Run([TimerTrigger("0 0 * * *")] TimerInfo myTimer)
        {
            _logger.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");

            if (myTimer.ScheduleStatus is not null)
            {
                _logger.LogInformation($"Next timer schedule at: {myTimer.ScheduleStatus.Next}");
            }

            // Fetch and process classification data. If any has changed, update the data in the database.
            await _seekDataService.FetchAndProcessDataAsync();
        }
    }
}
