from anthropic import Anthropic
from app.config import settings
import json
from typing import Dict, Any

client = Anthropic()


class DrugService:
    @staticmethod
    def analyze_drug(drug_name: str, dosage: str) -> Dict[str, Any]:
        """Analyze a drug using Claude API"""

        prompt = f"""
Analyze the following drug prescription:
- Drug Name: {drug_name}
- Dosage: {dosage}

Provide comprehensive analysis in JSON format with:
1. what_is_it: Simple description of what this drug is
2. treats: List of conditions this drug treats
3. why_you_need_it: Why someone might need this drug
4. side_effects: Common side effects
5. interactions: Known drug interactions to watch for
6. insurance_coverage: Typical insurance coverage info
7. generic_available: Whether generic version exists
8. red_flags: Any concerns or warnings
9. questions_for_doctor: Questions patient should ask

Format as valid JSON.
        """

        try:
            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Try to extract JSON
            try:
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                # If not pure JSON, extract between curly braces
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    analysis = json.loads(response_text[start:end])
                else:
                    analysis = {"raw_response": response_text}

            return analysis
        except Exception as e:
            return {"error": str(e), "drug_name": drug_name, "dosage": dosage}
