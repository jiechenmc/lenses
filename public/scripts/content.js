const address_node = document.querySelector("address");

const origin = encodeURI(address_node.textContent);
const dest = encodeURI("600 W Chicago Ave, Chicago");
const api = `http://34.229.111.5:8000/api/get_commute?origin=${origin}&destination=${dest}&mode=transit`;

fetch(api).then((r) =>
  r.json().then((d) => {
    console.log(d);
  })
);

function injectHi(address_node) {
  const id = "chrome-ext-hi";
  if (!document.getElementById(id)) {
    const span = document.createElement("div");
    span.textContent = "6 Minutes";
    span.id = id;
    address_node.parentNode.insertAdjacentElement("afterend", span);
  }
}

// Initial injection
injectHi(address_node);

// Watch for React wiping it out
const observer = new MutationObserver(() => {
  if (!document.getElementById("chrome-ext-hi")) {
    injectHi(address_node);
  }
});

observer.observe(address_node.parentNode, {
  childList: true,
});
