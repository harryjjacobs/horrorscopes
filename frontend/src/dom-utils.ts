const previousValues = {
  display: new WeakMap(),
};

export const hideElement = (element: HTMLElement) => {
  if (element.style.display && element.style.display != "none") {
    previousValues.display.set(element, element.style.display);
  }
  element.style.display = "none";
};

export const showElement = (element: HTMLElement) => {
  if (element.style.display && element.style.display != "none") {
    return;
  }
  if (previousValues.display.has(element)) {
    element.style.display = previousValues.display.get(element);
  } else {
    element.style.display = "inline-block";
  }
};
