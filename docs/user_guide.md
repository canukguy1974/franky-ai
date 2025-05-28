# AI Agent User Guide

## Introduction

This document provides comprehensive instructions for deploying and using the autonomous AI agent system designed to find small business clients, close deals, and deliver services without human intervention. The system consists of three primary modules working in concert to create a complete business development and service delivery pipeline.

## System Overview

The AI agent is a modular system with three core components:

1. **Client Discovery Module**: Autonomously identifies and qualifies potential small business clients.
2. **Deal Closing Module**: Engages with prospects, negotiates terms, and converts them into paying clients.
3. **Service Delivery Module**: Performs the actual work required by clients, delivering high-quality results.

## Deployment Instructions

### System Requirements

- **Server Environment**: Linux-based server with minimum 8GB RAM, 4 CPU cores
- **Python**: Version 3.8+ with pip
- **Database**: MongoDB 4.4+
- **Storage**: Minimum 50GB for application and data
- **Network**: Reliable internet connection with outbound access
- **API Keys**: Various third-party services (details below)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-organization/ai-agent.git
   cd ai-agent
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Database**
   ```bash
   # Install MongoDB if not already installed
   # On Ubuntu:
   # sudo apt-get install -y mongodb
   
   # Start MongoDB service
   sudo systemctl start mongodb
   
   # Initialize database
   python scripts/init_database.py
   ```

4. **Configure API Keys**
   - Create a `.env` file in the root directory
   - Add the following API keys (obtain from respective services):
   ```
   GOOGLE_PLACES_API_KEY=your_key_here
   SENDGRID_API_KEY=your_key_here
   LINKEDIN_API_KEY=your_key_here
   LINKEDIN_API_SECRET=your_key_here
   GRAMMARLY_API_KEY=your_key_here
   DOCUSIGN_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```

5. **Configure Service Settings**
   - Edit `config/service_definitions.json` to match your service offerings
   - Edit `config/pricing_rules.json` to set your pricing strategy
   - Edit `config/templates/` directory to customize communication templates

6. **Start the System**
   ```bash
   # Start all modules
   python main.py
   
   # Alternatively, start individual modules
   python -m client_discovery.main
   python -m deal_closing.main
   python -m service_delivery.main
   ```

## Configuration Guide

### Client Discovery Configuration

#### Lead Sources
Edit `config/sources.json` to define where the system should look for potential clients:

```json
{
  "directories": [
    {
      "name": "google_my_business",
      "type": "google_my_business",
      "locations": ["New York, NY", "San Francisco, CA"],
      "categories": ["marketing", "web_design", "accounting"]
    },
    {
      "name": "chamber_of_commerce",
      "type": "industry_directory",
      "url": "https://www.chamberofcommerce.com/directories",
      "industry": "professional_services"
    }
  ],
  "social_platforms": [
    {
      "name": "linkedin",
      "search_terms": ["new business", "startup", "small business"],
      "filters": {
        "company_size": "1-50",
        "founded_within_years": 2
      }
    }
  ]
}
```

#### Lead Scoring
Edit `config/scoring_weights.json` to adjust how leads are scored and prioritized:

```json
{
  "business_maturity": 0.25,
  "digital_presence": 0.25,
  "growth_indicators": 0.25,
  "service_needs": 0.25,
  "digital_presence_factors": {
    "website_quality": 0.4,
    "social_media": 0.3,
    "online_reviews": 0.3
  }
}
```

### Deal Closing Configuration

#### Communication Templates
Edit templates in `config/templates/` directory. Templates use a simple variable substitution format:

```
Subject: Improving {business_name}'s online presence

Hi {decision_maker_name},

I noticed {business_name} has been growing in the {industry} space, and wanted to reach out about potentially helping with your {identified_need}.

Our clients typically see {benefit} within {timeframe}.

Would you be open to a brief conversation about how we might help?

Best regards,
{agent_name}
```

#### Negotiation Rules
Edit `config/negotiation_rules.json` to define acceptable negotiation parameters:

```json
{
  "price_flexibility": {
    "max_discount_percentage": 15,
    "volume_discount_threshold": 3,
    "rush_fee_percentage": 20
  },
  "scope_flexibility": {
    "additional_revisions": 2,
    "feature_substitution": true
  },
  "timeline_flexibility": {
    "max_extension_days": 7,
    "rush_minimum_days": 3
  }
}
```

### Service Delivery Configuration

#### Service Definitions
Edit `config/service_definitions.json` to define your service offerings:

```json
{
  "services": [
    {
      "service_id": "blog_post_writing",
      "name": "Blog Post Writing",
      "description": "SEO-optimized blog posts tailored to your industry",
      "category": "content_creation",
      "execution_module": "content_generator",
      "inputs": [
        {"name": "topic", "type": "string", "required": true},
        {"name": "keywords", "type": "array", "required": true},
        {"name": "word_count", "type": "number", "default": 1000}
      ],
      "outputs": [
        {"name": "markdown_content", "type": "file"},
        {"name": "seo_report", "type": "file"}
      ],
      "qa_checks": ["grammar", "plagiarism", "keyword_density", "readability"],
      "base_price": 150,
      "price_factors": {
        "word_count": {"unit": 500, "price": 50},
        "research_depth": {"low": 0, "medium": 50, "high": 100}
      }
    }
  ]
}
```

## Usage Guide

### Monitoring the System

The AI agent provides a web-based dashboard for monitoring all activities:

1. Access the dashboard at `http://your-server-ip:8080`
2. Login with the admin credentials (default: admin/changeme)
3. View real-time metrics and status of all modules

### Dashboard Sections

#### Client Discovery Dashboard
- **Lead Pipeline**: View newly discovered leads and their qualification status
- **Source Performance**: Track which lead sources are most effective
- **Lead Scoring**: Monitor scoring distribution and conversion rates

#### Deal Closing Dashboard
- **Deal Pipeline**: Track deals at each stage of the sales process
- **Communication Log**: View all outgoing and incoming communications
- **Proposal Tracker**: Monitor proposal status and acceptance rates

#### Service Delivery Dashboard
- **Project Status**: Track all active projects and their completion status
- **Task Board**: View individual tasks across all projects
- **Quality Metrics**: Monitor quality scores and revision rates

### Manual Interventions

While the system is designed to operate autonomously, certain scenarios may require manual intervention:

1. **Approval Workflows**: Configure approval requirements in `config/approval_settings.json`
2. **Escalation Triggers**: Define when issues should be escalated in `config/escalation_rules.json`
3. **Manual Review**: Access the review interface at `http://your-server-ip:8080/review`

## Customization Guide

### Adding New Service Types

1. Create a new service executor in `service_delivery/src/execution/`
2. Implement the `ExecutorInterface` class
3. Add the service definition to `config/service_definitions.json`
4. Create appropriate QA checks in `service_delivery/src/quality_assurance/`

### Extending Lead Sources

1. Create a new scanner in `client_discovery/src/discovery/`
2. Implement the source-specific logic
3. Add the source configuration to `config/sources.json`

### Customizing Communication Style

1. Edit templates in `config/templates/`
2. Adjust tone settings in `config/communication_style.json`
3. Test communications using the sandbox environment

## Troubleshooting

### Common Issues

1. **API Rate Limiting**
   - Symptom: Reduced lead discovery or failed API calls
   - Solution: Adjust the scanning frequency in `config/rate_limits.json`

2. **Low Quality Scores**
   - Symptom: Services frequently failing QA checks
   - Solution: Review and adjust QA thresholds in `config/qa_thresholds.json`

3. **Low Response Rates**
   - Symptom: Few prospects responding to outreach
   - Solution: Review and adjust communication templates, test different approaches

### Logging and Diagnostics

- Logs are stored in the `logs/` directory
- Each module has its own log file
- Set log level in `config/logging.json` (default: INFO)

### Support Resources

- Documentation: `docs/` directory
- Issue Tracker: GitHub Issues
- Community Forum: [link to forum]

## Security Considerations

1. **API Key Protection**
   - Store API keys in environment variables or a secure vault
   - Rotate keys regularly

2. **Data Protection**
   - Client data is stored in MongoDB with encryption at rest
   - Communication logs are retained according to the retention policy

3. **Access Control**
   - Use role-based access for the dashboard
   - Enable two-factor authentication for admin access

## Maintenance and Updates

1. **Regular Updates**
   ```bash
   git pull
   pip install -r requirements.txt
   python scripts/update_database.py
   ```

2. **Backup Procedure**
   ```bash
   # Backup database
   mongodump --db ai_agent --out backup/$(date +%Y%m%d)
   
   # Backup configuration
   cp -r config/ backup/$(date +%Y%m%d)/config
   ```

3. **Health Checks**
   - The system performs self-diagnostics every 24 hours
   - View health reports at `http://your-server-ip:8080/health`

## Conclusion

This AI agent system provides a comprehensive solution for automating client acquisition, deal closing, and service delivery. By following this guide, you can deploy, configure, and maintain the system to suit your specific business needs. The modular architecture allows for ongoing customization and extension as your requirements evolve.

For additional support or custom development, please contact the development team.
