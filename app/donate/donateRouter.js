// Create ExpressJS Router
import express from "express";

const router = express.Router();

router.get("/", (req, res) => {
  res.send("Donate Page");
});

export default router;
