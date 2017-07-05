$(window).keydown(function(e) {
  parent.postMessage({
    type: "openai.keydown",
    event: {
      which: e.which,
      key: e.key,
    },
  }, "*");
});

$(window).keyup(function(e) {
  parent.postMessage({
    type: "openai.keyup",
    event: {
      which: e.which,
      key: e.key,
    }
 }, "*");
});

$(window).mousemove(function(e) {
  parent.postMessage({
    type: "openai.mousemove",
    event: {
      screenX: e.screenX,
      screenY: e.screenY,
    },
  }, "*");
});

$(window).mouseup(function(e) {
  parent.postMessage({
    type: "openai.mouseup",
    event: {
      button: e.button,
    }
  }, "*");
});

$(window).mousedown(function(e) {
  parent.postMessage({
    type: "openai.mousedown",
    event: {
      button: e.button,
    }
  }, "*");
});

function get(query) {
  var lookup = $(query);
  if (lookup.length > 0)
    return lookup
  return undefined;
}

var scoreElt = undefined;
function refreshScoreElt() {
  scoreElt = get(".nsi span span:nth-child(2)");
}

var nickElt = undefined;
function refreshNickElt() {
  nickElt = get("input#nick.sumsginp");
}

window.setInterval(function() {
  if (scoreElt == undefined)
    return;
  else if (scoreElt.is(":hidden"))
    refreshScoreElt();

  parent.postMessage({
    type: "openai.score",
    score: scoreElt.text(),
  }, "*");
}, 16);

window.setInterval(function() {
  refreshScoreElt();
  refreshNickElt();

  // the score area: it's visible once the game starts, and at the end
  // of the game
  if (scoreElt !== undefined)
    var hasStarted = scoreElt.is(":visible");
  // the nickname box, visible before the game starts and also at the
  // end.
  if (nickElt !== undefined)
    var endzone = nickElt.is(":visible");

  message = "hasStarted="+hasStarted+" endzone="+endzone;
  if (hasStarted && endzone) {
    state = "gameover";
  } else if (hasStarted && !endzone) {
    state = "running";
  } else if (!hasStarted && endzone) {
    state = "initial";

    startOnce();
  } else if (!hasStarted && !endzone) {
    // must still be loading
    state = "initial";
  }
  
  parent.postMessage({
    type: "openai.status",
    state: state,
    message: message,
  }, "*")
}, 1000);

// Start the game!
var i = 0;
var started = false;
function startOnce() {
  if (started)
    return;
    
  var lowResolution = $("#grqi");
  if (lowResolution.length == 0) {
    console.log("No low resolution button to click yet");
    return;
  }
  started = true;

  lowResolution.click();

  nickElt.val("handbeezy");
  i++;

  console.log("[iframe] Clicking the Play button");
  $("div.nsi").click();
}
