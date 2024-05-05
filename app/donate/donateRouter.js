// Create ExpressJS Router
import express from "express";
import cookieParser from "cookie-parser";
import randomProperty from "../utils/randomProperty.js";

const experimentGroups = {
  closedTaskClosedDesc: "closedTaskClosedDesc",
  closedTaskOpenDesc: "closedTaskOpenDesc",
  openTaskClosedDesc: "openTaskClosedDesc",
  openTaskOpenDesc: "openTaskOpenDesc",
};

const router = express.Router();

router.use(cookieParser());

router.get("/", (req, res) => {
  let experimentGroup = req.cookies.experimentGroup;
  console.log("Experiment Group: ", experimentGroup);
  if (!experimentGroup) {
    experimentGroup = randomProperty(experimentGroups);
    res.cookie("experimentGroup", experimentGroup);
  }
  res.send(
    `Donate Page. Experiment Group: ${req.cookies.experimentGroup} -> ${experimentGroup}`
  );
});

export default router;
