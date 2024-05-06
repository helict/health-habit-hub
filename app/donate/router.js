import express from "express";
import cookieParser from "cookie-parser";
import { showDonateForm } from "./controllers.js";

const router = express.Router();

router.use(cookieParser());

router.get("/", showDonateForm);

export default router;
