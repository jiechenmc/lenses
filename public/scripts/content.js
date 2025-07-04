const address_node = document.querySelector("address");

const origin = encodeURI(address_node.textContent);
const dest = encodeURI("600 W Chicago Ave, Chicago");
const api = `https://lenses.jiechen.dev/api/get_commute?origin=${origin}&destination=${dest}&mode=transit`;

let latestCommuteTime = null;

fetch(api).then((r) =>
  r.json().then((d) => {
    latestCommuteTime = parseInt(parseInt(d["duration"].slice(0, -1)) / 60);
    injectHi(address_node, latestCommuteTime);
  })
);

function injectHi(address_node, time) {
  const id = "chrome-ext-hi";
  if (!document.getElementById(id)) {
    const span = document.createElement("div");
    span.textContent = `${time} Minutes`;
    span.id = id;
    address_node.parentNode.insertAdjacentElement("afterend", span);
  }
}

// Watch for React wiping it out
const observer = new MutationObserver(() => {
  if (!document.getElementById("chrome-ext-hi") && latestCommuteTime !== null) {
    injectHi(address_node, latestCommuteTime);
  }
});

observer.observe(address_node.parentNode, {
  childList: true,
});
