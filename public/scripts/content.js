function getAddressNode() {
  return document.querySelector("address");
}

function fetchAndInject() {
  const address_node = getAddressNode();
  console.log(address_node);
  if (!address_node) return;

  const origin = encodeURI(address_node.textContent.trim());
  const dest = encodeURI("600 W Chicago Ave, Chicago");
  const api = `https://lenses.jiechen.dev/api/get_commute?origin=${origin}&destination=${dest}&mode=transit`;

  fetch(api)
    .then((r) => r.json())
    .then((d) => {
      const latestCommuteTime = Math.floor(parseInt(d["duration"], 10) / 60);
      injectHi(address_node, latestCommuteTime);
    });
}

function injectHi(address_node, time) {
  const id = "chrome-ext-hi";
  let span = document.getElementById(id);
  if (!span) {
    span = document.createElement("div");
    span.id = id;
    address_node.parentNode.insertAdjacentElement("afterend", span);
  }
  span.textContent = `${time} Minutes`;
}

// Initial fetch
fetchAndInject();

// Watch for React wiping it out or address changing
const observer = new MutationObserver(() => {
  fetchAndInject();
});

const address_node = getAddressNode();
if (address_node && address_node.parentNode) {
  observer.observe(address_node.parentNode, {
    childList: true,
    subtree: true,
  });
}
