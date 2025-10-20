// Wait for tab to finish loading
function waitForTabLoad(tabId) {
  return new Promise(resolve => {
    const listener = (updatedTabId, info) => {
      if (updatedTabId === tabId && info.status === "complete") {
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }
    };
    chrome.tabs.onUpdated.addListener(listener);
  });
}

// Execute a single browser action inside the tab
function runAction(action) {
  const sleep = ms => new Promise(res => setTimeout(res, ms));

  const waitForSelector = async (selector, timeout = 10000) => {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const el = document.querySelector(selector);
      if (el) return el;
      await sleep(100);
    }
    throw new Error(`Timeout waiting for ${selector}`);
  };

    const resolveSelector = (selector) => {
        return selector === "input[aria-label='Search mail']" || selector === "input[aria-label*='Search mail']" || selector === 'input[aria-label="Search in mail"]'
            ? "input[name='q']"
            : "input";
    };

  (async () => {
    try {
      if (action.type === "wait" ) {
        await waitForSelector(resolveSelector(action.selector), action.timeout);
      } else if (action.type === "search") {
        const el = await waitForSelector(resolveSelector(action.selector));
        el.focus();
        el.value = action.text;
        el.dispatchEvent(new Event("input", { bubbles: true }));

        actionselec= action.selector;

      } else if (action.type === 'click' ) {
        const el = await waitForSelector(resolveSelector(actionselec || action.selector));
        el.focus();
        const eventOptions = {
          key: "Enter",
          code: "Enter",
          keyCode: 13,
          which: 13,
          bubbles: true
        };
        el.dispatchEvent(new KeyboardEvent("keydown", eventOptions));
        el.dispatchEvent(new KeyboardEvent("keypress", eventOptions));
        el.dispatchEvent(new KeyboardEvent("keyup", eventOptions));
        await waitForTabLoad(tab.id);
        const form = el.closest("form");
        if (form) {
          form.submit();
          console.log("✅ Submitted form manually");
        }
      }
    } catch (err) {
      console.error("Action failed:", action, err);
    }
  })();
}

let lastPlanHash = null;

// Poll bridge server for new plans
setInterval(pollForPlan, 1000);
async function pollForPlan() {
  try {
    console.log("🕵️ Polling bridge...");
    const res = await fetch("http://localhost:3001/plan");
    const plan = await res.json();

    if (plan && plan.actions) {
      const hashPlan = (plan) => JSON.stringify(plan);
      const currentHash = hashPlan(plan);
      if (currentHash === lastPlanHash) {
        console.log("⏸️ Skipping duplicate plan");
        return;
      }
      lastPlanHash = currentHash;

      console.log("🚀 Executing new plan:", plan);
      await executePlan(plan);

      // Clear the plan after execution
      await fetch("http://localhost:3001/plan", { method: "DELETE" });
    }
  } catch (err) {
    console.error("Polling failed:", err);
  }
}

// Execute full plan in active tab
async function executePlan(plan) {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  const goto = plan.actions.find(a => a.type === "goto");
  if (goto) {
    tab = await chrome.tabs.create({ url: goto.url });
    await waitForTabLoad(tab.id);
  }

  for (const action of plan.actions) {
    if (action.type === "goto") continue;

    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: runAction,
      args: [action]
    });
  }
}

// Keep service worker alive
function keepAlive() {
  setInterval(() => chrome.runtime.getPlatformInfo(() => {}), 20000);
}
keepAlive();





