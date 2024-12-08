from metagadget import MetaGadget
import switchbot
import os


def main():
    app = MetaGadget()

    @app.receive
    def hundle(data):
        sceneId = os.environ.get("SWITCHBOT_SCENE_ID")
        switchbot.request("POST", f"/v1.1/scenes/{sceneId}/execute")

    app.run()


if __name__ == "__main__":
    main()