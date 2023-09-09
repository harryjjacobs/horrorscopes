export const requestHorrorscope = (
  zodiac: string,
  date: Date
): Promise<string> => {
  const queryParams = new URLSearchParams({
    zodiac: zodiac,
    date: date.toLocaleDateString("en-GB"),
  });
  const myRequest = new Request(
    "https://horrorscope-api-7uspvmpy6a-nw.a.run.app/api/horrorscope?" +
      queryParams
  );

  return fetch(myRequest).then((response) => {
    if (!response.ok) {
      Promise.reject("Failed to find horrorscope for today");
    }
    return response.text();
  });
};
