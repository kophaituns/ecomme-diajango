import os
import json
import random
import re
from django.conf import settings

# Helper function to extract keywords from text
def extract_keywords(text):
    """Extract potential keywords from text for product matching"""
    # Remove common words
    common_words = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                   'has', 'have', 'had', 'this', 'that', 'these', 'those', 'for', 'with',
                   'by', 'to', 'from', 'in', 'on', 'at', 'of'}
    
    # Split text into words, lowercase, and remove punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out common words and short words
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    return keywords

# We're using a local AI simulation instead of OpenAI API due to quota limitations
# This will provide responses without making actual API calls

# Function to simulate AI responses locally
def call_openai_api(messages, model="gpt-3.5-turbo", max_tokens=150):
    """Simulated AI response function that doesn't require API calls"""
    try:
        # Get the last user message
        user_message = ""
        for msg in messages:
            if msg["role"] == "user":
                user_message = msg["content"]
        
        # Check message content and generate appropriate responses
        response = generate_simulated_response(user_message)
        return response
    except Exception as e:
        print(f"Error in local AI simulation: {str(e)}")
        return "I'm sorry, I couldn't process your request at the moment. How else can I help you?"

def generate_simulated_response(message):
    """Generate appropriate responses based on the input message"""
    message = message.lower()
    
    # Product-related queries
    if any(word in message for word in ["product", "item", "buy", "purchase"]):
        return "We have a great selection of products including electronics, accessories, and more. You can browse our catalog and add items to your cart easily. Would you like recommendations for any specific category?"
    
    # Order-related queries
    elif any(word in message for word in ["order", "delivery", "shipping", "track"]):
        return "You can track your orders through the 'My Orders' section in your profile. Most deliveries take 3-5 business days. For any specific order inquiries, please provide your order number."
    
    # Price-related queries
    elif any(word in message for word in ["price", "cost", "discount", "offer"]):
        return "Our prices are competitive and we frequently run special offers. You can see all current discounts on our homepage. We also have seasonal sales and member-exclusive offers!"
    
    # Return policy
    elif any(word in message for word in ["return", "refund", "exchange"]):
        return "We offer a 30-day return policy for most items. Products must be in their original condition with all packaging. You can initiate returns from your order history section."
    
    # Account-related
    elif any(word in message for word in ["account", "login", "password", "profile"]):
        return "You can manage your account settings from your profile page. This includes updating your personal information, changing your password, and viewing your order history."
    
    # Payment-related
    elif any(word in message for word in ["payment", "card", "credit", "debit", "pay"]):
        return "We accept major credit cards, debit cards, and digital payment methods. All payment information is securely processed and encrypted. Would you like more information about a specific payment method?"
    
    # Recommendation requests
    elif "recommend" in message:
        return "Based on popular trends, I'd recommend checking out our wireless earbuds, smartphones, and laptop accessories. You can also visit our 'AI Recommendations' page for personalized suggestions based on your browsing history."
    
    # Greeting
    elif any(word in message for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! Welcome to our e-commerce store. How can I assist you today? I can help with product information, order tracking, or general inquiries."
    
    # Thank you
    elif any(word in message for word in ["thank", "thanks"]):
        return "You're welcome! Is there anything else I can help you with today?"
    
    # Default response
    else:
        return "Thank you for your message. I'm here to help with product information, order tracking, and general inquiries. How can I assist you further?"

def get_product_recommendations(user_preferences, available_products):
    """
    Get AI-powered product recommendations based on user preferences and browsing history.
    Using a local simulation instead of API calls due to quota limitations.
    
    Args:
        user_preferences: A description of user's preferences or previous purchases
        available_products: List of available products in the store
    
    Returns:
        List of recommended product IDs
    """
    try:
        # Instead of using OpenAI API, we'll use a simple algorithm to recommend products
        # This is a placeholder for the actual AI recommendation system
        
        # Get a list of all product IDs
        all_product_ids = [p.id for p in available_products]
        
        if not all_product_ids:
            return []  # Return empty list if no products available
        
        # If user has preferences, try to match products
        if user_preferences and "purchase" in user_preferences.lower():
            # Extract potential keywords from preferences
            keywords = extract_keywords(user_preferences.lower())
            
            # Score products based on keyword matches
            scored_products = []
            for product in available_products:
                score = 0
                product_text = (product.name + " " + product.description).lower()
                for keyword in keywords:
                    if keyword in product_text:
                        score += 1
                if score > 0:
                    scored_products.append((product.id, score))
            
            # Return top scoring products, if any matches found
            if scored_products:
                scored_products.sort(key=lambda x: x[1], reverse=True)
                return [p_id for p_id, _ in scored_products[:5]]
        
        # If no preferences or no matches, return top 5 products
        # For demonstration, we'll just return 5 random products
        if len(all_product_ids) <= 5:
            return all_product_ids
        else:
            return random.sample(all_product_ids, 5)
            
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        # Return some default recommendations if API call fails
        return [p.id for p in available_products[:5]]

def get_chatbot_response(user_query, customer_info=None):
    """
    Get AI-powered chatbot response for customer queries.
    
    Args:
        user_query: The query from the user
        customer_info: Optional customer information for personalized responses
    
    Returns:
        String response from the chatbot
    """
    try:
        # Direct call to our simulated AI function with the user's query
        messages = [
            {"role": "system", "content": "You are a helpful customer support agent for an e-commerce website."},
            {"role": "user", "content": user_query}
        ]
        
        # Add customer context if available
        if customer_info:
            customer_name = customer_info.get_name if hasattr(customer_info, 'get_name') else "Valued Customer"
            # Personalize the response with customer name
            messages[0]["content"] += f" You're speaking with {customer_name}."
        
        # Get response from our local AI function
        response = call_openai_api(messages)
        return response
        
    except Exception as e:
        print(f"Error in chatbot: {str(e)}")
        # Return a fallback response if there's an error
        return "I'm sorry, but I'm having trouble processing your request right now. Please try again later or contact our customer support team for assistance."

def analyze_product_feedback(feedback_text):
    """
    Analyze product feedback using AI to extract sentiment and key points.
    
    Args:
        feedback_text: The feedback text to analyze
        
    Returns:
        Dictionary containing sentiment and key points
    """
    try:
        # Simple sentiment analysis based on keywords
        feedback_lower = feedback_text.lower()
        
        # Count positive and negative words
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'like', 
                         'best', 'fantastic', 'wonderful', 'happy', 'satisfied', 
                         'perfect', 'awesome', 'pleased', 'quality']
        
        negative_words = ['bad', 'poor', 'terrible', 'awful', 'hate', 'dislike', 
                         'worst', 'disappointing', 'unhappy', 'dissatisfied', 
                         'defective', 'broken', 'issue', 'problem', 'complaint']
        
        positive_count = sum(1 for word in positive_words if word in feedback_lower)
        negative_count = sum(1 for word in negative_words if word in feedback_lower)
        
        # Determine sentiment
        sentiment = "neutral"
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        
        # Extract key points (simplified version)
        key_points = []
        if 'quality' in feedback_lower:
            key_points.append("Comment on product quality")
        if 'price' in feedback_lower or 'expensive' in feedback_lower or 'cheap' in feedback_lower:
            key_points.append("Comment on pricing")
        if 'shipping' in feedback_lower or 'delivery' in feedback_lower:
            key_points.append("Comment on shipping/delivery")
        if 'service' in feedback_lower or 'support' in feedback_lower:
            key_points.append("Comment on customer service")
        
        # Add a generic point if none found
        if not key_points:
            key_points.append("General product feedback")
        
        # Generate suggested response based on sentiment
        if sentiment == "positive":
            suggested_response = "Thank you for your positive feedback! We're delighted to hear you had a good experience with us."
        elif sentiment == "negative":
            suggested_response = "We apologize for your experience. Your feedback is important to us, and we'll work to address the issues you've raised."
        else:
            suggested_response = "Thank you for your feedback. We appreciate you taking the time to share your thoughts with us."
            
        # Create JSON response
        analysis = {
            "sentiment": sentiment,
            "key_points": key_points,
            "suggested_response": suggested_response
        }
        
        return json.dumps(analysis)
        
        # Fallback to simple analysis if API call fails or returns invalid JSON
        feedback_text = feedback_text.lower()
        
        # Simple sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'like', 'best', 'perfect', 'awesome', 'satisfied']
        negative_words = ['bad', 'poor', 'terrible', 'awful', 'hate', 'dislike', 'worst', 'horrible', 'disappointed', 'issue', 'problem']
        
        positive_count = sum(word in feedback_text for word in positive_words)
        negative_count = sum(word in feedback_text for word in negative_words)
        
        sentiment = "neutral"
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        
        # Extract key points (simplified version)
        key_points = []
        if 'quality' in feedback_lower:
            key_points.append("Comment on product quality")
        if 'price' in feedback_lower or 'expensive' in feedback_lower or 'cheap' in feedback_lower:
            key_points.append("Comment on pricing")
        if 'shipping' in feedback_lower or 'delivery' in feedback_lower:
            key_points.append("Comment on shipping/delivery")
        if 'service' in feedback_lower or 'support' in feedback_lower:
            key_points.append("Comment on customer service")
        
        # Add a generic point if none found
        if not key_points:
            key_points.append("General product feedback")
        
        # Generate suggested response
        if sentiment == "positive":
            suggested_response = "Thank you for your positive feedback! We're glad to hear you had a good experience with our products/services."
        elif sentiment == "negative":
            suggested_response = "We apologize for your experience. Your feedback is important to us, and we'll work on improving the issues you've mentioned."
        else:
            suggested_response = "Thank you for your feedback. We appreciate you taking the time to share your thoughts with us."
        
        # Format as JSON string for the template
        analysis_dict = {
            "sentiment": sentiment,
            "key_points": key_points,
            "suggested_response": suggested_response
        }
        return json.dumps(analysis_dict)
        
    except Exception as e:
        print(f"Error analyzing feedback: {str(e)}")
        return '{"sentiment": "neutral", "key_points": ["Unable to analyze feedback"], "suggested_response": "Thank you for your feedback."}'
