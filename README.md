# Odoo AI Support Chatbot

An intelligent, industry-specific AI assistant that provides personalized Odoo ERP support, guidance, and feature recommendations using the power of GPT-4.

## Features

- **Industry-Specific Guidance**: Tailored support for Retail, Manufacturing, Services, IT, Finance, Healthcare, and more
- **Interactive Chat Interface**: Clean, intuitive Streamlit UI for natural conversations
- **Powered by GPT-4o-mini**: High-quality responses while keeping API costs reasonable
- **Contextual Feature Guides**: Automatic detection of module-specific questions with tailored navigation instructions
- **Conversation Memory**: Maintains context throughout your session for more meaningful assistance
- **Professional UI**: Custom-styled chat bubbles for better conversation flow
- **Secure API Handling**: Supports both .env files and Streamlit secrets for API key management

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/odoo-ai-chatbot.git
   cd odoo-ai-chatbot
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root with:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Or use Streamlit secrets management when deploying

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Select your industry from the dropdown menu
3. Start chatting with the AI assistant about any Odoo-related questions

## Example Questions

- "How do I set up inventory tracking in Odoo?"
- "What's the best way to configure manufacturing operations?"
- "Can you explain how the CRM pipeline works?"
- "How do I create a custom invoice template?"
- "What Odoo modules would benefit a retail business the most?"

## Customization

### Modifying Industry Options

Edit the `industry_options` dictionary to add or modify available industries:

```python
industry_options = {
    "New Industry": "Description of industry focus",
    # Add more industries...
}
```

### Changing the AI Model

To use a different OpenAI model, modify the `MODEL` variable:

```python
MODEL = "gpt-4" # or any other OpenAI model
```

## Requirements

- Python 3.7+
- OpenAI API key
- Streamlit
- python-dotenv

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenAI](https://openai.com/) for their powerful GPT models
- [Streamlit](https://streamlit.io/) for the interactive web framework
- [Odoo](https://www.odoo.com/) for their comprehensive ERP system

---

Created for the Odoo community
