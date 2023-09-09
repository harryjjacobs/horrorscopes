import "./style.css";
import { displayHorrorscope as loadHoroscope } from "./horrorscope";
import { hideElement, showElement } from "./dom-utils";

type Params = { [key: string]: string };

const render = (params: Params) => {
  const horrorscopeElement =
    document.querySelector<HTMLButtonElement>("#horrorscope")!;
  const zodiacMenuElement =
    document.querySelector<HTMLButtonElement>("#zodiac-menu")!;
  const backButtonElement = document.querySelector<HTMLElement>("#nav-back")!;

  if ("zodiac" in params) {
    const zodiac = params["zodiac"];
    hideElement(zodiacMenuElement);
    loadHoroscope(horrorscopeElement, zodiac);
    showElement(horrorscopeElement);
    showElement(backButtonElement);
  } else {
    hideElement(horrorscopeElement);
    hideElement(backButtonElement);
    showElement(zodiacMenuElement);
  }
};

const parseHash = () => {
  if (window.location.hash) {
    return window.location.hash
      .substring(1)
      .split("=")
      .reduce((acc, _, index, arr) => {
        if (index % 2 == 0) {
          acc[arr.splice(index, 1)[0]] = arr.splice(index, 1)[0];
        }
        return acc;
      }, {} as { [key: string]: string });
  }
  return {};
};

document.addEventListener("DOMContentLoaded", (_) => {
  render(parseHash());
});

onhashchange = (_) => {
  render(parseHash());
};
