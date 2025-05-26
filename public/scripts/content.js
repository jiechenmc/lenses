const addHelloToAddresses = () => {
  const addresses = document.querySelectorAll("address");

  for (const address of addresses) {
    if (!address.querySelector(".badge")) {
      const p = document.createElement("div");
      p.innerText = "Hello World";
      p.className = ".badge";
      address.appendChild(p);
    }
  }
};

addHelloToAddresses();

const observer = new MutationObserver(() => {
  addHelloToAddresses();
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});
