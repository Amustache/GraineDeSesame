from app import create_app


application = create_app()

if __name__ == "__main__":
    from app.config import Config

    application.run(debug=Config.DEBUG, host=Config.SERVER_HOST, port=Config.SERVER_PORT)
