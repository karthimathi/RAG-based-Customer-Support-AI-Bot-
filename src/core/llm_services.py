# CONCEPTUAL: Llama-3 API integration pattern
from typing import List, Dict, Any
import json

class LlamaService:
    """Handles communication with the Llama-3 API."""
    
    def __init__(self, api_key: str, api_url: str = "https://api.llama.ai/v1/chat/completions"):
        self.api_key = api_key
        self.api_url = api_url
    
    def generate_response(self, 
                         user_query: str, 
                         context: List[str],
                         conversation_history: List[Dict[str, str]] = None) -> str:
        """Generate a response using Llama-3 with retrieved context."""
        
        # Prepare the context
        context_text = "\n\n".join([f"[Source {i+1}]: {text}" for i, text in enumerate(context)])
        
        # System prompt
        system_prompt = """You are a helpful customer support assistant. 
        Use the provided context to answer the user's question accurately.
        If the context doesn't contain relevant information, say so politely.
        Always be professional and helpful."""
        
        # User prompt with context
        user_prompt = f"""Context from company documents:
        {context_text}
        
        User Question: {user_query}
        
        Please provide a helpful answer based on the context above."""
        
        try:
            # CONCEPTUAL: Actual API call to Llama-3
            # This shows the complete production pattern
            
            # headers = {
            #     "Authorization": f"Bearer {self.api_key}",
            #     "Content-Type": "application/json"
            # }
            
            # payload = {
            #     "model": "llama-3-70b",
            #     "messages": [
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": user_prompt}
            #     ],
            #     "temperature": 0.7,
            #     "max_tokens": 500
            # }
            
            # response = requests.post(self.api_url, headers=headers, json=payload)
            # response_data = response.json()
            # return response_data["choices"][0]["message"]["content"]
            
            # For GitHub demonstration, generate mock responses
            return self._generate_mock_response(user_query, context)
            
        except Exception as e:
            print(f"Error calling Llama-3 API: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again later or contact our support team directly."
    
    def _generate_mock_response(self, user_query: str, context: List[str]) -> str:
        """Generate realistic mock responses for GitHub demo."""
        
        # Simple rule-based mock responses
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ["refund", "return", "money back"]):
            return """Based on our company policies, we offer a 30-day money-back guarantee on all products. Refunds are processed within 7-10 business days after we receive the returned item. To request a refund, please contact our support team with your order number and reason for return."""
        
        elif any(word in query_lower for word in ["shipping", "delivery", "track"]):
            return """Our standard shipping takes 3-5 business days within the continental US. International shipping typically takes 7-14 business days. You can track your order using the tracking link provided in your confirmation email."""
        
        elif any(word in query_lower for word in ["warranty", "guarantee", "support"]):
            return """All products come with a 1-year manufacturer's warranty. For warranty claims, please contact our support team with your purchase details and a description of the issue. Our technical support team is available Monday-Friday, 9am-5pm EST."""
        
        elif context and len(context) > 0:
            return f"""I found some relevant information in our documentation that might help: {context[0][:200]}... For more specific details, please refer to our full documentation or contact support."""
        
        else:
            return """Thank you for your question. I'm a customer support AI assistant. Based on the available information in our company documents, I don't have specific details about your query. For personalized assistance, please contact our human support team at support@company.com or call (555) 123-4567."""
