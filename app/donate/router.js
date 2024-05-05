// Create ExpressJS Router
import express from "express";
import cookieParser from "cookie-parser";
import controllers from "./controllers.js";

const router = express.Router();

router.use(cookieParser());

router.get("/", controllers.donate);

export default router;
