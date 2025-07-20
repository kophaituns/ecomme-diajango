# E-commerce AI Features

This document explains the AI features added to the e-commerce platform.

## Setup Instructions

1. Install the required packages:
```
pip install -r requirements.txt
```

2. Run migrations to create the ChatMessage model:
```
python manage.py migrate
```

3. Run the development server:
```
python manage.py runserver
```

## AI Features

### 1. AI Shopping Assistant (Chatbot)

The AI Shopping Assistant can help customers with:
- Product inquiries
- Order tracking information
- Shipping questions
- Return policy information
- General shopping advice

**How to access:**
- Click on the "AI Assistant" link in the navigation menu (when logged in as a customer)
- URL: `/ai-chatbot/`

### 2. AI Product Recommendations

The system provides personalized product recommendations based on:
- Purchase history
- Browsing patterns
- Similar customer preferences

**How to access:**
- Click on the "AI Recommendations" link in the navigation menu (when logged in as a customer)
- URL: `/ai-recommendations/`
- Also accessible from a banner on the customer home page

### 3. AI Feedback Analysis (Admin Feature)

Admins can analyze customer feedback using AI to:
- Determine sentiment (positive, negative, neutral)
- Extract key points
- Get suggested responses

**How to access:**
- Navigate to the Feedback section in the admin panel
- Click "Analyze with AI" on any feedback item
- URL: `/ai-analyze-feedback/<feedback_id>/`

## Technical Details

- Uses OpenAI's GPT model via API
- API key is configured in the ai_services.py file
- All AI responses are stored in the database for future reference and analysis

## Notes

- The AI features require an internet connection to connect to the OpenAI API
- API usage may incur costs depending on your OpenAI plan
- Be mindful of the API rate limits
