import { requestHorrorscope } from "./api";

export const displayHorrorscope = async (
  element: HTMLButtonElement,
  zodiac: string
) => {
  element.innerHTML = `<div class="loading-dots"></div>`;
  const date = new Date(Date.now());
  const month = date.toLocaleString("default", {
    month: "long",
    day: "numeric",
  });
  const horrorscope = await requestHorrorscope(zodiac, date)
    .then((horrorscope) => {
      return horrorscope;
    })
    .catch((error: string) => {
      return error;
    });
  element.innerHTML = `
    <h3>${
      zodiac.substring(0, 1).toUpperCase() + zodiac.substring(1)
    } Horrorscope ${month}</h3>
    <div>
      <p>${horrorscope}</p>
    </div>
  `;
};
