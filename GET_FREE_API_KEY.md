# How to Get a Free Google Gemini API Key

Google offers a generous free tier for the Gemini API, making it a great alternative to OpenAI for development and personal projects.

## 1. Go to Google AI Studio
Visit [Google AI Studio](https://aistudio.google.com/app/apikey). You will need to sign in with a Google account.

## 2. Create an API Key
1. Click the **"Create API key"** button.
2. If you don't have an existing project, selecting "Create API key in new project" is the easiest option.
3. Copy the generated API key.

## 3. Configure Your Project
1. Open your `.env` file (create one from `.env.example` if you haven't already).
2. Add your key and set the provider:

```ini
AI_PROVIDER=gemini
GEMINI_API_KEY=your_copied_api_key_here
```

## Free Tier Limits (as of early 2024)
- **Rate Limit**: 15 requests per minute (RPM)
- **Token Limit**: 1 million tokens per minute (TPM)
- **Daily Limit**: 1,500 requests per day

> [!NOTE]
> The free tier data may be used to improve Google's products. For production use with privacy guarantees, you can upgrade to a paid plan.
