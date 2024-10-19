from metagadget import MetaGadget

def main():
    app = MetaGadget()

    @app.receive
    def hundle(data):
        print(f"Received data: {data}")

    app.run()

if __name__ == "__main__":
    main()