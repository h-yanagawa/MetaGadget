stateOn = true;
$.onInteract(() => {
  const mh = $.material("heat");
  $.log("interacted.");
  if (stateOn) {
    stateOn = false;
    mh.setBaseColor(255, 255, 255, 1);
    mh.setEmissionColor(0, 0, 0, 0);
    $.callExternal("1 0", "heater");
  } else {
    stateOn = true;
    const mh = $.material("heat");
    mh.setBaseColor(255, 0, 0, 1);
    mh.setEmissionColor(255, 0, 0, 1);
    $.callExternal("1 50", "heater");
  }
});
