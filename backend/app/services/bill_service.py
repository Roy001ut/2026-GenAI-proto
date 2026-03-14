from anthropic import Anthropic
from app.config import settings
import json
from typing import Dict, Any, Optional

client = Anthropic(api_key=settings.CLAUDE_API_KEY)


class BillService:
    @staticmethod
    def analyze_bill(bill_text: str, patient_diagnosis: Optional[str] = None) -> Dict[str, Any]:
        """Analyze hospital bill for fraud and costs"""

        prompt = f"""
Analyze this hospital bill for potential fraud and cost issues:

Bill Text: {bill_text[:3000]}

Patient Diagnosis: {patient_diagnosis or "Not provided"}

Provide analysis in JSON with:
1. charges: List of all charges with {{code, description, amount, status}}
2. red_flags: List of concerning items
3. fraud_indicators: {{duplicates, diagnosis_mismatch, overpriced, unnecessary}}
4. fraud_risk_score: 0-100 risk level
5. total_charged: Total bill amount
6. estimated_average_cost: What this should typically cost
7. recommendations: Actions patient should take

Format as valid JSON.
        """

        try:
            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=3000,
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
