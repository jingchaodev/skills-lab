# Decagon: Evidence-Checked Employer Research

## What it concretely builds

Decagon sells an enterprise platform for building and operating customer-service AI agents across chat, voice, email, and SMS. Its agents ingest company knowledge and conversation history, connect to business systems, and can execute actions such as refunds rather than merely retrieve answers. Customers also receive conversation analytics and operational controls. Decagon uses both first-party and third-party models. ([Decagon product](https://decagon.ai/); [TechCrunch, June 18, 2024](https://techcrunch.com/2024/06/18/decagon-claims-its-customers-service-bots-are-smarter-than-average/))

Its current product abstraction is “Agent Operating Procedures”: customers define workflows in natural language instead of a proprietary configuration language. The public site describes one platform for building, optimizing, evaluating, and deploying agents across channels, but does not expose enough implementation detail to determine how much orchestration, model serving, evaluation, or memory infrastructure is proprietary. ([Decagon product](https://decagon.ai/))

This is not merely a thin support-widget hiring surface. A current infrastructure role says the team owns networking, data systems, ML serving, developer platforms, and real-time voice, with explicit p95/p99 latency and SLO responsibilities. Current openings also include agent orchestration, core/cloud/data infrastructure, developer experience, research, and voice roles. ([Core Infrastructure role](https://jobs.ashbyhq.com/decagon/7a22482c-e2d4-45b6-b364-89b63189a4ae); [careers page](https://decagon.ai/careers))

## Verified founders

- **Jesse Zhang, co-founder and CEO:** previously a Google software engineer and founder of social-gaming company Lowkey, which Niantic acquired in 2021. ([TechCrunch](https://techcrunch.com/2024/06/18/decagon-claims-its-customers-service-bots-are-smarter-than-average/); [No Priors interview](https://www.youtube.com/watch?v=emaSFP7y7Ko))
- **Ashwin Sreenivas, co-founder:** previously a Palantir deployment strategist and co-founder of computer-vision startup Helia, acquired by Scale AI in 2020. The public sources reviewed identify him as co-founder but do not consistently establish his current formal title. ([TechCrunch](https://techcrunch.com/2024/06/18/decagon-claims-its-customers-service-bots-are-smarter-than-average/))

Both founders had previously built and sold startups, but I found no reliable public evidence establishing when they met, whether they worked together before Decagon, or their present division of engineering, research, product, and sales responsibilities. ([TechCrunch](https://techcrunch.com/2024/06/18/decagon-claims-its-customers-service-bots-are-smarter-than-average/))

## Claim audit

**Company claim — attributed, not independently validated:** Decagon’s homepage reports “70% chat and voice resolution” beside a named customer executive, while its job description calls Decagon the “leading” conversational-AI platform. These are company-controlled statements; no methodology, denominator, comparison set, or independent audit is supplied on those pages. ([Decagon product](https://decagon.ai/); [Core Infrastructure role](https://jobs.ashbyhq.com/decagon/7a22482c-e2d4-45b6-b364-89b63189a4ae))

**Independently supported business claim:** TechCrunch reported in June 2024 that Decagon had raised $35 million and named Eventbrite, Bilt, and Substack as clients. However, its statement that Decagon had reached break-even appears to derive from company information rather than audited financial disclosure. Thus the financing and customer relationships have independent reporting support; production depth, recurring revenue, and profitability remain unresolved. ([TechCrunch](https://techcrunch.com/2024/06/18/decagon-claims-its-customers-service-bots-are-smarter-than-average/))

## Culture signal

Decagon explicitly describes itself as **in-office**, organized around “excellence and velocity,” with values including “Just Get It Done,” “Winner’s Mindset,” customer invention, and polymathic breadth. The same role assigns engineers end-to-end ownership of production services. This supports a culture claim of high speed, broad ownership, and physical co-location—but it is employer-authored evidence, not proof of employees’ lived experience, sustainable workload, or how failures and dissent are handled. ([Core Infrastructure role](https://jobs.ashbyhq.com/decagon/7a22482c-e2d4-45b6-b364-89b63189a4ae))

## Two useful interviews

1. **“No Priors Ep. 132 | With Decagon CEO and Co-Founder Jesse Zhang”** — approximately 31 minutes; independently hosted by No Priors. Useful for product differentiation, customer workflow integration, pricing, hiring philosophy, and Zhang’s application-layer thesis. **Canonical URL:** [YouTube](https://www.youtube.com/watch?v=emaSFP7y7Ko). **Transcript provenance:** platform captions appear to be the available transcript path, but I could not retrieve and validate the full caption body because YouTube presented an automated-traffic gate; treat substantive quotations as not yet transcript-verified.

2. **“First Block: Interview with Jesse Zhang, Co-Founder and CEO of Decagon”** — approximately 23 minutes; hosted by Notion and useful for AOPs, enterprise trust, scaling, hiring, and operating tools. **Canonical URL:** [YouTube](https://www.youtube.com/watch?v=TnDemLcmOE8). **Transcript provenance:** publisher-linked transcript/resources are advertised in the video description via [Notion’s canonical companion link](https://ntn.so/2rl402); the transcript body was not independently retrieved, so provenance is **publisher-transcript, availability discovered but contents unverified**.

## Explicit unknowns

- Audited ARR, profitability, retention, customer concentration, pricing, and production volume.
- Resolution-rate methodology and performance versus human agents or competing platforms.
- Model-provider dependence and the exact boundary between proprietary and purchased models.
- Architecture for memory, evaluation, guardrails, tenant isolation, and human escalation.
- Actual weekly hours, office-day requirement, attrition, incident culture, and treatment of failed projects.
- Founder responsibility split and employee perspectives independent of recruiting material.
