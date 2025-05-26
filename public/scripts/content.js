const createBadge = (type, data) => {
  const crimeThresh = { low: 0, medium: 10, high: 30 };
  const commuteThresh = { low: 0, medium: 30, high: 60 };

  const element = document.createElement("div");

  switch (type) {
    case "crime":
      element.innerText = `👮 ${data}`;
      if (data > crimeThresh["high"]) element.className = "badge error";
      else if (data > crimeThresh["high"]) element.className = "badge warning";
      else element.className = "badge success";
      break;
    case "commute":
      element.innerText = `🚗 ${data}`;
      if (data > commuteThresh["high"]) element.className = "badge error";
      else if (data > commuteThresh["high"])
        element.className = "badge warning";
      else element.className = "badge success";
      break;
  }

  return element;
};

const addBadgeToAddresses = () => {
  const addresses = document.querySelectorAll("address");

  for (const address of addresses) {
    const fakeData = {
      crime_rate: Math.floor(Math.random() * 100) + 1,
      commute: Math.floor(Math.random() * 100) + 1,
      schools: [],
      convenient_stores: [],
    };

    if (!address.parentElement.parentElement.querySelector(".badge")) {
      const crime = createBadge("crime", `${fakeData["crime_rate"]}`);
      const commute = createBadge("commute", fakeData["commute"]);

      const container = document.createElement("div");

      container.appendChild(crime);
      container.appendChild(commute);

      address.parentElement.parentElement.insertAdjacentElement(
        "beforeend",
        container
      );
    }
  }
};

const observer = new MutationObserver((mutations, obs) => {
  observer.disconnect();
  addBadgeToAddresses();
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});
