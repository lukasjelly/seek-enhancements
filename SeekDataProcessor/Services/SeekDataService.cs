using System;
using System.Diagnostics;
using System.Net;
using System.Security.Policy;
using System.Text.Json;
using System.Threading.Tasks;
using Azure;
using Microsoft.Extensions.Logging;
using ShellProgressBar;

namespace SeekDataProcessor
{
    public class SeekDataService
    {
        private readonly ILogger _logger;

        public SeekDataService(ILogger<SeekDataService> logger)
        {
            _logger = logger;
        }

        public async Task FetchAndProcessDataAsync()
        {
            _logger.LogInformation("Fetching location, classification, and work-type data...");

            // Simulate fetching data
            var data = await FetchAndProcessMetaDataAsync();

            // Process the data
            var hasChanged = ProcessData(data);

            if (hasChanged)
            {
                _logger.LogInformation("Data has changed, updating the database...");
                await UpdateDatabaseAsync(data);
            }
            else
            {
                _logger.LogInformation("No changes detected in the data.");
            }
        }

        private async Task<string> FetchAndProcessMetaDataAsync()
        {
            var url = "https://jobsearch-api-ts.cloud.seek.com.au/v4/counts?siteKey=NZ-Main&sourcesystem=houston&userid=b75b2db1-191b-4ea3-98f7-f8f488fd6359&usersessionid=b75b2db1-191b-4ea3-98f7-f8f488fd6359&eventCaptureSessionId=b75b2db1-191b-4ea3-98f7-f8f488fd6359&where=All+New+Zealand&page=1&seekSelectAllPages=true&include=seodata&locale=en-NZ";
            var client = new HttpClient();
            var response = await client.GetAsync(url);
            var data = await response.Content.ReadAsStringAsync();
            var jsonData = JsonDocument.Parse(data);
            await ProcessClassificationDataAsync(jsonData);
            return data;
        }

        private async Task ProcessClassificationDataAsync(JsonDocument jsonData)
        {
            var allClassificationIds = new List<string>();
            var mainClassifications = new List<Dictionary<string, string>>();
            var subClassifications = new List<Dictionary<string, string>>();

            ExtractClassificationIdsFromJson(jsonData, allClassificationIds);

            using (var progressBar = new ProgressBar(allClassificationIds.Count, "Fetching classification labels"))
            {
                await FetchClassificationLabels(allClassificationIds, mainClassifications, subClassifications, progressBar);
            }

            MapMainClassificationIds(mainClassifications, subClassifications);

            // output the main classifications and sub classifications as json file
            var mainClassificationsJson = JsonSerializer.Serialize(mainClassifications);
            var subClassificationsJson = JsonSerializer.Serialize(subClassifications);
            await File.WriteAllTextAsync("mainClassifications.json", mainClassificationsJson);
            await File.WriteAllTextAsync("subClassifications.json", subClassificationsJson);
        }

        private static void MapMainClassificationIds(List<Dictionary<string, string>> mainClassifications, List<Dictionary<string, string>> subClassifications)
        {
            foreach (var subClassification in subClassifications)
            {
                foreach (var mainClassification in mainClassifications)
                {
                    if (subClassification["mainClassification"] == mainClassification["label"])
                    {
                        subClassification["mainClassificationId"] = mainClassification["id"];
                        break;
                    }
                }
            }
        }

        private static async Task FetchClassificationLabels(List<string> allClassificationIds, List<Dictionary<string, string>> mainClassifications, List<Dictionary<string, string>> subClassifications, ProgressBar progressBar)
        {
            var client = new HttpClient();
            foreach (var classificationId in allClassificationIds)
            {
                var url = $"https://www.seek.co.nz/jobs?classification={classificationId}";
                var response = await client.GetAsync(url);
                var redirectedUrl = response.RequestMessage?.RequestUri?.ToString() ?? string.Empty;

                if (url != redirectedUrl)
                {
                    var mainClassification = redirectedUrl.Split('/').Last();
                    mainClassifications.Add(new Dictionary<string, string>
                            {
                                { "id", classificationId },
                                { "label", mainClassification }
                            });
                }
                else
                {
                    url = $"https://www.seek.co.nz/jobs?subclassification={classificationId}";
                    response = await client.GetAsync(url);
                    redirectedUrl = response.RequestMessage?.RequestUri?.ToString() ?? string.Empty;

                    var subClassification = redirectedUrl.Split('/').Last();
                    var mainClassification = redirectedUrl.Split('/').Reverse().Skip(1).First();
                    subClassifications.Add(new Dictionary<string, string>
                            {
                                { "id", classificationId },
                                { "label", subClassification },
                                { "mainClassification", mainClassification }
                            });
                }

                progressBar.Tick();
            }
        }

        private static void ExtractClassificationIdsFromJson(JsonDocument jsonData, List<string> allClassificationIds)
        {
            foreach (var item in jsonData.RootElement.GetProperty("counts").EnumerateArray())
            {
                if (item.GetProperty("name").GetString() == "classification")
                {
                    foreach (var classificationItem in item.GetProperty("items").EnumerateArray())
                    {
                        allClassificationIds.Add(classificationItem.GetString());
                    }
                    break;
                }
            }
        }

        private bool ProcessData(string data)
        {
            // Simulate processing data and checking for changes
            // Return true if data has changed, otherwise false
            return !string.IsNullOrEmpty(data);
        }

        private Task UpdateDatabaseAsync(string data)
        {
            // Simulate updating the database with the new data
            _logger.LogInformation("Database updated with new data: {data}", data);
            return Task.CompletedTask;
        }
    }
}
