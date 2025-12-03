# 🎨 OpenRouter Image Generator

An image generator built on the OpenRouter multimodal API, supporting multiple advanced AI image generation models. (***Generated with assistance from Claude-sonnet-4.5***)

## ✨ Features
- 🤖 Support for multiple mainstream image generation models (Gemini, FLUX, GPT-5 Image, etc.)
- 🎯 Custom aspect ratio settings (Gemini models exclusive)
- 🖼️ Real-time preview of generated results
- 📊 Complete API response debugging information
- 🔒 Secure API Key management

## 🚀 Supported Models
[View Supported Models](https://openrouter.ai/models?fmt=cards&output_modalities=image)

| Model Name | Model ID | Input Price | Output Price | Context Length |
|------------|----------|-------------|--------------|----------------|
| **FLUX.2 Flex** | `black-forest-labs/flux.2-flex` | $14.64/1M | $14.64/1M | 67,344 |
| **FLUX.2 Pro** | `black-forest-labs/flux.2-pro` | $3.66/1M | $3.66/1M | 46,864 |
| **Gemini 3 Pro Image** | `google/gemini-3-pro-image-preview` | $2/1M | $12/1M | 65,536 |
| **GPT-5 Image Mini** | `openai/gpt-5-image-mini` | $2.50/1M | $2/1M | 400,000 |
| **GPT-5 Image** | `openai/gpt-5-image` | $10/1M | $10/1M | 400,000 |
| **Gemini 2.5 Flash Image** | `google/gemini-2.5-flash-image` | $0.30/1M | $2.50/1M | 32,768 |
| **Gemini 2.5 Flash Image Preview** | `google/gemini-2.5-flash-image-preview` | - | - | - |

## 📦 Quick Start

### Method 1: Local Run
#### 1. Clone Repository
```bash
git clone <your-repo-url>
cd openrouter-image-generator
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run Application
```bash
python app.py
```

#### 4. Access Interface
Open browser and visit: `http://localhost:7860`

### Method 2: Docker Run
#### 1. Build Image
```bash
docker build -t openrouter-image-gen .
```

#### 2. Run Container
```bash
docker run -p 7860:7860 openrouter-image-gen
```

#### 3. Access Interface
Open browser and visit: `http://localhost:7860`

### Method 3: Docker Compose (Recommended)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "7860:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## 🔑 Get API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Register/Login to your account
3. Go to [API Keys](https://openrouter.ai/keys) page
4. Create a new API Key
5. Copy the Key (format: `sk-or-...`)

## 📖 Usage Guide

### Basic Usage Flow
1. **Enter API Key**  
   Paste your API key in the "OpenRouter API Key" field

2. **Select Model**  
   Choose an image generation model from the dropdown menu

3. **Set Aspect Ratio** (Optional)  
   Only effective for Gemini series models, supports:
   - 1:1 (Square)
   - 16:9 (Widescreen)
   - 9:16 (Portrait)
   - Other ratios...

4. **Enter Prompt**  
   Describe the image you want to generate in natural language, for example:
   - "A beautiful sunset over mountains with vivid colors"
   - "A futuristic city with flying cars at night"

5. **Click Generate**  
   Wait a few seconds to see the generated result

### Prompt Writing Tips
- ✅ **Be Specific**: Include subject, scene, style, colors, and other details
- ✅ **Use Adjectives**: vivid colors, photorealistic, minimalist, etc.
- ✅ **Specify Style**: oil painting, digital art, 3D render, etc.
- ❌ **Avoid Vagueness**: "a picture" → "a photorealistic portrait"

### Example Prompts
```
A cute robot playing with a cat in a cozy room, warm lighting, Studio Ghibli style
```
```
Futuristic cyberpunk city at night, neon lights, rain-soaked streets, cinematic composition
```
```
Minimalist geometric abstract art, pastel colors, modern design, 4K quality
```

## 🛠️ Tech Stack
- **Frontend Framework**: Gradio
- **HTTP Client**: Requests
- **API Provider**: OpenRouter

## 🐛 Troubleshooting

### Issue: Image Not Displaying
**Solution**:
- Check if API Key is correct
- Confirm selected model supports image generation
- Check error messages in "Complete JSON Response"

### Issue: Request Timeout
**Solution**:
- Check network connection
- Try switching models (some models respond faster)
- Simplify prompt content

### Issue: Insufficient API Balance
**Solution**:
- Go to [OpenRouter Credits](https://openrouter.ai/credits) to top up
- Choose lower-priced models (e.g., Gemini 2.5 Flash)

## 📝 Environment Variables
Optional environment variable configuration:
```bash
# Gradio server settings
GRADIO_SERVER_NAME=0.0.0.0    # Listen address
GRADIO_SERVER_PORT=7860        # Listen port
# Optional: Preset API Key (not recommended for production)
OPENROUTER_API_KEY=sk-or-...
```

## 🔒 Security Recommendations
- ⚠️ **Do NOT** hardcode API Keys in code
- ⚠️ **Do NOT** commit API Keys to version control
- ✅ Use environment variables or secret management services
- ✅ Regularly rotate API Keys
- ✅ Use HTTPS in production environments

## 📄 License
MIT License

## 🤝 Contributing
Welcome to submit Issues and Pull Requests!

## 📧 Contact
For questions, please contact via:
- GitHub Issues: [Project Issues Page]
- Email: your-email@example.com

## 🙏 Acknowledgments
- [OpenRouter](https://openrouter.ai/) - API Provider
- [Gradio](https://gradio.app/) - UI Framework
- [Black Forest Labs](https://blackforestlabs.ai/) - FLUX Models
- [Google DeepMind](https://deepmind.google/) - Gemini Models
- [OpenAI](https://openai.com/) - GPT Models

---
**⭐ If this project helps you, please give it a Star!**