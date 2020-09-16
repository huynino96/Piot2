from app import app


if __name__ == '__main__':
    print('Server is running on port 5000')
    app.run("127.0.0.1", 5000, debug=True)