# 使用Python官方镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . .

# 安装依赖项
RUN pip install --no-cache-dir flask requests beautifulsoup4

# 暴露端口
EXPOSE 15555

# 启动应用
CMD ["python", "app.py"]
