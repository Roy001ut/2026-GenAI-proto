"""Claude API wrappers for drug, bill, and insurance analysis."""
import json
from typing import Any, Dict
from anthropic import Anthropic
from app.config import settings

_client = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=settings.CLAUDE_API_KEY)
    return _client


def _call(prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
    try:
        msg = _get_client().messages.create(
            model="claude-opus-4-6",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            s, e = text.find("{"), text.rfind("}") + 1
            if s >= 0 and e > s:
                return json.loads(text[s:e])
        return {"raw_response": text}
    except Exception as exc:
        return {"error": str(exc)}


def analyze_drug(drug_name: str, dosage: str) -> Dict[str, Any]:
    prompt = f"""Analyze this drug prescription and return ONLY valid JSON:
Drug: {drug_name}, Dosage: {dosage}

{{
  "what_is_it": "...",
  "treats": [...],
  "side_effects": [...],
  "insurance_coverage": {{...}},
  "red_flags": [...]
}}"""
    return _call(prompt)


def analyze_bill(bill_text: str, diagnosis: str = "") -> Dict[str, Any]:
    prompt = f"""Analyze this hospital bill for fraud. Return ONLY valid JSON:
Bill: {bill_text[:3000]}
Diagnosis: {diagnosis}

{{
  "charges": [...],
  "red_flags": [...],
  "fraud_risk_score": 0,
  "recommendations": [...]
}}"""
    return _call(prompt, max_tokens=3000)


def analyze_insurance(policy_text: str) -> Dict[str, Any]:
    prompt = f"""Parse this insurance policy. Return ONLY valid JSON:
Policy: {policy_text[:5000]}

{{
  "provider_name": "...",
  "premium": "...",
  "deductible": {{...}},
  "copays": {{...}},
  "covered_services": [...],
  "excluded_services": [...]
}}"""
    return _call(prompt, max_tokens=2500)
