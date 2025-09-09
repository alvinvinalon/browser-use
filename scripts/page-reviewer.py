from browser_use import Agent, ChatAzureOpenAI
from pydantic import SecretStr
import os
import asyncio
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Page reviewer script")
    parser.add_argument("--url", required=True, help="URL of the web page to review")
    return parser.parse_args()

# Get command line arguments
args = parse_args()

# Initialize the model
llm = ChatAzureOpenAI(
    model="gpt-4.1",
)

# Define the agent task
agent_task = f"""
 You are an expert AI assistant specializing in consumer protection and web content auditing. Your task is to analyze the provided text from a web page and evaluate it for potential violations of consumer rights, misleading information, and confusing language.

Your analysis will be based on a set of general consumer protection principles. Your goal is to identify and report any content that could cause a consumer to be misled or make a decision based on incomplete or confusing information.

**Web Page URL:**
{args.url}

**Principles for Analysis:**

1.  **Truthful and Non-Deceptive Information (Rule: 200)**: All claims, statements, and representations about products, services, prices, or benefits must be accurate and truthful. Avoid making false or misleading claims, including exaggerations or guarantees that cannot be substantiated.
    * **Violation Examples:** "Guaranteed to work every time," "Lose 10kg in one week," or displaying a product review that is not genuine.
2.  **Clear and Transparent Pricing (Rule: 201)**: The total price of the product or service must be clearly stated, including any additional fees, charges, taxes, or surcharges. Any offers, discounts, or special deals must have their conditions (e.g., expiry date, eligibility) clearly outlined.
    * **Violation Examples:** Stating a price "from $10" without specifying what that includes, or a "free trial" that automatically converts to a paid subscription without a clear warning.
3.  **No Misleading Urgency or Scarcity Tactics (Rule: 202)**: The page should not use false claims of limited stock, limited-time offers, or other pressure tactics to rush a consumer into a purchase.
    * **Violation Examples:** "Only 2 left in stock!" when there is a large inventory, or a countdown timer that resets every time the page is reloaded.
4.  **Clear and Understandable Language (Rule: 203)**: The language used must be plain, simple, and easy for the average person to understand. Avoid excessive jargon, complex legal terms, or vague language that could confuse a consumer about what they are buying or agreeing to.
    * **Violation Examples:** Using technical industry terms without explanation, or a complex, dense paragraph of text that hides key terms in a lengthy legal disclaimer.
5.  **Easy-to-Find Information (Rule: 204)**: Essential information, such as return policies, contact details, and terms and conditions, should be easy to find and not hidden away in a hard-to-access area of the website.
    * **Violation Examples:** The "Returns Policy" link is buried at the very bottom of the page in tiny, grey text, or the contact information is not provided at all.

**Instructions for Output:**

Analyze the web page content and produce a structured JSON object with the following keys:

* `page_summary`: A brief summary of the page's purpose and key information.
* `overall_compliance_score`: A score from 0 to 100 representing overall compliance, where 100 is full compliance. This should be an aggregate score based on the violations found.
* `compliance_violations`: An array of objects, where each object details a rule violation. If no violations are found, this array should be empty. Each object in the array should contain the following keys:
    * `rule_id`: The ID of the rule that was violated (e.g., `200`).
    * `rule_name`: The name of the rule (e.g., `Truthful and Non-Deceptive Information`).
    * `violation_description`: A detailed explanation of why the content violates the rule.
    * `violating_text_snippets`: An array of specific text snippets from the page that violate the rule.

**Example of Expected Output (if violations exist):**
```json
{{
  "page_summary": "This page is an e-commerce product page for a fitness supplement.",
  "overall_compliance_score": 50,
  "compliance_violations": [
    {{
      "rule_id": 200,
      "rule_name": "Truthful and Non-Deceptive Information",
      "violation_description": "The page makes unsubstantiated claims of dramatic weight loss with phrases that promise guaranteed results.",
      "violating_text_snippets": [
        "Guaranteed to lose 5kg in 7 days!",
        "Our clients have all achieved their dream bodies, effortlessly."
      ]
    }},
    {{
      "rule_id": 201,
      "rule_name": "Clear and Transparent Pricing",
      "violation_description": "The total cost of the product is not clear. The stated price does not include shipping or taxes, which are only revealed at the final checkout step.",
      "violating_text_snippets": [
        "Only $19.99 today!",
        "Shipping will be calculated at checkout."
      ]
    }},
    {{
      "rule_id": 202,
      "rule_name": "No Misleading Urgency or Scarcity Tactics",
      "violation_description": "A fake countdown timer is used to create a false sense of urgency, which is a deceptive practice.",
      "violating_text_snippets": [
        "Sale ends in 02:45:00"
      ]
    }}
  ]
}}
```  

Save the output as a JSON file.

"""

# Create agent with the model
agent = Agent(
    task=agent_task, 
    llm=llm
)

async def main():
    # Run the agent to perform the task
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())