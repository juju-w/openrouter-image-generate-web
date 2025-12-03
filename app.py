import gradio as gr
import requests
import json
import base64
import io
from PIL import Image

# 预设的支持图片生成的模型列表 (根据文档)
# 预设的支持图片生成的模型列表（按价格排序）
DEFAULT_MODELS = [
    "google/gemini-2.5-flash-image",                    # 最便宜：$0.30/$2.50
    "google/gemini-3-pro-image-preview",                # $2/$12
    "openai/gpt-5-image-mini",                          # $2.50/$2
    "google/gemini-2.5-flash-image-preview",            # Preview 版本
    "black-forest-labs/flux.2-pro",                     # $3.66/$3.66
    "openai/gpt-5-image",                               # $10/$10
    "black-forest-labs/flux.2-flex",                    # 最贵：$14.64/$14.64
]

# 模型信息字典（用于显示价格提示）
MODEL_INFO = {
    "google/gemini-2.5-flash-image": "💰 $0.30/$2.50 per 1M tokens | Context: 32K",
    "google/gemini-3-pro-image-preview": "💰 $2/$12 per 1M tokens | Context: 65K",
    "openai/gpt-5-image-mini": "💰 $2.50/$2 per 1M tokens | Context: 400K",
    "google/gemini-2.5-flash-image-preview": "💰 Preview Model | Context: TBD",
    "black-forest-labs/flux.2-pro": "💰 $3.66/$3.66 per 1M tokens | Context: 46K",
    "openai/gpt-5-image": "💰 $10/$10 per 1M tokens | Context: 400K",
    "black-forest-labs/flux.2-flex": "💰 $14.64/$14.64 per 1M tokens | Context: 67K",
}
# Gemini 支持的宽高比列表
ASPECT_RATIOS = [
    "1:1", "2:3", "3:2", "3:4", "4:3",
    "4:5", "5:4", "9:16", "16:9", "21:9"
]

def update_model_info(model_name):
    """更新模型信息显示"""
    return MODEL_INFO.get(model_name, "ℹ️ 自定义模型")

def decode_base64_image(base64_string):
    """
    将 Base64 Data URL 转换为 PIL Image 对象
    """
    # 去掉 "data:image/xxx;base64," 前缀
    if base64_string.startswith('data:'):
        base64_string = base64_string.split(',', 1)[1]

    # 解码 Base64
    image_data = base64.b64decode(base64_string)

    # 转换为 PIL Image
    image = Image.open(io.BytesIO(image_data))
    return image


def generate_image(
        api_key,
        base_url,
        model_name,
        prompt,
        aspect_ratio
):
    """
    调用 OpenRouter API 生成图片
    """
    if not api_key:
        return None, "❌ 错误: 请输入 API Key", None

    if not prompt:
        return None, "❌ 错误: 请输入提示词 (Prompt)", None

    # 构造 Request Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/gradio-app/gradio",
        "X-Title": "Gradio Image Gen"
    }

    # 构造 Request Payload (依据文档)
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"]
    }

    # 如果选择了非默认宽高比，且模型通常支持配置 (主要是 Gemini)
    if aspect_ratio and aspect_ratio != "1:1":
        payload["image_config"] = {
            "aspect_ratio": aspect_ratio
        }

    try:
        # 发送请求
        response = requests.post(base_url, headers=headers, json=payload)

        # 检查 HTTP 状态码
        if response.status_code != 200:
            return None, f"❌ API 错误 ({response.status_code}): {response.text}", None

        result = response.json()

        # 解析返回结果
        if result.get("choices"):
            message = result["choices"][0]["message"]
            text_content = message.get("content", "")

            if message.get("images"):
                # 获取第一张图片的 Base64 Data URL
                image_url = message["images"][0]["image_url"]["url"]

                # 🔧 关键修复：将 Base64 转换为 PIL Image
                try:
                    pil_image = decode_base64_image(image_url)
                    status_msg = f"✅ 生成成功! {text_content}" if text_content else "✅ 生成成功!"
                    return pil_image, status_msg, result
                except Exception as e:
                    return None, f"❌ 图片解码失败: {str(e)}", result
            else:
                return None, f"⚠️ 请求成功但未返回图片数据。完整响应: {json.dumps(result, indent=2)}", result
        else:
            return None, f"⚠️ 返回格式无法解析: {json.dumps(result, indent=2)}", result

    except Exception as e:
        return None, f"❌ 系统错误: {str(e)}", None


# --- 构建 Gradio 界面 ---

with gr.Blocks(title="OpenRouter Image Generator") as demo:
    gr.Markdown("# 🎨 OpenRouter 图片生成器")
    gr.Markdown("基于 OpenRouter 多模态 API 文档构建，支持 Gemini 及 Flux 系列模型。")

    with gr.Row():
        with gr.Column(scale=1):
            # 配置区域
            with gr.Group():
                gr.Markdown("### ⚙️ API 设置")
                api_key_input = gr.Textbox(
                    label="OpenRouter API Key",
                    placeholder="sk-or-...",
                    type="password",
                    value=""
                )
                base_url_input = gr.Textbox(
                    label="API Endpoint",
                    value="https://openrouter.ai/api/v1/chat/completions"
                )

            with gr.Group():
                gr.Markdown("### 🎨 模型参数")
                model_input = gr.Dropdown(
                    label="选择模型 (Model)",
                    choices=DEFAULT_MODELS,
                    value="google/gemini-2.5-flash-image",
                    allow_custom_value=True
                )
                model_info_display = gr.Markdown(
                    value=MODEL_INFO["google/gemini-2.5-flash-image"]
                )
                aspect_ratio_input = gr.Dropdown(
                    label="宽高比 (仅 Gemini 模型有效)",
                    choices=ASPECT_RATIOS,
                    value="1:1"
                )

        with gr.Column(scale=2):
            # 输入和输出区域
            prompt_input = gr.Textbox(
                label="提示词 (Prompt)",
                placeholder="例如：A beautiful sunset over mountains with vivid colors",
                lines=4
            )
            generate_btn = gr.Button("🚀 开始生成", variant="primary", size="lg")

            status_output = gr.Textbox(label="状态信息", interactive=False)
            image_output = gr.Image(label="生成结果", type="pil")

            with gr.Accordion("完整 JSON 响应 (调试用)", open=False):
                json_output = gr.JSON()

    # 绑定事件
    model_input.change(
        fn=update_model_info,
        inputs=[model_input],
        outputs=[model_info_display]
    )

    generate_btn.click(
        fn=generate_image,
        inputs=[
            api_key_input,
            base_url_input,
            model_input,
            prompt_input,
            aspect_ratio_input
        ],
        outputs=[image_output, status_output, json_output]
    )

    # 添加示例
    gr.Examples(
        examples=[
            ["A beautiful sunset over mountains with vivid colors, photorealistic, 4K"],
            ["A futuristic cyberpunk city at night with neon lights and flying cars"],
            ["A cute robot playing with a cat in a cozy room, warm lighting, Studio Ghibli style"],
            ["Abstract geometric art with pastel colors, minimalist design"],
        ],
        inputs=prompt_input,
    )

    gr.Markdown("""
    ---
    ### 💡 使用提示
    - **Gemini 系列**：性价比高，支持宽高比设置
    - **FLUX 系列**：高质量艺术风格
    - **GPT-5 Image**：强大的理解能力，超大上下文
    - 详细的提示词可以获得更好的效果
    """)

if __name__ == "__main__":
    demo.launch()
