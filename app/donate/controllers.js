import randomProperty from "../utils/randomProperty.js";
import url from "url";

const experimentGroups = {
  closedTaskClosedDesc: "closedTaskClosedDesc",
  closedTaskOpenDesc: "closedTaskOpenDesc",
  openTaskClosedDesc: "openTaskClosedDesc",
  openTaskOpenDesc: "openTaskOpenDesc",
};

export function donate(req, res) {
  let experimentGroup = req.cookies.experimentGroup;
  console.log("Experiment Group: ", experimentGroup);
  if (!experimentGroup) {
    experimentGroup = randomProperty(experimentGroups);
    res.cookie("experimentGroup", experimentGroup);
  }
  //   res.sendFile("views/donate.html", { root: __dirname });
  res.sendFile(
    url.fileURLToPath(new URL("views/donate.html", import.meta.url))
  );
}

export default {
  donate,
};
