# 使用官方 Python 运行时作为基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（Pillow 需要的图像库）
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app.py .

# 暴露 Gradio 默认端口
EXPOSE 7860

# 设置环境变量
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# 启动应用
CMD ["python", "app.py"]