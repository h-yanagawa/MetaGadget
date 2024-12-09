import json
import os
import traceback
from typing import Optional, Any

from pydantic import BaseModel, Field

from switchbot_client.switchbot_client import SwitchBotClient
from metagadget import MetaGadget

class SmartHomeRequest(BaseModel):
    function_name: str = Field(..., title="func_name", alias="functionName")
    args: Optional[list[Any]] = Field(..., title="args")
    kwargs: Optional[dict[str, Any]] = Field(..., title="kwargs")


def main():
    app = MetaGadget()
    switchbot_client = SwitchBotClient(os.environ.get("SWITCHBOT_TOKEN"), os.environ.get("SWITCHBOT_SECRET"))

    @app.receive
    def handle(data):
        sh_req = SmartHomeRequest.model_validate_json(data)
        # Remote Procedure Call
        try:
            func = getattr(switchbot_client, sh_req.function_name)
            ret = func(*sh_req.args, **sh_req.kwargs)
            if isinstance(ret, BaseModel):
                ret = ret.model_dump_json()
            return ret
        except Exception:
            traceback.print_exc()
            mes = traceback.format_exc()[:500]
            return json.dumps({"error": mes})

    app.run()


if __name__ == "__main__":
    main()