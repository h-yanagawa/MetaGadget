const BOT_DEVICE_ID = "CDC10B...";

function setLight(isOn, r = 0.14, g = 0.74, b = 0.52, brightness = 1.0) {
  $.state.isOn = isOn;
  $.state.lastLightUpdated = Date.now();
  const mat = $.material("base");
  const intensity = isOn ? 1.0 : 0.0;
  const factor = isOn ? 4.0 : 0.2;
  mat.setEmissionColor(r * factor, g * factor, b * factor, 1.0);
  mat.setBaseColor(r, g, b, 1.0);
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function callMetaGadget(functionName, args, kwargs, meta) {
  assert(typeof(functionName) === "string", `functionName must be a string, but got ${functionName}`);
  assert(args === undefined || Array.isArray(args), `args must be an array, but got ${args}`);
  assert(kwargs === undefined || typeof(kwargs) === "object", `kwargs must be an object, but got ${kwargs}`);
  assert(meta === undefined || typeof(meta) === "string", `meta must be a string, but got ${meta}`);

  const requestBody = {
    "functionName": functionName,
    "args": args,
    "kwargs": kwargs
  }
  $.callExternal(JSON.stringify(requestBody), meta || "default meta");
}

function callGadget(functionName, ...args) {
  callMetaGadget(functionName, args, {}, "default meta");
}

$.onUpdate(deltaTime => {
  if ($.state.isOn && Date.now() - $.state.lastLightUpdated > 500) {
    setLight(false);
  }
})

$.onExternalCallEnd((response, meta, errorReason) => {
  $.log(`onExternalCallEnd response: ${response}, meta: ${meta}, errorReason: ${errorReason}`);
})

$.onInteract(() => {
  $.log("onInteract");
  setLight(!$.state.isOn);
  callGadget("botPress", BOT_DEVICE_ID);
});