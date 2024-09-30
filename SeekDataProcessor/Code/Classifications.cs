using Microsoft.Extensions.Logging;

namespace Classifications
{
    class Classifications
    {
        private readonly ILogger _logger;

        public Classifications(ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger<Classifications>();
        }

        public static string[] GetClassifications()
        {
            return new string[] { "A", "B", "C" };
        }
    }

}