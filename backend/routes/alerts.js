const express = require("express");
const router = express.Router();

const {
  getAllAlerts,
  getAlertById,
  getAlertTrace,
  getAlertLLM,
  getAlertMitigation
} = require("../controllers/alertController");

// GET /alerts
router.get("/", getAllAlerts);

// GET /alerts/:id
router.get("/:id", getAlertById);

// GET /alerts/:id/trace
router.get("/:id/trace", getAlertTrace);

// GET /alerts/:id/llm
router.get("/:id/llm", getAlertLLM);

// GET /alerts/:id/mitigation
router.get("/:id/mitigation", getAlertMitigation);

module.exports = router;
