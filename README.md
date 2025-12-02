# Agentic Workflow System

A multi-agent system for automated lead generation, enrichment, and personalized cold email outreach.

## Overview

This system uses a three-layer architecture:

1. **Directives Layer** - Defines what to do (objectives, processes, success criteria)
2. **Orchestration Layer** - AI decision-making and workflow coordination
3. **Execution Layer** - Deterministic tools and scripts

## Features

- 🔍 **Web Scraping** - Extract leads from target websites
- ✉️ **Contact Extraction** - Identify emails, phones, and social profiles
- ✅ **Lead Validation** - Verify email deliverability and quality
- 🎯 **Lead Enrichment** - Add tech stack, company data, and context
- 📧 **Email Generation** - Create personalized cold emails using AI
- 💾 **Data Storage** - Google Sheets and Supabase integration
- 🧠 **Self-Learning** - Continuous improvement from feedback

## Architecture

```
/agentic-workflow/
├── directives/          # What to do (AI reads these)
├── orchestration/       # Decision-making and routing
├── execution/           # Tools and scripts
├── .tmp/               # Temporary working files
├── tests/              # Test suite
└── config/             # Configuration and prompts
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd agentic-workflow

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for JavaScript-heavy sites)
playwright install
```

### Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env .env
```

2. Configure your environment variables:
```env
# Google Sheets
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# AI APIs (for email generation)
OPENAI_API_KEY=your_openai_key

# Notifications
NOTIFICATION_EMAIL=your@email.com
SLACK_WEBHOOK=your_slack_webhook
```

3. Edit `config/settings.yaml` for pipeline configuration

### Usage

#### Run Daily Scraping Workflow

```bash
python orchestrator.py --workflow orchestration/workflow_plans/daily_scrape_plan.yaml
```

#### Run Manual Lead Generation

```bash
python orchestrator.py --workflow orchestration/workflow_plans/lead_generation_plan.yaml --urls urls.txt
```

#### Run Self-Annealing Learner

```bash
python orchestrator.py --workflow orchestration/workflow_plans/self_annealing_plan.yaml
```

## Workflow Plans

### Daily Scrape Plan
- Automated daily scraping
- Runs at 2 AM via cron
- Processes up to 50 pages per site
- Stores results in Google Sheets

### Lead Generation Plan
- On-demand lead generation
- Higher quality thresholds
- Full enrichment pipeline
- Stores in Supabase

### Self-Annealing Plan
- Weekly learning cycle
- Analyzes feedback and corrections
- Updates prompts automatically
- A/B tests improvements

## Directives

Each directive defines a specific task:

- `scrape_website.md` - Web scraping guidelines
- `extract_contacts.md` - Contact extraction rules
- `validate_lead.md` - Lead validation criteria
- `enrich_lead.md` - Enrichment process
- `generate_email.md` - Email generation guidelines
- `store_to_sheets.md` - Google Sheets storage
- `migrate_to_supabase.md` - Database migration
- `learner_self_anneal.md` - Learning process
- `orchestrator_pipeline.md` - Pipeline coordination
- `errors_and_edge_cases.md` - Error handling

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Tools

1. Create script in `execution/<category>/`
2. Update `orchestration/agent_router.md`
3. Add tests in `tests/`
4. Update relevant directive

### Customizing Email Templates

Edit files in `config/prompts/`:
- `email_writer_prompt.txt` - Main email generation prompt
- `examples/email_examples.json` - Example emails for few-shot learning

## Docker Support

```bash
# Build image
docker-compose build

# Run pipeline
docker-compose up
```

## Monitoring

Logs are stored in `.tmp/error_logs/`

View execution metrics:
```bash
cat .tmp/metrics_report.json
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open a GitHub issue.

## Roadmap

- [ ] Add more enrichment sources
- [ ] Implement A/B testing framework
- [ ] Add email sending integration
- [ ] Build web dashboard
- [ ] Add more AI providers
- [ ] Implement rate limiting
- [ ] Add webhook support
