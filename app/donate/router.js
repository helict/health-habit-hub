import express from "express";
import cookieParser from "cookie-parser";
import { showDonateForm, saveDonateData } from "./controllers.js";

const router = express.Router();

router.use(cookieParser());

router.get("/", showDonateForm);
router.post("/data", saveDonateData);

export default router;
