# Known AI crawler / agent user-agent tokens, as used in robots.txt.
# Kept as a single source of truth so audit.py and fix.py never drift apart.
# Sources: each vendor's own published crawler docs (OpenAI, Anthropic,
# Perplexity, Google, Common Crawl, ByteDance, Amazon, Apple, Cohere, Meta).

AI_CRAWLERS = {
    "GPTBot": "OpenAI — trains/improves models on crawled content",
    "ChatGPT-User": "OpenAI — fetches pages a ChatGPT user links to",
    "OAI-SearchBot": "OpenAI — powers ChatGPT search result citations",
    "ClaudeBot": "Anthropic — trains/improves Claude on crawled content",
    "Claude-Web": "Anthropic — fetches pages referenced in a Claude chat",
    "anthropic-ai": "Anthropic — legacy training crawler token",
    "PerplexityBot": "Perplexity — indexes content for AI search answers",
    "Perplexity-User": "Perplexity — fetches pages a user asked about",
    "Google-Extended": "Google — controls use in Gemini / AI Overviews (separate from Googlebot)",
    "CCBot": "Common Crawl — public dataset used to train many LLMs",
    "Bytespider": "ByteDance — crawls for AI training",
    "Amazonbot": "Amazon — crawls for Alexa/AI features",
    "Applebot-Extended": "Apple — controls use in Apple Intelligence (separate from Applebot)",
    "cohere-ai": "Cohere — trains/improves models on crawled content",
    "Meta-ExternalAgent": "Meta — crawls for AI training and search features",
    "Diffbot": "Diffbot — powers third-party AI/knowledge-graph products",
    "YouBot": "You.com — indexes content for AI search answers",
}
