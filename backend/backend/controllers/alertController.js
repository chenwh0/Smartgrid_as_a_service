const path = require("path");
const alerts = require("../data/alerts.json");
const { validateAll } = require("../utils/validateSchema");

// Validate all alerts once on load
validateAll(alerts);

// Helper to find alert by ID
function findAlertById(id) {
  return alerts.find((a) => a.alert_id === id);
}

// GET /alerts
function getAllAlerts(req, res, next) {
  try {
    // For table, we can just send everything (frontend can choose fields)
    res.json(alerts);
  } catch (err) {
    next(err);
  }
}

// GET /alerts/:id
function getAlertById(req, res, next) {
  try {
    const { id } = req.params;
    const alert = findAlertById(id);

    if (!alert) {
      return res.status(404).json({ error: `Alert with id ${id} not found` });
    }

    res.json(alert);
  } catch (err) {
    next(err);
  }
}

// GET /alerts/:id/trace
function getAlertTrace(req, res, next) {
  try {
    const { id } = req.params;
    const alert = findAlertById(id);

    if (!alert) {
      return res.status(404).json({ error: `Alert with id ${id} not found` });
    }

    res.json({
      alert_id: alert.alert_id,
      packet_trace: alert.packet_trace
    });
  } catch (err) {
    next(err);
  }
}

// GET /alerts/:id/llm
function getAlertLLM(req, res, next) {
  try {
    const { id } = req.params;
    const alert = findAlertById(id);

    if (!alert) {
      return res.status(404).json({ error: `Alert with id ${id} not found` });
    }

    res.json({
      alert_id: alert.alert_id,
      llm_reasoning: alert.llm_reasoning
    });
  } catch (err) {
    next(err);
  }
}

// GET /alerts/:id/mitigation
function getAlertMitigation(req, res, next) {
  try {
    const { id } = req.params;
    const alert = findAlertById(id);

    if (!alert) {
      return res.status(404).json({ error: `Alert with id ${id} not found` });
    }

    res.json({
      alert_id: alert.alert_id,
      mitigation_action: alert.mitigation_action,
      rule_based_action: alert.rule_based_action,
      llm_verification: alert.llm_verification,
      current_status: alert.current_status
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  getAllAlerts,
  getAlertById,
  getAlertTrace,
  getAlertLLM,
  getAlertMitigation
};
