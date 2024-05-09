import url from "url";

const dummyContent = {
  title: null,
  // TODO: Add all other variables used in about.ejs file
};

export function renderAboutPage(req, res) {
  res.render(
    url.fileURLToPath(new URL("../views/about.ejs", import.meta.url)),
    dummyContent
  );
}
