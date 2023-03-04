from app import create_app

app = create_app()


# 主进程，启动后端服务
if __name__ == "__main__":
    app.run(debug=True, port=8888)
