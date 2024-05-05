import randomProperty from "../utils/randomProperty.js";
import url from "url";

const experimentGroups = {
  closedTaskClosedDesc: "closedTaskClosedDesc",
  closedTaskOpenDesc: "closedTaskOpenDesc",
  openTaskClosedDesc: "openTaskClosedDesc",
  openTaskOpenDesc: "openTaskOpenDesc",
};

function isClosedTask(experimentGroup) {
  if (
    experimentGroup === experimentGroups.closedTaskClosedDesc ||
    experimentGroup === experimentGroups.closedTaskOpenDesc
  ) {
    return true;
  }
  return false;
}

function isClosedDescription(experimentGroup) {
  if (
    experimentGroup === experimentGroups.closedTaskClosedDesc ||
    experimentGroup === experimentGroups.openTaskClosedDesc
  ) {
    return true;
  }
  return false;
}

export function donate(req, res) {
  let experimentGroup = req.cookies.experimentGroup;
  console.log("Experiment Group: ", experimentGroup);
  if (!experimentGroup) {
    experimentGroup = randomProperty(experimentGroups);
    res.cookie("experimentGroup", experimentGroup);
  }
  res.render(url.fileURLToPath(new URL("views/donate.ejs", import.meta.url)), {
    experimentGroup: experimentGroup,
    closedTask: isClosedTask(experimentGroup),
    closedDescription: isClosedDescription(experimentGroup),
  });
}

export default {
  donate,
};
