VISION_PROMPT = """
You MUST return valid JSON.
Do NOT include markdown.
Do NOT include explanations.
Do NOT include code fences.

Return a JSON ARRAY.
Each element must match this schema:

{
  "company_name": string,
  "role": string,
  "recruiter_name": string | null,
  "action_type": string,
  "channel": string,
  "confidence": number | null,
  "notes": string | null
}

If multiple job-related actions occurred, return multiple objects.
If none occurred, return an empty array [].

"""
