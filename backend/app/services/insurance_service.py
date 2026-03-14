from anthropic import Anthropic
from app.config import settings
import json
from typing import Dict, Any

client = Anthropic(api_key=settings.CLAUDE_API_KEY)


class InsuranceService:
    @staticmethod
    def parse_insurance_policy(policy_text: str) -> Dict[str, Any]:
        """Parse insurance policy document"""

        prompt = f"""
Parse this insurance policy and extract key information:

Policy Text: {policy_text[:5000]}

Extract and format as JSON:
1. provider_name: Insurance company name
2. premium: Monthly/annual premium
3. deductible: {{health, dental, vision}}
4. copays: {{office_visit, specialist, er, prescription}}
5. coinsurance: Percentage patient pays
6. out_of_pocket_max: Annual maximum
7. covered_services: List of covered services
8. excluded_services: List of excluded services
9. pre_auth_requirements: Services requiring pre-authorization

Format as valid JSON.
        """

        try:
            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            try:
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    analysis = json.loads(response_text[start:end])
                else:
                    analysis = {"raw_response": response_text}

            return analysis
        except Exception as e:
            return {"error": str(e)}
